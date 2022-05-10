from dataclasses import dataclass
import re
from typing import List
from bs4 import BeautifulSoup, ResultSet, Tag
from requests import Response, Session

@dataclass
class Series:
    name: str
    slug: str

    @property
    def link(self) -> str:
        return f"https://www.viz.com/shonenjump/chapters/{self.slug}"


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
            name = series_tag.find_all("div", class_="type-center")[-1].text.strip()
            
            series.append(Series(name, slug))
        return sorted(series, key=lambda s: s.name.lower())

if __name__ == "__main__":
    details = VizMangaDetails()
    series: List[Series] = details.get_series()
    for manga in series:
        print(f"{manga.name} : {manga.slug}")
