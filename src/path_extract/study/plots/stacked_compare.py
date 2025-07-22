from typing import Callable
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
from altair_transform import extract_data


def prep_df(
    project_name: ProjectNames,
    base_exp_num: int,
    alt_exp_num: int,
    filter_categ: UseCategories = None,
):
    df = compare_two_experiments(project_name, base_exp_num, alt_exp_num)

    rprint(df)

    rprint(df.sum())
    if filter_categ:
        d = df.filter(pl.col(Columns.CUSTOM_CATEGORY.name) == filter_categ.name)
        rprint(d)
        rprint(d.sum())
        return d

    return df


CHART_GRAPH_FX = Callable[[alt.Chart], alt.LayerChart]


def stacked_graph(base: alt.Chart) -> alt.LayerChart:
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


def simplifed_graph(base: alt.Chart) -> alt.LayerChart:
    post_base = base.transform_calculate(
        IsEmit=alt.expr.if_(alt.datum.data > 0, True, False)
    )

    bar = post_base.mark_bar().encode(
        x=alt.X("AxisName:N").sort().title("Scenarios"),
        y=alt.Y("sum(data):Q").axis(format=NUMBER_FORMAT).title(CARBON_EMIT_LABEL),
        color=alt.Color("IsEmit:N").legend(labelLimit=500).sort(),
    )

    text = (
        post_base.transform_aggregate(Total="sum(data)", groupby=["IsEmit", "AxisName"])
        .encode(
            text=alt.Text("Total:Q").format(NUMBER_FORMAT),
            x=alt.X("AxisName:N").sort(),
            y=alt.Y("Total:Q"),
        )
        .mark_text(dy=10)
    )

    contents = (
        post_base.transform_aggregate(
            Contents="values(ELEMENT)", groupby=["IsEmit", "AxisName"]
        )
        .encode(
            text=alt.Text("Contents:N"),
            x=alt.X("AxisName:N").sort(),
            y=alt.Y("Total:Q"),
        )
        .mark_text(dy=-50, dx=400)
    )
    # rprint(extract_data(contents))

    return (bar + text + contents).configure_axisX(labelAngle=0)


def plot_stack_compare(df: pl.DataFrame, chart_fx: CHART_GRAPH_FX = stacked_graph):
    base = (
        alt.Chart(df).transform_fold(
            # creates a 'key' colum with VALUE / VALUE ALT as rows, and stacks the actual values -> creates a long datafra,e..
            [Columns.VALUE.name, Columns.VALUE_ALT.name],
            as_=["key", "data"],
        )
    ).transform_calculate(
        AxisName=alt.expr.if_(
            alt.datum.key == Columns.VALUE.name, "As Designed", "Alternative"
        )
    )

    return chart_fx(base)


def make_stack_compare_figure(
    project_name: ProjectNames,
    base_exp_num: int,
    alt_exp_num: int,
    renderer: RendererTypes = BROWSER,
    filter_categ: UseCategories = UseCategories.HARDSCAPE,
    chart_fx: CHART_GRAPH_FX = stacked_graph,
):
    alt.renderers.enable(renderer)
    clmt_path = CLMTPath(project_name)
    df = prep_df(project_name, base_exp_num, alt_exp_num, filter_categ)
    chart = plot_stack_compare(df, chart_fx)
    if renderer == HTML:
        fig_name = f"exp{base_exp_num}_{alt_exp_num}_stack_compare.png"
        save_fig(chart, clmt_path, fig_name)
    else:
        chart.show()
    return chart


if __name__ == "__main__":
    # alt.theme.enable("scape")
    c = make_stack_compare_figure(
        "bpcr",
        2,
        3,
        renderer=BROWSER,
        filter_categ=None,
        chart_fx=simplifed_graph,
    )

    # rprint("Hello!")

    # c = make_stack_compare_figure(
    #     "newtown_creek",
    #     0,
    #     2,
    #     renderer=HTML,
    #     filter_categ=UseCategories.HARDSCAPE,
    #     # chart_fx=simplifed_graph,
    # )
