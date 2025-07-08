from typing import Literal
from enum import StrEnum

class UseCategories(StrEnum):
    DEMO = "Demolition"
    PREP = "Preparation"
    PRESERVED_PLANTING = "Preserved Planting / Restoration"
    NEW_PlANTING = "New Planting"  # TODO 'on-structure'
    SUBSTRUCTURE = "Substructure"
    GREEN_INFRA = "Green Infrasturcture"  # these are composites..
    HARDSCAPE = "Hardscape"
    ACCESSORIES = "Accessories"
    OPERATIONS = "Operations"




PathFinderCategories = Literal[
    "Exterior Lighting",
    "Demolition Site Preparation",
    "Perennials Perennial Grasses",
    "Green Infrastructure",
    "Landscape Water Use",
    "Metal Wood Hardscape",
    "Soil Amendments",
    "Playground Athletic",
    "Concrete Hardscape",
    "Furnishings",
    "Shrubs",
    "Planting Accessories",
    "Brick Stone Hardscape",
    "Ecosystem Restoration",
    "Site Elements",
    "Trees",
    "Aggregate Asphalt Hardscape",
    "Infrastructure Subsurface",
    "Lawn",
    "Trees Existing To Protect",
    "Ecosystems Existing To Protect",
]


pathfinder_categories:list[PathFinderCategories] = [
    "Exterior Lighting",
    "Demolition Site Preparation",
    "Perennials Perennial Grasses",
    "Green Infrastructure",
    "Landscape Water Use",
    "Metal Wood Hardscape",
    "Soil Amendments",
    "Playground Athletic",
    "Concrete Hardscape",
    "Furnishings",
    "Shrubs",
    "Planting Accessories",
    "Brick Stone Hardscape",
    "Ecosystem Restoration",
    "Site Elements",
    "Trees",
    "Aggregate Asphalt Hardscape",
    "Infrastructure Subsurface",
    "Lawn",
    "Trees Existing To Protect",
    "Ecosystems Existing To Protect",
]