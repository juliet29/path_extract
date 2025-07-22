import altair as alt
import polars as pl

from path_extract.categories.categories import UseCategories
from path_extract.constants import Columns
from path_extract.project_paths import CLMTPath, ProjectNames
from path_extract.study.plots.constants import (
    BROWSER,
    CARBON_EMIT_LABEL,
    NUMBER_FORMAT,
    RendererTypes,
    HTML,
    save_fig,
)
from path_extract.study.plots.data_waterfall import compare_two_experiments

# from path_extract.study.plots.theme import scape
from rich import print as rprint


def prep_df(
    project_name: ProjectNames,
    base_exp_num: int,
    alt_exp_num: int,
    filter_categ: UseCategories = None,
):
    df = compare_two_experiments(project_name, base_exp_num, alt_exp_num)

    if filter_categ:
        return df.filter(pl.col(Columns.CUSTOM_CATEGORY.name) == filter_categ.name)
    # rprint(df)

    return df


def plot_stack_compare(df: pl.DataFrame):
    base = (
        alt.Chart(df).transform_fold(
            [Columns.VALUE.name, Columns.VALUE_ALT.name], as_=["key", "data"]
        )
        # creates a 'key' colum with VALUE / VALUE ALT as rows, and stacks the actual values -> creates a long datafra,e..
    ).transform_calculate(
        AxisName=alt.expr.if_(
            alt.datum.key == Columns.VALUE.name, "As Designed", "Alternative"
        )
    )

    bar = base.mark_bar().encode(
        x=alt.X("AxisName:N").sort().title("Scenarios"),
        y=alt.Y("sum(data):Q").axis(format=NUMBER_FORMAT).title(CARBON_EMIT_LABEL),
        color=alt.Color(f"{Columns.ELEMENT.name}:N").legend(labelLimit=500),
    )

    text = (
        base.transform_aggregate(total="sum(data)", groupby=["AxisName"])
        .encode(
            text=alt.Text("total:Q").format(NUMBER_FORMAT),
            x=alt.X("AxisName:N").sort(),
            y="total:Q",
        )
        .mark_text(dy=-10)
    )

    return (bar + text).configure_axisX(labelAngle=0)


def make_stack_compare_figure(
    project_name: ProjectNames,
    base_exp_num: int,
    alt_exp_num: int,
    renderer: RendererTypes = BROWSER,
    filter_categ: UseCategories = UseCategories.HARDSCAPE,
):
    alt.renderers.enable(renderer)
    clmt_path = CLMTPath(project_name)
    df = prep_df(project_name, base_exp_num, alt_exp_num, filter_categ)
    chart = plot_stack_compare(df)
    if renderer == HTML:
        fig_name = f"exp{base_exp_num}_{alt_exp_num}_stack_compare.png"
        save_fig(chart, clmt_path, fig_name)
    else:
        chart.show()
    return chart


if __name__ == "__main__":
    # alt.theme.enable("scape")
    c = make_stack_compare_figure(
        "newtown_creek", 0, 1, renderer=HTML, filter_categ=UseCategories.HARDSCAPE
    )
