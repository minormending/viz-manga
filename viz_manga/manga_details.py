import re
from bs4 import BeautifulSoup, ResultSet, Tag
from requests import Response, Session


class VizMangaDetails:
    def __init__(self) -> None:
        self.session = Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
        }

    def get_series(self) -> None:
        url: str = "https://www.viz.com/shonenjump"
        resp: Response = self.session.get(url)

        soup: BeautifulSoup = BeautifulSoup(resp.text, "html.parser")
        series_section: Tag = soup.find(class_="section_chapters")
        series_table: Tag = series_section.find("div", {"class":"property-row"})
        series_tags: ResultSet = series_table.find_all(href=re.compile("/shonenjump/chapters/"), class_="o_chapters-link")
        for series_tag in series_tags[0:3]:
            print(series_tag)


if __name__ == "__main__":
    details = VizMangaDetails()
    details.get_series()
