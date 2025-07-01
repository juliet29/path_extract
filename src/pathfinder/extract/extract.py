from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag
from pathfinder.paths import SAMPLE_HTML
from pathfinder.constants import ClassNames, TableNames
from pathlib import Path
import polars as pl
from rich import print as rprint 
import pandas as pd
from collections import Counter
from typing import NamedTuple
import re

ValueAndUnit = NamedTuple("ValueAndUnit", [("value", int), ("unit", str)])


def is_header_of_class_type(tag: Tag, class_:ClassNames):
	if tag.has_attr('class'):
		if class_.value in tag["class"]:
			return True



def get_header_name(tag: Tag):
	return tag.td.get_text(strip=True)
		
def is_element_row(tag: Tag):
	if tag.has_attr('class'):
		if len(tag["class"]) == 0:
			return True

def get_element_name(tag: Tag):
	td = tag.find("td", ClassNames.ELEMENT.value)
	assert isinstance(td, Tag)
	# TODO add to obsidian [drop excess white space with regex](https://stackoverflow.com/questions/1546226/is-there-a-simple-way-to-remove-multiple-spaces-in-a-string)
	return re.sub(' +', ' ', td.get_text(strip=True)).replace("\n", "")


def get_element_value(tag: Tag):
	td = tag.find("td", ClassNames.VALUE.value)
	assert isinstance(td, Tag)
	
	result =  td.get_text("|", strip=True).split(" ")
	if len(result) == 2:
		return ValueAndUnit(*result)
	if len(result) == 1:
		return ValueAndUnit(0, None)
	else:
		raise NotImplementedError(f"Invalid result: `{result}` - should have len 1 or 2, but has len {len(result)}")






def create_meta_lists(_class: ClassNames,  row: Tag,  curr_value=""):
	if is_header_of_class_type(row, _class):
		curr_value = get_header_name(row)
	return curr_value



		
def extract_data(path:Path) -> pl.DataFrame:
	soup = BeautifulSoup(open(path), features="html.parser")
	all_rows = [i for i in soup.find_all("tr") if isinstance(i, Tag) ]

	type_counter = Counter()
	section_counter = Counter()
	category_counter = Counter()
	elements = []
	values:list[ValueAndUnit] = []

	curr_section = ""
	curr_type = ""
	curr_category = ""
	for row in all_rows:
		# type_counter = Counter()
		curr_section = create_meta_lists(ClassNames.SECTION, row,  curr_section )

		curr_type = create_meta_lists(ClassNames.TYPE, row,  curr_type)

		curr_category = create_meta_lists(ClassNames.CATEGORY, row,  curr_category)


		if curr_category:
			if is_element_row(row):
				elements.append(get_element_name(row))
				values.append(get_element_value(row))
				section_counter[curr_section]+=1
				type_counter[curr_type]+=1
				category_counter[curr_category]+=1
		

		# TODO want to split the section headers.. 

	# rprint(data)
	# rprint(section_counter)
	# rprint(type_counter)
	# rprint(category_counter)
	# rprint(values)
	rprint(elements)
	# rprint(section_counter.total(), type_counter.total(), category_counter.total())

	assert section_counter.total() == type_counter.total() == category_counter.total() == len(elements)

	data = {
		ClassNames.SECTION.name: section_counter.elements(),
        ClassNames.TYPE.name: type_counter.elements(),
        ClassNames.CATEGORY.name: category_counter.elements(),
        ClassNames.ELEMENT.name: elements,
        ClassNames.VALUE.name: [i.value for i in values],
        TableNames.UNIT.name: [i.unit for i in values],
    }

	df = pd.DataFrame(data)

	rprint(df.head(8))

	return df



		



	# get all the table rows... 
	# find the first TYPE table row.. 
	# for row in row if row is not type, add to list.. 

	

	# type_0 = soup.find("tr", class_ = ClassNames.TYPE.value)
	# print(f"cat 0: {type_0}")
	# assert isinstance(type_0, Tag)

	# type_1 = type_0.find_next("tr",  class_ = ClassNames.TYPE.value)
	# print(f"cat 1: {type_1}")
	# assert isinstance(type_1, Tag)

	# forward_categories = type_0.find_all_next("tr", class_=ClassNames.CATEGORY.value)
	# backward_categories = type_1.find_all_previous("tr", class_=ClassNames.CATEGORY.value)
	# print(f"forward: {forward_categories}")
	# print(f"backward: {backward_categories}")

	# TODO could keep list of seen values when going backwards.. 
		




def extract_data1(path:Path) -> pl.DataFrame:
	BREAK_NUM = 10

	soup = BeautifulSoup(open(SAMPLE_HTML), features="html.parser")
	categories = soup.find_all("tr", class_=ClassNames.CATEGORY.value)
	category_tags = [i for i in categories if  isinstance(i, Tag)]

	for category in category_tags:
		category_name = category.find("td").get_text()
		rprint(f"CURRENT CATEGORY: {category_name}")

		try: 
			rprint(f"NEXT CATEGORY: <<<{category.find_next_sibling("tr", class_=ClassNames.CATEGORY.value)}>>>")
		except AttributeError:
			pass

		
		rprint(category.find_next_sibling().find("td", class_=ClassNames.ELEMENT.value))
		# TODO get element names, except they are not nested...
		
		

	



if __name__ == "__main__":
	extract_data(SAMPLE_HTML)