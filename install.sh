#!/bin/bash

# Alfred Bookmark Manager Installation Script

echo "Installing Alfred Bookmark Manager..."

# Get the absolute path of the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Make sure all Python scripts are executable
chmod +x "$SCRIPT_DIR/src/bookmark_manager.py"
chmod +x "$SCRIPT_DIR/src/chrome_tab_manager.py"
chmod +x "$SCRIPT_DIR/src/alfred_wrapper.py"
chmod +x "$SCRIPT_DIR/src/alfred_test.py"

echo "All scripts are now executable."

# Create log directory
LOG_DIR="$HOME/Library/Logs/MayankBookmarkManager"
mkdir -p "$LOG_DIR"
echo "Log directory created at: $LOG_DIR"

# Print instructions for Alfred
echo ""
echo "=== Alfred Workflow Setup Instructions ==="
echo ""
echo "1. Open Alfred Preferences"
echo "2. Go to the Workflows tab"
echo "3. Click the + button at the bottom and select 'Blank Workflow'"
echo "4. Fill in the workflow details (name, description, etc.)"
echo ""
echo "5. Add a Script Filter for bookmark search:"
echo "   - Right-click in the workflow area and select 'Input > Script Filter'"
echo "   - Keyword: bm"
echo "   - Title: Search Bookmarks"
echo "   - Script: $SCRIPT_DIR/src/alfred_wrapper.py bm {query}"
echo "   - Language: /bin/bash"
echo ""
echo "6. Add a Script Filter for bookmark creation/tabs:"
echo "   - Right-click in the workflow area and select 'Input > Script Filter'"
echo "   - Keyword: bms"
echo "   - Title: Create Bookmark/Show Tabs"
echo "   - Script: $SCRIPT_DIR/src/alfred_wrapper.py bms {query}"
echo "   - Language: /bin/bash"
echo ""
echo "7. Connect the outputs to appropriate actions (e.g., 'Open URL')"
echo ""
echo "Installation complete!"
echo "You can test the scripts by running:"
echo "  $SCRIPT_DIR/src/alfred_wrapper.py bm"
echo "  $SCRIPT_DIR/src/alfred_wrapper.py bms"
echo "" 