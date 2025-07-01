from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag
from path_extract.paths import SAMPLE_HTML
from path_extract.constants import ClassNames, TableNames
from pathlib import Path
import polars as pl
from rich import print as rprint 
import pandas as pd
from collections import Counter
from typing import NamedTuple
import re

ValueAndUnit = NamedTuple("ValueAndUnit", [("value", int), ("unit", str | None)])


		
def is_element_row(tag: Tag):
	if tag.has_attr('class'):
		if len(tag["class"]) == 0:
			return True

def get_element_name(tag: Tag):
	td = tag.find("td", class_=ClassNames.ELEMENT.value)
	assert isinstance(td, Tag)
	# TODO add to obsidian [drop excess white space with regex](https://stackoverflow.com/questions/1546226/is-there-a-simple-way-to-remove-multiple-spaces-in-a-string)
	return re.sub(' +', ' ', td.get_text(strip=True)).replace("\n", "")


def get_element_value(tag: Tag):
	td = tag.find("td", class_=ClassNames.VALUE.value)
	assert isinstance(td, Tag)
	
	result =  td.get_text("|", strip=True).split(" ")
	if len(result) == 2:
		return ValueAndUnit(int(result[0].replace(",", "")), result[1])
	if len(result) == 1:
		return ValueAndUnit(0, None)
	else:
		raise NotImplementedError(f"Invalid result: `{result}` - should have len 1 or 2, but has len {len(result)}")


def is_header_of_class_type(tag: Tag, class_:ClassNames):
	if tag.has_attr('class'):
		if class_.value in tag["class"]:
			return True
		
def get_header_name(tag: Tag):
	assert tag.td
	return tag.td.get_text(strip=True)


def create_list_of_class_type(_class: ClassNames,  row: Tag,  curr_value=""):
	if is_header_of_class_type(row, _class):
		curr_value = get_header_name(row)
	return curr_value



		
def extract_data(path:Path) -> pl.DataFrame:
	soup = BeautifulSoup(open(path), features="html.parser")
	all_rows = [i for i in soup.find_all("tr") if isinstance(i, Tag) ]

	category_counter = Counter()
	elements = []
	values:list[ValueAndUnit] = []

	type_counter = Counter()
	section_counter = Counter()

	curr_category = ""
	curr_section = ""
	curr_type = ""
	for row in all_rows:
		# type_counter = Counter()
		curr_section = create_list_of_class_type(ClassNames.SECTION, row,  curr_section )
		curr_type = create_list_of_class_type(ClassNames.TYPE, row,  curr_type)
		curr_category = create_list_of_class_type(ClassNames.CATEGORY, row,  curr_category)


		if curr_category:
			if is_element_row(row):
				elements.append(get_element_name(row))
				values.append(get_element_value(row))
				
				category_counter[curr_category]+=1
				section_counter[curr_section]+=1
				type_counter[curr_type]+=1
		

	assert section_counter.total() == type_counter.total() == category_counter.total() == len(elements)

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
	df = extract_data(SAMPLE_HTML)
	rprint(df.head(30))
