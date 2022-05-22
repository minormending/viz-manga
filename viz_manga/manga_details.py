from dataclasses import dataclass
import re
from typing import List
from bs4 import BeautifulSoup, ResultSet
from requests import Response, Session


@dataclass
class Series:
    name: str
    slug: str

    @property
    def link(self) -> str:
        return f"https://www.viz.com/shonenjump/chapters/{self.slug}"


@dataclass
class Chapter:
    title: str
    id: str
    link: str
    is_free: bool = False


class VizMangaDetails:
    def __init__(self) -> None:
        self.session = Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
        }

    def get_series(self) -> List[Series]:
        url: str = "https://www.viz.com/shonenjump"
        resp: Response = self.session.get(url)

        series_link_pattern: str = "/shonenjump/chapters/"

        soup: BeautifulSoup = BeautifulSoup(resp.text, "html.parser")
        series_tags: ResultSet = soup.find_all(
            href=re.compile(series_link_pattern), class_="o_chapters-link"
        )

        series: List[Series] = []
        for series_tag in series_tags:
            link: str = series_tag["href"]
            slug: str = link.replace(series_link_pattern, "").strip()
            name: str = series_tag.find_all("div", class_="type-center")[
                -1
            ].text.strip()

            series.append(Series(name, slug))
        return sorted(series, key=lambda s: s.name.lower())

    def get_series_chapters(self, series: Series) -> List[Chapter]:
        resp: Response = self.session.get(series.link)

        chapter_link_pattern: str = "/shonenjump/[^/]+/chapter/(\d+)"

        soup: BeautifulSoup = BeautifulSoup(resp.text, "html.parser")
        chapter_tags: ResultSet = soup.find_all(
            lambda tag: tag.name == "a"
            and "ch-" in tag.get("id", "")
            and re.search(chapter_link_pattern, tag.get("data-target-url", ""))
        )

        chapters: List[Chapter] = []
        for chapter_tag in chapter_tags:
            link: str = chapter_tag["data-target-url"]
            match: re.Match = re.search(chapter_link_pattern, link)
            chapter_id: str = match.group(1)
            link = f"https://www.viz.com{match.group(0)}"

            name: str = chapter_tag["id"]
            is_free: bool = "join to read" not in chapter_tag.get("href", "").lower()
            chapters.append(Chapter(name, chapter_id, link, is_free))
        return chapters
