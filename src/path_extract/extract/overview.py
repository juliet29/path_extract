from bs4 import BeautifulSoup
from bs4.filter import SoupStrainer
from bs4.element import PageElement, Tag
from pathlib import Path
import polars as pl
from rich import print as rprint
from path_extract.project_paths import SAMPLE_CLMT_OVERVIEW_HTML
from path_extract.constants import Emissions, Area, overview_map, ClassNames, TableNames
from typing import NamedTuple
from path_extract.extract.helpers import ValueAndUnit, Comparison
import re
# key information

# just read main
MAIN_WRAPPER = "main-wrapper"

class DataRow(NamedTuple):  
    name: Tag  
    data: Tag


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
    # rprint(f"value: {value[0]}, unit: {value[1]}")

    integer_value = int(value[0].replace(",", ""))
    value_and_unit = ValueAndUnit(integer_value, value[1])
    if value_and_unit.unit == "Metric":
        value_and_unit = ValueAndUnit(integer_value, "Metric Tons")

    return name, value_and_unit

def process_overview(result_dict:dict): # TODO use constants! 
    data = {
        TableNames.NAME.name:[overview_map[i].value for i in result_dict.keys()],
        ClassNames.VALUE.name: [i.value for i in result_dict.values()],
        TableNames.UNIT.name: [i.unit for i in result_dict.values()],
    }
    # rprint(data)

    return pl.DataFrame(data)




def read_overview(path: Path):
    soup = BeautifulSoup(
        open(path),
        features="html.parser",
        from_encoding="utf-8",
        parse_only=SoupStrainer(id=MAIN_WRAPPER),
    )

    tags = [i for i in soup.find_all("div", class_="data-row") if isinstance(i, Tag)]

    result_dict = {}

    for tag in tags:
        name, value_and_unit = process_data_row(tag)
        result_dict[name] = value_and_unit
    return process_overview(result_dict) 



def get_overview_comparison(df):
    embodied = df.filter(pl.col(TableNames.NAME.name) == Emissions.EMBODIED.value)[ClassNames.VALUE.name].sum()
    biogenic = df.filter(pl.col(TableNames.NAME.name) == Emissions.BIOGENIC.value)[ClassNames.VALUE.name].sum()
    return Comparison(embodied, biogenic)


    

if __name__ == "__main__":
    df = read_overview(SAMPLE_CLMT_OVERVIEW_HTML)
    rprint(df)
    f = get_overview_comparison(df)
    rprint(f)
