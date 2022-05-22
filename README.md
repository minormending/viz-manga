# Viz Manga Viewer
Retrieves and deobfuscates manga pages for an input chapter id. Manga pages can be saves the dual spread images as well as single page images. Chapter ids need to be retrieved from the Viz site by looking at the chapter url.

DISCLAIMER: I am not licensed or affiliated with Viz Media and this repository is meant for informational purposes only. Please delete the retrieved pages after reading.

# Installation
```
pip install viz_manga
```

# Usage
The `VizMangaDetails` class can be used to lookup series and chapter metadata and the `VizMangaFetch` class is used to actually get the chapter pages.

To get all the series that are publicly available:
```
from viz_manga import VizMangaDetails, VizMangaFetch

details: VizMangaDetails = VizMangaDetails()
series: List[Series] = details.get_series()
```

To get all the chapters that are publicly free for a series:
```
series: Series = Series(None, "one-piece")
details: VizMangaDetails = VizMangaDetails()
for chapter in details.get_series_chapters(series):
    if chapter.is_free:
        print(chapter)
```

To get all pages for a chapter:
```
viz: VizMangaFetch = VizMangaFetch()
viz.save_chapter(24297, "images/", combine=True):
```

# CLI Usage
This module is bundled with a CLI script `viz-manga-cli` that allows the user to lookup and get chapters without writing any code.

```
usage: viz-manga-cli [-h] {fetch,series,chapters} ...

Lookup Viz manga information.

positional arguments:
  {fetch,series,chapters}
    fetch               Fetches and deobfuscates an entire manga chapter for reading.
    series              Get series title and slug (for chapter lookup) obtained from the Viz site.
    chapters            Get chapter title and id obtained from the Viz site.

options:
  -h, --help            show this help message and exit

```

## Lookup Manga Series
```
>>> viz-manga-cli series

{'name': '7thGARDEN', 'slug': '7th-garden'}
{'name': 'Agravity Boys', 'slug': 'agravity-boys'}
{'name': 'Akane-banashi', 'slug': 'akane-banashi'}
{'name': "Akira Toriyama's Manga Theater", 'slug': 'akira-toriyamas-manga-theater'}
{'name': 'All You Need is Kill', 'slug': 'all-you-need-is-kill-manga'}
{'name': 'Assassination Classroom', 'slug': 'assassination-classroom'}

```

## Lookup Manga Chapters
```
>>> viz-manga-cli chapters --help
usage: viz-manga-cli chapters [-h] [--free] series_slug

positional arguments:
  series_slug  Series title for which to lookup chapter ids from the Viz site.

options:
  -h, --help   show this help message and exit
  --free       Only show publicly available free chapters for the series.

>>> viz-manga-cli chapters 7th-garden

{'title': 'ch-1', 'id': '15220', 'link': 'https://www.viz.com/shonenjump/7th-garden-chapter-1/chapter/15220', 'is_free': True}
{'title': 'ch-2', 'id': '15221', 'link': 'https://www.viz.com/shonenjump/7th-garden-chapter-2/chapter/15221', 'is_free': True}
{'title': 'ch-3', 'id': '15222', 'link': 'https://www.viz.com/shonenjump/7th-garden-chapter-3/chapter/15222', 'is_free': True}
{'title': 'ch-4', 'id': '15223', 'link': 'https://www.viz.com/shonenjump/7th-garden-chapter-4/chapter/15223', 'is_free': False}
{'title': 'ch-5', 'id': '15224', 'link': 'https://www.viz.com/shonenjump/7th-garden-chapter-5/chapter/15224', 'is_free': False}

```

## Fetch Chapter
```
>>> viz-manga-cli fetch --help
usage: viz-manga-cli fetch [-h] [--directory DIRECTORY] [--combine] chapter_id

positional arguments:
  chapter_id            Chapter id obtained from the Viz site.

options:
  -h, --help            show this help message and exit
  --directory DIRECTORY
                        Output directory to save the deobfuscated pages.
  --combine             Combine left and right pages into one image.

>>> viz-manga-cli fetch 15220 --directory images/ --combine

INFO:root:Getting 79 pages for Root 1: The Demon's Servant
Successfully retrieved chapter 15220

```

# Docker
```
>>> docker build -t viz-manga .
>>> docker run -v /home/user/images/:/app/images viz-manga  fetch 24297 --directory images/ --combine

INFO:root:Getting 20 pages for One Piece Chapter 1047.0
Successfully retrieved chapter 24297

```