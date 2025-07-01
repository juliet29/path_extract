import pytest
import polars as pl
from pathfinder.constants import ClassNames, Headings, sample_categories, sample_elements, sample_values
from pathfinder.paths import SAMPLE_HTML
from rich import print as rprint
from pathfinder.extract.extract import extract_data, is_category_header
from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag

@pytest.mark.skip("Trivial")
def test_setup():
    assert 1 + 1 == 2

def test_is_category_header():
    tag = '<tr class="category-header"><td colspan="2">Aggregate Asphalt Hardscape</td></tr>'
    soup = BeautifulSoup(tag,  features="html.parser")
    tr = soup.find("tr")
    assert isinstance(tr, Tag)
    result = is_category_header(tr)
    assert result == True
     
     
    
@pytest.mark.skip("Not here yet")
def test_html_to_df():
    # for sample df, only have `Embodied Carbon Emissions
    # TODO read our SAMPLE_HTML

    df = extract_data(SAMPLE_HTML)

    data = {
        ClassNames.TYPE.name : [Headings.EMBODIED_CARBON_EMISSIONS.value]*len(sample_categories), 
        ClassNames.CATEGORY.name: sample_categories,
        ClassNames.ELEMENT.name: sample_elements,
        ClassNames.VALUE.name: [0,0, 4_082],

    }
    # TODO expect the rows to be in the dataframe.. 
    expected_df_top = pl.DataFrame(data)

    assert df.head(3) == expected_df_top
    
    

if __name__ == "__main__":
	test_html_to_df()