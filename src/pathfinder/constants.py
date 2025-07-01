from enum import StrEnum
from typing import Literal

class Headings(StrEnum):
    CARBON_IMPACT = "CARBON IMPACT"
    EMBODIED_CARBON_EMISSIONS = "Embodied Carbon Emissions"


class ClassNames(StrEnum):
    SECTION = "section-header"
    TYPE = "type-header"
    CATEGORY = "category-header"
    ELEMENT = "element-name"
    VALUE = "element-co2"


class TableNames(StrEnum):
    UNIT = "units"


# For testing! 
sample_categories = ["Aggregate Asphalt Hardscape", "Brick Stone Hardscape", "Concrete Hardscape"]
sample_elements = ["Asphalt Curb", "Brick Paving", "Cast-in-Place Concrete Paving"]
sample_values = [0,0, 4_082]