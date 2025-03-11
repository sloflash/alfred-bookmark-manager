#!/usr/bin/python3
# -*- coding: utf-8 -*-

import codecs
import json
import os
import sys
import logging
from typing import List, Dict, Any, Union
from urllib.parse import urljoin

# Configure logging
log_dir = os.path.expanduser('~/Library/Logs/MayankBookmarkManager')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'bookmark_manager.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s'
)

# Chrome bookmark file path relative to HOME
CHROME_BOOKMARK_PATH = 'Library/Application Support/Google/Chrome/Default/Bookmarks'

class BookmarkManager:
    def __init__(self):
        self.user_dir = os.path.expanduser('~')
        self.chrome_path = os.path.join(self.user_dir, CHROME_BOOKMARK_PATH)
        logging.info(f"Chrome bookmarks path: {self.chrome_path}")

    def get_all_urls(self, the_json: Dict) -> List[Dict[str, str]]:
        """
        Extract all URLs and title from Chrome Bookmarks file
        """
        urls = []

        def extract_data(data: Dict):
            if isinstance(data, dict):
                if data.get('type') == 'url':
                    urls.append({
                        'title': data.get('name', 'Untitled'),
                        'url': data.get('url', ''),
                        'source': 'chrome'
                    })
                if data.get('type') == 'folder' and 'children' in data:
                    for child in data.get('children', []):
                        extract_data(child)

        def get_container(o: Union[List, Dict]):
            if isinstance(o, list):
                for i in o:
                    extract_data(i)
            if isinstance(o, dict):
                for k, i in o.items():
                    extract_data(i)

        try:
            get_container(the_json)
            return sorted(urls, key=lambda k: k['title'], reverse=False)
        except Exception as e:
            logging.error(f"Error extracting URLs: {e}")
            return []

    def get_json_from_file(self) -> Dict:
        """
        Get Bookmark JSON from Chrome bookmarks file
        """
        try:
            with codecs.open(self.chrome_path, 'r', 'utf-8-sig') as f:
                return json.load(f)['roots']
        except Exception as e:
            logging.error(f"Error reading Chrome bookmarks: {e}")
            return {}

    def search_bookmarks(self, query: str = None) -> List[Dict[str, str]]:
        """
        Search Chrome bookmarks
        """
        logging.info(f"Searching bookmarks. Query: {query}")

        if not os.path.exists(self.chrome_path):
            logging.error("Chrome bookmarks file not found")
            return []

        # Get all bookmarks
        bookmarks_json = self.get_json_from_file()
        all_bookmarks = self.get_all_urls(bookmarks_json)
        logging.info(f"Total bookmarks found: {len(all_bookmarks)}")

        # If query is empty or None, return first 20 bookmarks
        if not query:
            return all_bookmarks[:20]

        # Check if query contains a path suffix
        parts = query.split(' ', 1)
        search_query = parts[0].lower()
        path_suffix = parts[1] if len(parts) > 1 else ''

        # Filter bookmarks based on search query
        filtered_bookmarks = []
        for bookmark in all_bookmarks:
            if search_query in bookmark['title'].lower() or search_query in bookmark['url'].lower():
                # If path suffix exists, append it to the URL
                if path_suffix:
                    bookmark = bookmark.copy()
                    bookmark['url'] = urljoin(bookmark['url'], path_suffix.lstrip('/'))
                filtered_bookmarks.append(bookmark)

        logging.info(f"Filtered bookmarks: {len(filtered_bookmarks)}")
        return filtered_bookmarks

    def debug_bookmark_paths(self) -> List[str]:
        """
        Debug method to print out Chrome bookmark file location
        """
        if os.path.exists(self.chrome_path):
            return [f"Chrome bookmarks found at: {self.chrome_path}"]
        else:
            return [f"Chrome bookmarks NOT found at: {self.chrome_path}"]

def main():
    action = sys.argv[1] if len(sys.argv) > 1 else None
    
    bm_manager = BookmarkManager()
    
    if action == 'search':
        query = sys.argv[2] if len(sys.argv) > 2 else None
        bookmarks = bm_manager.search_bookmarks(query)
        print(json.dumps({
            "items": [
                {
                    "title": b['title'],
                    "subtitle": b['url'],
                    "arg": b['url'],
                    "text": {
                        "copy": b['url'],
                        "largetype": b['title']
                    }
                } for b in bookmarks
            ]
        }))
    
    elif action == 'debug_paths':
        paths = bm_manager.debug_bookmark_paths()
        print(json.dumps(paths))

if __name__ == '__main__':
    main() 