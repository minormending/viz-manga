# Viz Manga Viewer
Retrieves and unobfuscates manga pages for an input chapter id. Manga pages can be saves the dual spread images as well as single page images. Chapter ids need to be retrieved from the Viz site by looking at the chapter url.

DISCLAIMER: I am not licensed or affiliated with Viz Media and this repository is meant for informational purposes only. Please delete the retrieved pages after reading.

# Installation
```
pip install viz_manga
```

# Usage
```
usage: manga.py [-h] [--directory DIRECTORY] [--combine] chapter_id

Unobfuscates an entire manga chapter for reading.

positional arguments:
  chapter_id            Chapter id obtained from the Viz site.

options:
  -h, --help            show this help message and exit
  --directory DIRECTORY
                        Output directory to save the unobfuscated pages.
  --combine             Combine left and right pages into one image.
```

# Example
```
>>> python manga.py 24297 --directory images/ --combine

INFO:root:Getting 20 pages for One Piece Chapter 1047.0
Successfully retrieved chapter 24297

```

# Docker
```
>>> docker build -t viz-manga .
>>> docker run -v /home/user/images/:/app/images viz-manga  24297 --directory images/ --combine

INFO:root:Getting 20 pages for One Piece Chapter 1047.0
Successfully retrieved chapter 24297

```