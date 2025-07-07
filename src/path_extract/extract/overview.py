from bs4 import BeautifulSoup
from bs4.filter import SoupStrainer
from bs4.element import PageElement, Tag
from pathlib import Path
import polars as pl
from rich import print as rprint
from path_extract.project_paths import SAMPLE_CLMT_OVERVIEW_HTML
from path_extract.constants import Emissions, Area
from typing import NamedTuple
from path_extract.extract.helpers import ValueAndUnit
import re
# key information

# just read main
MAIN_WRAPPER = "main-wrapper"

class DataRow(NamedTuple):  
    name: Tag  
    data: Tag

VALUE_MATCH = r"(((\d+),?)+)"
UNIT_MATCH = r"((([a-zA-Z/\u00B2\u2082]+)\s*)+)"

def match_value(pattern_str: str, text:str):
    # TODO write tests for this.. 
    pattern = re.compile(pattern_str)
    # find the first 
    res = pattern.match(text)
    assert res is not None, f"Invalid text: {text}"
    # rprint(res)
    return res.group()




def process_data_row(tag: Tag):
    # TODO helper tag filter.. 
    contents = [i for i in tag.children if isinstance(i, Tag)]
    # rprint(tag.get_text())
    # rprint(contents)
    assert len(contents) == 2, f"Unexpected format of `data-row` -> should have 2 subtags, instead has {len(contents)} : `{contents}`"
    data_row = DataRow(*contents)
    # name = data_row.name.get_text()
    name = re.sub(" +", " ", data_row.name.get_text(strip=True)).replace("\n", "")
    value = data_row.data.get_text().split(" ")#ValueAndUnit()
    assert len(value) >= 2, f"Unexpected format of `data-row` subtag. Should have at least length 2 for a value and a unit, but has len {len(value)}:  `{value}`"
    #rprint(f"name: {name}")
    rprint(f"value: {value[0]}, unit: {value[1]}")

    # rprint(f"res: {value_and_unit}. value: {match_value(VALUE_MATCH, value_and_unit)} | unit: {match_value(UNIT_MATCH, value_and_unit)}")
    integer_value = int(value[0].replace(",", ""))
    value_and_unit = ValueAndUnit(integer_value, value[1])
    if value_and_unit.unit == "Metric":
        value_and_unit = ValueAndUnit(integer_value, "Metric Tons")

    return name, value_and_unit


def read_overview(path: Path):
    soup = BeautifulSoup(
        open(path),
        features="html.parser",
        from_encoding="utf-8",
        parse_only=SoupStrainer(id=MAIN_WRAPPER),
    )
    # rprint(soup.prettify())
    # keys = [i for i in Emissions] + [i for i in Area]
    # key_values = [i.value for i in keys]
    tags = [i for i in soup.find_all("div", class_="data-row") if isinstance(i, Tag)]

    # rprint([i.prettify() for i in tags], "\n")
    result_dict = {}

    for tag in tags:
        name, value_and_unit = process_data_row(tag)
        result_dict[name] = value_and_unit

    rprint(result_dict)
    # TODO make into dataframe, differentiate betwen areas and not.. 

    return result_dict



    # # each has two sub elements..
    # test_res = res[0]
    # # TODO assert length of child is 2 
    # for child in test_res.contents:
    #     rprint(child)


    # extract all data -> use regexes for the Area values.. filter out stuff not needed 


    # COMPARE overview with breakdown! 
    

if __name__ == "__main__":
    read_overview(SAMPLE_CLMT_OVERVIEW_HTML)
    # rprint(df)
