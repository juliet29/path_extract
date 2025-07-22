import altair as alt
import polars as pl

from path_extract.categories.categories import UseCategories
from path_extract.constants import Columns
from path_extract.project_paths import CLMTPath, ProjectNames
from path_extract.study.plots.constants import BROWSER, RendererTypes, HTML, save_fig
from path_extract.study.plots.data_waterfall import compare_two_experiments

# from path_extract.study.plots.theme import scape
from rich import print as rprint


def prep_df(
    project_name: ProjectNames,
    base_exp_num: int,
    alt_exp_num: int,
    filter_categ: UseCategories = UseCategories.HARDSCAPE,
):
    df = compare_two_experiments(project_name, base_exp_num, alt_exp_num).filter(
        pl.col(Columns.CUSTOM_CATEGORY.name) == filter_categ.name
    )
    rprint(df)

    return df


def plot_stack_compare(df: pl.DataFrame):
    chart = (
        alt.Chart(df)
        .transform_fold(
            [Columns.VALUE.name, Columns.VALUE_ALT.name], as_=["key", "data"]
        )
        # creates a 'key' colum with VALUE / VALUE ALT as rows, and stacks the actual values -> creates a long datafra,e..
        .mark_bar()
        .encode(
            x="key:N",
            y="sum(data):Q",
            color="key:N",
            column=f"{Columns.ELEMENT.name}:N",
        )
    ).properties(width=80)

    return chart


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
        fig_name = f"exp{base_exp_num}_{alt_exp_num}_waterfall.png"
        save_fig(chart, clmt_path, fig_name)
    else:
        chart.show()
    return chart


if __name__ == "__main__":
    # alt.theme.enable("scape")
    c = make_stack_compare_figure("newtown_creek", 0, 1)
