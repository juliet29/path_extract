from bs4 import BeautifulSoup, SoupStrainer
from bs4.element import PageElement, Tag
from pathlib import Path
import polars as pl
from rich import print as rprint 
from path_extract.project_paths import SAMPLE_CLMT_OVERVIEW_HTML
# key information

# just read main 
MAIN_WRAPPER = "main-wrapper"

def read_overview(path:Path) -> dict:
	soup = BeautifulSoup(open(path), features="html.parser", from_encoding='utf-8', parse_only=SoupStrainer(id=MAIN_WRAPPER))
	
if __name__ == "__main__":
    df = read_overview(SAMPLE_CLMT_BREAKDOWN_HTML)
    rprint(df.head(10))