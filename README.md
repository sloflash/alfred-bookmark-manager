# Alfred Bookmark Manager

A powerful Alfred workflow to manage Chrome bookmarks and open tabs.

## Features

- Search through Chrome bookmarks
- View and manage open Chrome tabs
- Create bookmarks with custom folder structures
- Quick access to frequently used bookmarks

## Installation

1. Ensure you have Alfred installed with the Powerpack
2. Clone this repository
3. Double click the `.alfredworkflow` file to install

## Usage

### Basic Commands

- `bm [query]` - Search through your Chrome bookmarks
- `bms` - View open Chrome tabs and create bookmarks

### Creating Bookmarks

You can create bookmarks in two ways:

1. From a URL:
   ```
   bms "www.example.com" folder "Bookmark Title"
   ```

2. From nested folders:
   ```
   bms "www.example.com" folder/subfolder "Bookmark Title"
   ```

## Requirements

- Python 3.6+
- Google Chrome
- Alfred Powerpack

## License

MIT License 