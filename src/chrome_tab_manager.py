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
        self.chrome_tabs_db = os.path.join(
            self.user_dir,
            'Library/Application Support/Google/Chrome/Default/History'
        )
        
    def get_open_tabs(self) -> List[Dict[str, str]]:
        """
        Get all open Chrome tabs from the current session using SQLite database
        """
        try:
            if not os.path.exists(self.chrome_tabs_db):
                logging.error(f"Chrome history database not found at: {self.chrome_tabs_db}")
                return []

            # Create a temporary copy of the database since Chrome might lock it
            temp_db = "/tmp/chrome_history_temp"
            os.system(f"cp '{self.chrome_tabs_db}' '{temp_db}'")
            
            tabs = []
            try:
                conn = sqlite3.connect(temp_db)
                cursor = conn.cursor()
                
                # Query for recently accessed tabs (within last hour)
                cursor.execute("""
                    SELECT title, url 
                    FROM urls 
                    WHERE last_visit_time > ? 
                    ORDER BY last_visit_time DESC 
                    LIMIT 20
                """, (int((time.time() - 3600) * 1000000 + 11644473600000000),))
                
                for row in cursor.fetchall():
                    title, url = row
                    if url and url.startswith('http'):
                        tabs.append({
                            'title': title or url.split('/')[-1] or url,
                            'url': url,
                            'source': 'chrome_tab'
                        })
                
                conn.close()
                
            except sqlite3.Error as e:
                logging.error(f"SQLite error: {e}")
            finally:
                try:
                    os.remove(temp_db)
                except:
                    pass
            
            # Log the results for debugging
            logging.info(f"Found {len(tabs)} open tabs")
            for tab in tabs:
                logging.info(f"Tab: {tab['title']} - {tab['url']}")
            
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