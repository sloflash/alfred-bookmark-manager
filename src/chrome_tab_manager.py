#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import json
import logging
from typing import List, Dict, Optional
from pathlib import Path

class ChromeTabManager:
    def __init__(self):
        self.user_dir = os.path.expanduser('~')
        self.chrome_state_file = os.path.join(
            self.user_dir,
            'Library/Application Support/Google/Chrome/Default/Sessions/Tabs_*'
        )
        self.chrome_db = os.path.join(
            self.user_dir,
            'Library/Application Support/Google/Chrome/Default/History'
        )
        
    def get_open_tabs(self) -> List[Dict[str, str]]:
        """
        Get all open Chrome tabs from the current session
        """
        try:
            # Create a temporary copy of the History database since Chrome locks it
            temp_db = "/tmp/chrome_history_temp"
            os.system(f"cp '{self.chrome_db}' '{temp_db}'")
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            # Query for current tabs
            cursor.execute("""
                SELECT urls.url, urls.title 
                FROM urls 
                JOIN visits ON urls.id = visits.url 
                WHERE visits.visit_time > (
                    SELECT MAX(visit_time) - 86400000000 FROM visits
                )
                GROUP BY urls.url 
                ORDER BY MAX(visits.visit_time) DESC 
                LIMIT 50
            """)
            
            tabs = []
            for url, title in cursor.fetchall():
                if url and title:  # Filter out empty entries
                    tabs.append({
                        'title': title,
                        'url': url,
                        'source': 'chrome_tab'
                    })
            
            conn.close()
            os.remove(temp_db)
            
            return tabs
            
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