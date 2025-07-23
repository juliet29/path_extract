from path_extract.constants import ClassNames, Columns
from path_extract.data.dataframes import edit_breakdown_df


import altair as alt
import polars as pl

from path_extract.plots.breakdown.color_category_map import map_use_category_colors_to_elements


def plot_elements(_df: pl.DataFrame, title: str = "", renderer="browser"):
    alt.renderers.enable(renderer)
    df = edit_breakdown_df(_df)
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
