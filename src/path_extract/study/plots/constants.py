from typing import Literal, TypedDict

from path_extract.project_paths import CLMTPath, ProjectNames
from path_extract.study.dataframes import edit_breakdown_df
import polars as pl
from rich import print as rprint
import altair as alt 


## Markers
POINT_SIZE = 1000


## Axes
LABEL_ANGLE = -20
NUMBER_FORMAT = ".2s"
NUMBER_FORMAT_3 = ".3s"
CARBON_EMIT_LABEL = "Equivalent Carbon Emissions [kg-Co2-e]"
AS_DESIGNED = "As Designed"
ALTERNATIVE = "Alternative"


# Size of the plot
class Dimensions(TypedDict):
    width: int
    height: int


DEF_DIMENSIONS: Dimensions = {"width": 340, "height": 300}


## Rendering
RendererTypes = Literal["browser", "html"]
BROWSER = "browser"
HTML = "html"


# TODO share with pres works
def get_exp_df(
    project_name: ProjectNames,
    exp_num: int,
):
    clmt_path = CLMTPath(project_name)
    init_df = clmt_path.read_csv(exp_num)
    return edit_breakdown_df(init_df)


def print_whole_df(df, dfname=""):
    with pl.Config(tbl_rows=-1):
        rprint(f"{dfname}: {df}")



