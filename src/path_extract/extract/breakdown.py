from bs4 import BeautifulSoup
from bs4.element import Tag
from path_extract.extract.helpers import (
    ValueAndUnit,
    create_list_of_class_type,
    get_element_name,
    get_element_value,
    is_element_row,
)
from path_extract.project_paths import SAMPLE_CLMT_BREAKDOWN_HTML
from path_extract.constants import ClassNames, TableNames
from pathlib import Path
import polars as pl
from rich import print as rprint

from collections import Counter


def read_breakdown(path: Path) -> pl.DataFrame:
    soup = BeautifulSoup(open(path), features="html.parser", from_encoding="utf-8")
    all_rows = [i for i in soup.find_all("tr") if isinstance(i, Tag)]

    category_counter = Counter()
    elements = []
    values: list[ValueAndUnit] = []

    type_counter = Counter()
    section_counter = Counter()

    curr_category = ""
    curr_section = ""
    curr_type = ""
    for row in all_rows:
        # type_counter = Counter()
        curr_section = create_list_of_class_type(ClassNames.SECTION, row, curr_section)
        curr_type = create_list_of_class_type(ClassNames.TYPE, row, curr_type)
        curr_category = create_list_of_class_type(
            ClassNames.CATEGORY, row, curr_category
        )

        if curr_category:
            if is_element_row(row):
                elements.append(get_element_name(row))
                values.append(get_element_value(row))

                category_counter[curr_category] += 1
                section_counter[curr_section] += 1
                type_counter[curr_type] += 1

    assert (
        section_counter.total()
        == type_counter.total()
        == category_counter.total()
        == len(elements)
    )

    data = {
        ClassNames.SECTION.name: section_counter.elements(),
        ClassNames.TYPE.name: type_counter.elements(),
        ClassNames.CATEGORY.name: category_counter.elements(),
        ClassNames.ELEMENT.name: elements,
        ClassNames.VALUE.name: [i.value for i in values],
        TableNames.UNIT.name: [i.unit for i in values],
    }
    return pl.DataFrame(data)


if __name__ == "__main__":
    df = read_breakdown(SAMPLE_CLMT_BREAKDOWN_HTML)
    rprint(df.head(10))
