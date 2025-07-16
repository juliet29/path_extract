from path_extract.clmt_pilot.dataframes import get_emissions_df
from path_extract.extract.breakdown import read_breakdown
from path_extract.paths import SAMPLE_HTML, BASE_PATH
from path_extract.constants import ClassNames, TableNames, Emissions, Headings
import polars as pl
from rich import print as rprint
import altair as alt
from path_extract.vega_colors import VegaColors, vega_colors, get_dict_of_colors
from path_extract.categories.categories import UseCategories


from path_extract.extract.overview import read_overview
from path_extract.project_paths import (
    SAMPLE_CLMT_OVERVIEW_HTML,
    SAMPLE_CLMT_BREAKDOWN_HTML,
)

from path_extract.clmt_pilot.dataframes import edit_breakdown_df


# group by category


def plot_experiment_summary(
    df: pl.DataFrame, title: str, renderer="browser", show=False
):
    # TODO should be making its own dataframe edits..
    alt.renderers.enable(renderer)
    res = df.group_by(ClassNames.TYPE.name).agg(pl.col(ClassNames.VALUE.name).sum())
    # rprint(res)
    df2 = (
        res.transpose(column_names=ClassNames.TYPE.name)
        .select([Headings.EMBODIED_CARBON_EMISSIONS.value, Headings.BIOGENIC.value])
        .rename(
            {
                Headings.EMBODIED_CARBON_EMISSIONS.value: Emissions.EMBODIED.name,
                Headings.BIOGENIC.value: Emissions.BIOGENIC.name,
                # "Operational Emissions": Emissions.OPERATIONAL.name
                # Headings.OPERATIONAL.value: Emissions.OPERATIONAL.name,
            }
        )
        .with_columns(
            (pl.col(Emissions.EMBODIED.name) + pl.col(Emissions.BIOGENIC.name)).alias(
                "TOTAL"
            )
        )
    )
    df3 = df2.unpivot(
        variable_name=TableNames.NAME.name, value_name=ClassNames.VALUE.name
    )

    # rprint(df3)

    chart = (
        alt.Chart(df3, title=title)
        .mark_bar()
        .encode(
            x=alt.X(TableNames.NAME.name).title("Emissions Type"),
            y=alt.Y(ClassNames.VALUE.name).title(
                "Equivalent Carbon Emissions [kg-Co2-e]"
            ),
            color=alt.Color(TableNames.NAME.name).title("Emissions Type"),
        )
    )
    return chart


def plot_elements_by_category(
    df: pl.DataFrame, title="", renderer="browser", show=False
):
    # consider sequestration!
    # TODO should be making its own dataframe edits..
    alt.renderers.enable(renderer)
    chart = (
        alt.Chart(df, title=title)
        .mark_bar()
        .encode(
            x=alt.X(ClassNames.CATEGORY.name).title("Category Names"),
            y=alt.Y(f"sum({ClassNames.VALUE.name})").title(
                "Equivalent Carbon Emissions [kg-Co2-e]"
            ),
            color=alt.Color(ClassNames.ELEMENT.name)
            .sort(None)
            .scale(scheme="tableau20"),
            tooltip=ClassNames.ELEMENT.name,
        )
    )

    return chart


use_category_map: dict[UseCategories, VegaColors] = {
    UseCategories.PRESERVED_PLANTING: "greens",
    UseCategories.DEMO: "browns",  # orange
    UseCategories.PREP: "yellowOrangeBrown",  # orange
    UseCategories.SUBSTRUCTURE: "warmGreys",  # brown
    UseCategories.HARDSCAPE: "greys",  # grey
    UseCategories.NEW_PLANTING: "greens",
    UseCategories.GREEN_INFRA: "teals",
    UseCategories.ACCESSORIES: "darkGold",  # pink
    UseCategories.OPERATIONS: "purples",  # yellow
}


def map_use_category_colors(df: pl.DataFrame):
    # TODO assert that df has correct shape..
    # NOTE: df should be sorted using the Enum values.. -> maybe just add to df so its explicit..
    # scheme = "greens"
    # n_colors = 6
    # colors = make_list_of_colors(scheme)
    # rprint(colors)
    # coloring the 'true' categories.. but also potentially the elements..
    domains = df[ClassNames.CATEGORY.name].unique(maintain_order=True).to_list()
    # rprint(domains)
    # tracker: dict[VegaColors, int] = {}
    range_ = []

    dict_of_colors = get_dict_of_colors()

    category_groups = df.group_by(
        [ClassNames.CATEGORY.name, TableNames.CUSTOM_CATEGORY.name],
        maintain_order=True,
    ).agg()

    for row in category_groups.iter_rows(named=True):
        # category_name = row[ClassNames.CATEGORY.name]
        use_category_name = row[TableNames.CUSTOM_CATEGORY.name]
        color_scheme = use_category_map[UseCategories[use_category_name]]
        curr_color = next(dict_of_colors[color_scheme])
        # rprint(color_scheme, use_category_name)
        # if color_scheme not in tracker.keys():
        #     tracker[color_scheme] = 0
        # else:
        #     tracker[color_scheme] += 1

        range_.append(curr_color)

        # rprint(use_category_name, category_name, color_scheme, curr_color)

    # assign use categories to a range of colors -> ideally pre-existing list
    # for each element in df, pick a color from this family of shades..and cycle over//
    # keep a pointer to each item in the list so that have max diversity//
    return domains, range_


def plot_use_categories(_df: pl.DataFrame, title: str, renderer="browser"):
    alt.renderers.enable(renderer)
    df = edit_breakdown_df(_df)

    # group = df.group_by(
    #     [ClassNames.CATEGORY.name, TableNames.CUSTOM_CATEGORY.name],
    #     maintain_order=True,
    # ).agg().iter
    # rprint(group)
    domains, range_ = map_use_category_colors(df)
    # rprint([(i, j) for i, j in zip(domains, range_)])
    # rprint(df)
    # rprint(list(df[ClassNames.CATEGORY.name].unique(maintain_order=True)))
    chart = (
        alt.Chart(df, title=title)
        .mark_bar()
        .encode(
            x=alt.X(TableNames.CUSTOM_CATEGORY.name).title("Use Categories").sort(None),
            y=alt.Y(f"sum({ClassNames.VALUE.name})").title(
                "Equivalent Carbon Emissions [kg-Co2-e]"
            ),
            color=alt.Color(ClassNames.CATEGORY.name)
            .sort(None)
            .scale(domain=domains, range=range_),
            tooltip=ClassNames.CATEGORY.name,
        )
    )

    return chart


def plot_use_categories_and_elements(_df: pl.DataFrame, title: str, renderer="browser"):
    df = edit_breakdown_df(_df)
    # rprint(df)
    alt.renderers.enable(renderer)

    chart = (
        alt.Chart(df, title=title)
        .mark_bar()
        .encode(
            x=alt.X(ClassNames.CATEGORY.name).title("Category").sort(None),
            y=alt.Y(f"sum({ClassNames.VALUE.name})").title(
                "Equivalent Carbon Emissions [kg-Co2-e]"
            ),
            color=alt.Color(ClassNames.ELEMENT.name),
        )
        .facet(column=TableNames.CUSTOM_CATEGORY.name)
    )

    return chart


if __name__ == "__main__":
    df = read_breakdown(SAMPLE_CLMT_BREAKDOWN_HTML)
    chart = plot_use_categories(df, "example")
    chart.show()
    # map_use_category_colors(edit_breakdown_df(df))
