from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag
from pathfinder.paths import SAMPLE_HTML
from pathfinder.constants import ClassNames
from pathlib import Path
import polars as pl
from rich import print as rprint 

def is_category_header(tag: Tag):
	if tag.has_attr('class'):
		if ClassNames.CATEGORY.value in tag["class"]:

			return True
		
def extract_data(path:Path) -> pl.DataFrame:
	soup = BeautifulSoup(open(SAMPLE_HTML), features="html.parser")
	type_0 = soup.find("tr", class_ = ClassNames.TYPE.value)
	print(f"cat 0: {type_0}")
	assert isinstance(type_0, Tag)

	type_1 = type_0.find_next("tr",  class_ = ClassNames.TYPE.value)
	print(f"cat 1: {type_1}")
	assert isinstance(type_1, Tag)

	forward_categories = type_0.find_all_next("tr", class_=ClassNames.CATEGORY.value)
	backward_categories = type_1.find_all_previous("tr", class_=ClassNames.CATEGORY.value)
	print(f"forward: {forward_categories}")
	print(f"backward: {backward_categories}")

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