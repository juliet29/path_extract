from typing import Literal, NamedTuple, TypedDict

## Markers
POINT_SIZE = 1000


## Axes
LABEL_ANGLE = -20
NUMBER_FORMAT = ".2s"
CARBON_EMIT_LABEL = "Equivalent Carbon Emissions [kg-Co2-e]"


# Size of the plot 
class Dimensions(TypedDict):
    width: int
    height: int
DEF_DIMENSIONS: Dimensions = {"width": 340, "height": 300}



## Rendering 
RendererTypes = Literal["browser", "html"]
BROWSER = "browser"
HTML = "html"
