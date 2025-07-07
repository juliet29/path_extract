from enum import StrEnum
from typing import TypedDict

# TODO can do "linked str enums.. "
class Emissions(StrEnum):
    EMBODIED = "Embodied"
    OPERATIONAL = "Operational"
    BIOGENIC = "Biogenic"
    STORAGE = "Carbon Stored"

class Area(StrEnum):
    TOTAL = "Site"
    PLANTED = "Planted"

class Other(StrEnum):
    NET = "Net"
    EMIT_PA = "Emissions per Area"
    SEQ_PA = "Seq per Area"



overview_map = {
    'Net Impact over 60 years': Other.NET,
    'Total Embodied Emissions': Emissions.EMBODIED,
    'Total Biogenic(Sequestration + Emissions)': Emissions.BIOGENIC,
    'Total Operational Emissions': Emissions.OPERATIONAL,
    'Total Carbon Stored': Emissions.STORAGE,
    'Site Area': Area.TOTAL,
    'Planted Area': Area.PLANTED,
    'Emissions per Area': Other.EMIT_PA,
    'Sequestration per Area': Other.SEQ_PA
}

# class OverviewNames(StrEnum):
#     EMBODIED = "Total Embodied Emissions"
#     OPERATIONAL = "Total Biogenic(Sequestration + Emissions)"
#     BIOGENIC = "Biogenic"
#     STORAGE = "Carbon Stored"



class Headings(StrEnum):
    CARBON_IMPACT = "Carbon Impact"
    EMBODIED_CARBON_EMISSIONS = "Embodied Carbon Emissions"
    BIOGENIC = "Biogenic (Sequestration + Emissions)"


class ClassNames(StrEnum):
    SECTION = "section-header"
    TYPE = "type-header"
    CATEGORY = "category-header"
    ELEMENT = "element-name"
    VALUE = "element-co2"
    SEQUESTERING = "seq"






class TableNames(StrEnum):
    UNIT = "units"
    CUSTOM_CATEGORY = "custom_category"
    NAME = "names"



class ExperimentInfo(TypedDict):
    project: str
    experiment: str
    index: int
# For testing! 

