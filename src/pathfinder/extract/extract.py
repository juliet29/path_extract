from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag
from pathfinder.paths import SAMPLE_HTML
from pathfinder.constants import ClassNames
from pathlib import Path
import polars as pl
from rich import print as rprint 
import pandas as pd

def is_category_header(tag: Tag):
	# TODO also will be a table row.. 
	if tag.has_attr('class'):
		if ClassNames.CATEGORY.value in tag["class"]:

			return True
		
def is_element_row(tag: Tag):
	if tag.has_attr('class'):
		if len(tag["class"]) == 0:
			return True
		
def is_type_header(tag: Tag):
	if tag.has_attr('class'):
		if ClassNames.TYPE.value in tag["class"]:
			return True
		

def get_category_name(tag: Tag):
	return tag.td.get_text()

def get_element_name(tag: Tag):
	td = tag.find("td", ClassNames.ELEMENT.value)
	assert isinstance(td, Tag)
	return td.get_text()


		
def extract_data(path:Path) -> pl.DataFrame:
	soup = BeautifulSoup(open(SAMPLE_HTML), features="html.parser")
	all_rows = [i for i in soup.find_all("tr") if isinstance(i, Tag) ]
	#print(f"all_rows: {all_rows}")

	# category_0 = soup.find("tr", class_ = ClassNames.CATEGORY.value)
	# print(f"cat 0: {category_0}")

	data = {}
	curr_category = ""
	for row in all_rows:
		if is_category_header(row):
			category = get_category_name(row)
			
			# start new thing..
			# rprint(f"-- CAT: {get_category_name(row)}")
			if category not in data.keys():
				data[category] = []
			curr_category = category

		if curr_category:
			if is_element_row(row):
				data[curr_category].append(get_element_name(row))

		# TODO want to split the section headers.. 

	rprint(data)

		



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