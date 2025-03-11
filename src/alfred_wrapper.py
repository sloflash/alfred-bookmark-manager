#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import logging
import subprocess

# Configure logging
log_dir = os.path.expanduser('~/Library/Logs/MayankBookmarkManager')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'alfred_wrapper.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s'
)

def main():
    """
    Wrapper script for Alfred to handle different commands
    """
    logging.info("=== Alfred Wrapper Started ===")
    logging.info(f"Command line arguments: {sys.argv}")
    
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bookmark_manager = os.path.join(script_dir, 'bookmark_manager.py')
    
    # Default command is search with no query
    command = 'search'
    query = None
    
    # Parse arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        logging.info(f"Argument: {arg}")
        
        if arg == 'bm':
            command = 'search'
            if len(sys.argv) > 2:
                query = sys.argv[2]
        elif arg == 'bms':
            command = 'create'
            if len(sys.argv) > 2:
                query = ' '.join(sys.argv[2:])
        elif arg == 'tabs':
            command = 'tabs'
        else:
            # If no recognized command, treat as search query
            command = 'search'
            query = arg
    
    # Build command
    cmd = [bookmark_manager, command]
    if query:
        cmd.append(query)
    
    logging.info(f"Executing command: {cmd}")
    
    try:
        # Execute the bookmark manager script
        result = subprocess.run(cmd, capture_output=True, text=True)
        logging.info(f"Return code: {result.returncode}")
        
        if result.stdout:
            logging.info(f"Output: {result.stdout[:200]}...")  # Log first 200 chars
            print(result.stdout)
        
        if result.stderr:
            logging.error(f"Error: {result.stderr}")
    except Exception as e:
        logging.error(f"Error executing command: {e}")
        print(json.dumps({
            "items": [
                {
                    "title": f"Error: {str(e)}",
                    "subtitle": "Please check the logs for details"
                }
            ]
        }))

if __name__ == '__main__':
    main() 