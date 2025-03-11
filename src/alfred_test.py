#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys
import os
import logging

# Configure logging
log_dir = os.path.expanduser('~/Library/Logs/MayankBookmarkManager')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'alfred_test.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s: %(message)s'
)

def main():
    logging.info("=== Alfred Test Script Started ===")
    logging.info(f"Command line arguments: {sys.argv}")
    logging.info(f"Current directory: {os.getcwd()}")
    
    # Return a simple test result
    print(json.dumps({
        "items": [
            {
                "title": "Test Item 1",
                "subtitle": "This is a test item",
                "arg": "test1",
                "text": {
                    "copy": "test1",
                    "largetype": "Test Item 1"
                }
            },
            {
                "title": "Test Item 2",
                "subtitle": "This is another test item",
                "arg": "test2",
                "text": {
                    "copy": "test2",
                    "largetype": "Test Item 2"
                }
            }
        ]
    }))

if __name__ == '__main__':
    main() 