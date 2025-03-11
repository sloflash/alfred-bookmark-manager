#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import json
import logging
import time
import glob
from typing import List, Dict, Optional
from pathlib import Path

class ChromeTabManager:
    def __init__(self):
        self.user_dir = os.path.expanduser('~')
        self.chrome_state_dir = os.path.join(
            self.user_dir,
            'Library/Application Support/Google/Chrome/Default/Sessions'
        )
        self.chrome_snss_file = os.path.join(
            self.user_dir,
            'Library/Application Support/Google/Chrome/Default/Current Session'
        )
        
    def get_open_tabs(self) -> List[Dict[str, str]]:
        """
        Get all open Chrome tabs from the current session
        """
        try:
            # First try to get active tabs from Current Session
            if os.path.exists(self.chrome_snss_file):
                # Create a temporary copy since Chrome might lock the file
                temp_file = "/tmp/chrome_session_temp"
                os.system(f"cp '{self.chrome_snss_file}' '{temp_file}'")
                
                # Read the file in binary mode to find URLs
                with open(temp_file, 'rb') as f:
                    content = f.read()
                os.remove(temp_file)
                
                # Extract URLs from binary content
                tabs = []
                # Split on http/https and try to extract URLs
                parts = content.split(b'http')
                for part in parts[1:]:  # Skip first part before http
                    try:
                        # Convert to string and find end of URL
                        url_part = part.decode('utf-8', errors='ignore')
                        url_end = url_part.find('\x00')
                        if url_end > 0:
                            url = 'http' + url_part[:url_end]
                            if url.startswith('https://my.1password.com') or url.startswith('http://my.1password.com'):
                                title = "1Password Sign In"
                            else:
                                title = url.split('/')[-1] or url
                            tabs.append({
                                'title': title,
                                'url': url,
                                'source': 'chrome_tab'
                            })
                    except Exception as e:
                        logging.error(f"Error parsing URL: {e}")
                        continue
                
                # Log the results for debugging
                logging.info(f"Found {len(tabs)} open tabs")
                for tab in tabs:
                    logging.info(f"Tab: {tab['title']} - {tab['url']}")
                
                return tabs
            
            logging.error("No Current Session file found")
            return []
            
        except Exception as e:
            logging.error(f"Error getting open tabs: {e}")
            return []

    def create_bookmark(self, url: str, folder_path: str, title: str, bookmark_manager) -> bool:
        """
        Create a new bookmark in Chrome with the specified folder structure
        """
        try:
            # Get current bookmarks
            bookmarks = bookmark_manager.get_json_from_file()
            
            # Navigate to or create folder structure
            current_node = bookmarks['bookmark_bar']
            folder_parts = folder_path.split('/')
            
            for folder in folder_parts:
                # Find or create folder
                folder_found = False
                if 'children' not in current_node:
                    current_node['children'] = []
                
                for child in current_node['children']:
                    if child['type'] == 'folder' and child['name'] == folder:
                        current_node = child
                        folder_found = True
                        break
                
                if not folder_found:
                    new_folder = {
                        'type': 'folder',
                        'name': folder,
                        'children': []
                    }
                    current_node['children'].append(new_folder)
                    current_node = new_folder
            
            # Add bookmark to final folder
            bookmark = {
                'type': 'url',
                'name': title,
                'url': url
            }
            current_node['children'].append(bookmark)
            
            # Save updated bookmarks
            with open(bookmark_manager.chrome_path, 'w', encoding='utf-8') as f:
                json.dump({'roots': bookmarks}, f, indent=2)
            
            return True
            
        except Exception as e:
            logging.error(f"Error creating bookmark: {e}")
            return False 