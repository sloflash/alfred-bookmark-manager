# Alfred Bookmark Manager

A powerful Alfred workflow to manage Chrome bookmarks and open tabs. This tool allows you to search through your Chrome bookmarks, view open tabs, and create new bookmarks with custom folder structures.

## Features

- Search through Chrome bookmarks with `bm [query]`
- View and manage open Chrome tabs with `bms`
- Create bookmarks with custom folder structures
- Support for nested folder hierarchies
- Quick access to frequently used bookmarks

## Installation

1. Ensure you have Alfred installed with the Powerpack
2. Clone this repository
3. Double click the `.alfredworkflow` file to install

## Usage

### Basic Commands

- `bm [query]` - Search through your Chrome bookmarks
- `bms` - View open Chrome tabs

### Creating Bookmarks

You can create bookmarks in two ways:

1. From a URL directly:
   ```
   bms "www.example.com" folder "Bookmark Title"
   ```
   This creates a bookmark in the specified folder.

2. With nested folders:
   ```
   bms "www.example.com" folder/subfolder/subsubfolder "Bookmark Title"
   ```
   This creates the folder structure if it doesn't exist and adds the bookmark.

### Working with Open Tabs

1. View open tabs:
   - Type `bms` to see a list of currently open Chrome tabs
   - Select a tab to copy its URL
   - Press space to enter bookmark creation mode

2. Create bookmark from open tab:
   - Select a tab from the list
   - Press space
   - Type the folder path and title:
     ```
     folder/path "Bookmark Title"
     ```

## Requirements

- Python 3.6+
- Google Chrome
- Alfred Powerpack
- macOS (Chrome bookmark access is macOS specific)

## Technical Details

The workflow uses Chrome's bookmark file and history database to:
- Access and modify bookmarks
- Read currently open tabs
- Create folder structures
- Manage bookmark metadata

## License

MIT License 