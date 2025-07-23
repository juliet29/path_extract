from path_extract.constants import ClassNames, Columns
from path_extract.plots.breakdown.color_category_map import map_use_category_colors
from path_extract.project_paths import CLMTPath, ProjectNames
from path_extract.data.dataframes import edit_breakdown_df
from path_extract.plots.helpers.constants import (
    BROWSER,
    CARBON_EMIT_LABEL,
    HTML,
    LABEL_ANGLE,
    NUMBER_FORMAT,
    RendererTypes,
    get_exp_df,
    save_fig,
)
from rich import print as rprint
from path_extract.plots.helpers.theme import scape


import altair as alt
import polars as pl


def prep_df(
    project_name: ProjectNames,
    exp_num: int,
):
    df = get_exp_df(project_name, exp_num).with_columns(
        pl.col(Columns.CUSTOM_CATEGORY.name)
        .str.replace_all("_", " ")
        .str.to_titlecase()
        .alias(Columns.CUSTOM_CATGEORY_LABEL.name)
    )
    # rprint(df)

    return df


def plot_use_categories(df: pl.DataFrame, title: str = "", renderer="browser"):
    alt.renderers.enable(renderer)

    domains, range_ = map_use_category_colors(df)
    chart = (
        alt.Chart(df, title=title)
        .mark_bar()
        .encode(
            x=alt.X(Columns.CUSTOM_CATGEORY_LABEL.name)
            .title("Use Categories")
            .sort(None),
            y=alt.Y(
                f"sum({ClassNames.VALUE.name})", axis=alt.Axis(format=NUMBER_FORMAT)
            ).title(CARBON_EMIT_LABEL),
            color=alt.Color(ClassNames.CATEGORY.name)
            .sort(None)
            .scale(domain=domains, range=range_),
            tooltip=[
                ClassNames.CATEGORY.name,
                alt.Tooltip(f"sum({ClassNames.VALUE.name})", format=".2s"),
            ],
        )
        .configure_axisX(labelAngle=LABEL_ANGLE)
    )

    return chart


def make_categorical_figure(
    project_name: ProjectNames,  # noqa: F821
    exp_num: int,
    renderer: RendererTypes = BROWSER,
):
    clmt_path = CLMTPath(project_name)
    df = prep_df(project_name, exp_num)
    chart = plot_use_categories(df, renderer=renderer)
    if renderer == HTML:
        fig_name = f"exp{exp_num}_categories.png"
        save_fig(chart, clmt_path, fig_name)
    else:
        chart.show()

    return chart


if __name__ == "__main__":
    alt.theme.enable("scape")
    make_categorical_figure("newtown_creek", 0)
