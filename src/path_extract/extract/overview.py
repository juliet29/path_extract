from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag
from pathlib import Path
import polars as pl
from rich import print as rprint 
# key information

# just read main 

def read_breakdown(path:Path):
	soup = BeautifulSoup(open(path), features="html.parser", from_encoding='utf-8')