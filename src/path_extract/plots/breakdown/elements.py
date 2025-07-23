from path_extract.constants import ClassNames, Columns
from path_extract.data.columns import CARBON_EMIT_LABEL
from path_extract.data.dataframes import edit_breakdown_df
from path_extract.project_paths import CLMTPath, ProjectNames
from path_extract.data.dataframes import edit_breakdown_df
from path_extract.plots.helpers.constants import (
    BROWSER,
    HTML,
    LABEL_ANGLE,
    NUMBER_FORMAT,
    RendererTypes,
    get_exp_df,
    save_fig,
)


import altair as alt
import polars as pl

from path_extract.plots.breakdown.color_category_map import (
    map_use_category_colors_to_elements,
)
from path_extract.plots.breakdown.categories import prep_df


def plot_elements(df: pl.DataFrame, title: str = "", renderer="browser"):
    alt.renderers.enable(renderer)
    domains, range_ = map_use_category_colors_to_elements(df)

    chart = (
        alt.Chart(df, title=title)
        .mark_bar()
        .encode(
            x=alt.X(Columns.CUSTOM_CATEGORY.name).title("Category").sort(None),
            y=alt.Y(f"sum({ClassNames.VALUE.name})").title(
                "Equivalent Carbon Emissions [kg-Co2-e]"
            ),
            color=alt.Color(ClassNames.ELEMENT.name)
            .sort(None)
            .scale(domain=domains, range=range_),
            tooltip=[
                ClassNames.ELEMENT.name,
                alt.Tooltip(ClassNames.VALUE.name, format=".2s"),
            ],
        )
        # .facet(column=TableNames.CUSTOM_CATEGORY.name)
    )

    return chart


def make_element_figure(
    project_name: ProjectNames,  # noqa: F821
    exp_num: int,
    renderer: RendererTypes = BROWSER,
):
    clmt_path = CLMTPath(project_name)
    df = prep_df(project_name, exp_num)
    chart = plot_elements(df, renderer=renderer)
    if renderer == HTML:
        fig_name = f"exp{exp_num}_elements.png"
        save_fig(chart, clmt_path, fig_name)
    else:
        chart.show()

    return chart


if __name__ == "__main__":
    alt.theme.enable("scape")
    make_element_figure("newtown_creek", 0)
