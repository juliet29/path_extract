from enum import StrEnum
from typing import Literal
from typing import TypedDict

class Headings(StrEnum):
    CARBON_IMPACT = "Carbon Impact"
    EMBODIED_CARBON_EMISSIONS = "Embodied Carbon Emissions"


class ClassNames(StrEnum):
    SECTION = "section-header"
    TYPE = "type-header"
    CATEGORY = "category-header"
    ELEMENT = "element-name"
    VALUE = "element-co2"
    SEQUESTERING = "seq"


class TableNames(StrEnum):
    UNIT = "units"



class ExperimentInfo(TypedDict):
    project: str
    experiment: str
    index: int
# For testing! 
