#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
from src.bookmark_manager import BookmarkManager

def main():
    # Get the action from command line arguments
    action = sys.argv[1] if len(sys.argv) > 1 else None
    
    bm_manager = BookmarkManager()
    
    if action == 'tabs':
        # Get open tabs
        tabs = bm_manager.get_open_tabs()
        
        # Format for Alfred
        alfred_output = {
            "items": [
                {
                    "uid": tab['url'],
                    "title": tab['title'],
                    "subtitle": tab['url'],
                    "arg": tab['url'],
                    "autocomplete": tab['title'],
                    "text": {
                        "copy": tab['url'],
                        "largetype": tab['title']
                    }
                } for tab in tabs
            ]
        }
        
        print(json.dumps(alfred_output))
    
    elif action == 'create':
        # Expect additional arguments for bookmark creation
        if len(sys.argv) < 5:
            print(json.dumps({"items": [{"title": "Invalid bookmark creation command"}]}))
            return
        
        url = sys.argv[2]
        folder_path = sys.argv[3]
        title = sys.argv[4]
        
        success = bm_manager.create_bookmark(url, folder_path, title)
        
        if success:
            print(json.dumps({
                "items": [{
                    "title": "Bookmark Created Successfully",
                    "subtitle": f"{title} in {folder_path}",
                    "arg": url
                }]
            }))
        else:
            print(json.dumps({
                "items": [{
                    "title": "Failed to Create Bookmark",
                    "subtitle": f"Could not create {title} in {folder_path}"
                }]
            }))

if __name__ == '__main__':
    main() 