import pytest
import polars as pl

from path_extract.constants import (
    ClassNames,
    Headings,
)
from path_extract.extract.extract import extract_data
from path_extract.extract.helpers import is_element_row, is_header_of_class_type
from path_extract.paths import SAMPLE_HTML
from rich import print as rprint
from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag


# @pytest.mark.skip("Trivial")
# def test_setup():
#     assert 1 + 1 == 2


def test_is_category_header():
    tag = """
        <tr class="category-header">
            <td colspan="2">Aggregate Asphalt Hardscape</td>
        </tr>
        """
    soup = BeautifulSoup(tag, features="html.parser")
    tr = soup.find("tr")
    assert isinstance(tr, Tag)
    result = is_header_of_class_type(tr, ClassNames.CATEGORY)
    assert result


def test_is_element_row():
    tag = """ 
        <tr class>
            <td class="element-name">Brick Paving</td>
            <td class="element-co2 neutral ">
                <span>0 kgCO₂e</span>
            </td>
        </tr>
    """
    soup = BeautifulSoup(tag, features="html.parser")
    tr = soup.find("tr")
    assert isinstance(tr, Tag)
    result = is_element_row(tr)
    assert result


# @pytest.mark.skip("Not here yet")
def test_html_to_df():
    sample_categories = ["Aggregate Asphalt Hardscape", "Brick Stone Hardscape", "Concrete Hardscape"]
    sample_elements = ["Asphalt Curb", "Brick Paving", "Cast-in-Place Concrete Paving"]
    sample_values = [0,0, 4082]
    sample_types = [Headings.EMBODIED_CARBON_EMISSIONS.value] * len(sample_categories)

    df = extract_data(SAMPLE_HTML)

    data = {
        ClassNames.TYPE.name: sample_types,
        ClassNames.CATEGORY.name: sample_categories,
        ClassNames.ELEMENT.name: sample_elements,
        ClassNames.VALUE.name: sample_values,
    }
    expected_df_top = pl.DataFrame(data)

    assert df.select(data.keys()).head(3).equals(expected_df_top)


if __name__ == "__main__":
    test_html_to_df()
