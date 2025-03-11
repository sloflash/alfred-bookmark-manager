#!/usr/bin/env python3
import os
import shutil
import zipfile
import uuid

def create_alfred_workflow():
    # Workflow name and details
    workflow_name = "MayankBookmarkManager"
    bundle_id = "com.mketkar.bookmarkmanager"
    
    # Create temporary build directory
    build_dir = os.path.join('build', workflow_name)
    os.makedirs(build_dir, exist_ok=True)
    
    # Copy necessary files
    shutil.copy('src/bookmark_manager.py', build_dir)
    
    # Create Alfred script filter
    bm_script = '''#!/bin/bash
python3 bookmark_manager.py search "$1"'''
    
    # Write script filter file
    with open(os.path.join(build_dir, 'bm_search.sh'), 'w') as f:
        f.write(bm_script)
    os.chmod(os.path.join(build_dir, 'bm_search.sh'), 0o755)
    
    # Generate unique IDs for workflow elements
    script_filter_uid = str(uuid.uuid4())
    browser_uid = str(uuid.uuid4())
    
    # Create info.plist with Alfred configuration
    info_plist_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>bundleid</key>
    <string>com.mketkar.bookmarkmanager</string>
    <key>category</key>
    <string>Productivity</string>
    <key>connections</key>
    <dict>
        <key>%s</key>
        <array>
            <dict>
                <key>destinationuid</key>
                <string>%s</string>
                <key>modifiers</key>
                <integer>0</integer>
                <key>modifiersubtext</key>
                <string></string>
                <key>vitoclose</key>
                <false/>
            </dict>
        </array>
    </dict>
    <key>createdby</key>
    <string>Mayank Ketkar</string>
    <key>description</key>
    <string>Search Chrome bookmarks</string>
    <key>disabled</key>
    <false/>
    <key>name</key>
    <string>MayankBookmarkManager</string>
    <key>objects</key>
    <array>
        <dict>
            <key>config</key>
            <dict>
                <key>alfredfiltersresults</key>
                <false/>
                <key>argumenttype</key>
                <integer>0</integer>
                <key>escaping</key>
                <integer>102</integer>
                <key>keyword</key>
                <string>bm</string>
                <key>queuedelay</key>
                <integer>3</integer>
                <key>runningsubtext</key>
                <string>Searching bookmarks...</string>
                <key>script</key>
                <string>./bm_search.sh "{query}"</string>
                <key>scriptargtype</key>
                <integer>0</integer>
                <key>subtext</key>
                <string>Search your Chrome bookmarks</string>
                <key>title</key>
                <string>Search Bookmarks</string>
                <key>type</key>
                <integer>0</integer>
                <key>withspace</key>
                <true/>
            </dict>
            <key>type</key>
            <string>alfred.workflow.input.scriptfilter</string>
            <key>uid</key>
            <string>%s</string>
            <key>version</key>
            <integer>3</integer>
        </dict>
        <dict>
            <key>config</key>
            <dict>
                <key>browser</key>
                <string>com.google.Chrome</string>
                <key>spaces</key>
                <string></string>
                <key>url</key>
                <string>{query}</string>
                <key>utf8</key>
                <true/>
                <key>infront</key>
                <true/>
                <key>newwindow</key>
                <true/>
            </dict>
            <key>type</key>
            <string>alfred.workflow.action.openurl</string>
            <key>uid</key>
            <string>%s</string>
            <key>version</key>
            <integer>1</integer>
        </dict>
    </array>
    <key>readme</key>
    <string>Search your Chrome bookmarks with Alfred</string>
    <key>uidata</key>
    <dict>
        <key>%s</key>
        <dict>
            <key>xpos</key>
            <integer>100</integer>
            <key>ypos</key>
            <integer>100</integer>
        </dict>
        <key>%s</key>
        <dict>
            <key>xpos</key>
            <integer>300</integer>
            <key>ypos</key>
            <integer>100</integer>
        </dict>
    </dict>
    <key>version</key>
    <string>1.0.0</string>
    <key>webaddress</key>
    <string>https://github.com/mketkar</string>
</dict>
</plist>''' % (script_filter_uid, browser_uid, script_filter_uid, browser_uid, script_filter_uid, browser_uid)
    
    with open(os.path.join(build_dir, 'info.plist'), 'w') as f:
        f.write(info_plist_content)
    
    # Create .alfredworkflow file (zip)
    workflow_file = os.path.join('build', f'{workflow_name}.alfredworkflow')
    
    with zipfile.ZipFile(workflow_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(build_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, build_dir)
                zf.write(file_path, arcname)
    
    print(f"Alfred workflow created: {workflow_file}")

if __name__ == '__main__':
    create_alfred_workflow() 