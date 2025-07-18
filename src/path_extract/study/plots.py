from path_extract.study.colors import (
    map_use_category_colors,
    map_use_category_colors_to_elements,
)
from path_extract.extract.breakdown import read_breakdown
from path_extract.constants import ClassNames, Columns, Emissions, Headings, LABEL_ANGLE, NUMBER_FORMAT
import polars as pl
import altair as alt


from path_extract.project_paths import (
    SAMPLE_CLMT_BREAKDOWN_HTML,
)

from path_extract.study.dataframes import edit_breakdown_df


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
    df3 = df2.unpivot(variable_name=Columns.NAME.name, value_name=ClassNames.VALUE.name)

    # rprint(df3)

    chart = (
        alt.Chart(df3, title=title)
        .mark_bar()
        .encode(
            x=alt.X(Columns.NAME.name).title("Emissions Type"),
            y=alt.Y(ClassNames.VALUE.name).title(
                "Equivalent Carbon Emissions [kg-Co2-e]"
            ),
            color=alt.Color(Columns.NAME.name).title("Emissions Type"),
            tooltip=[
                Columns.NAME.name,
                alt.Tooltip(ClassNames.VALUE.name, format=".2s"),
            ],
        )
    )
    return chart


# TODO move this elsewhere..
def plot_use_categories(_df: pl.DataFrame, title: str, renderer="browser"):
    alt.renderers.enable(renderer)
    df = edit_breakdown_df(_df)

    domains, range_ = map_use_category_colors(df)
    chart = (
        alt.Chart(df, title=title)
        .mark_bar()
        .encode(
            x=alt.X(Columns.CUSTOM_CATEGORY.name).title("Use Categories").sort(None),
            y=alt.Y(f"sum({ClassNames.VALUE.name})", axis=alt.Axis(format=NUMBER_FORMAT)).title(
                "Equivalent Carbon Emissions [kg-Co2-e]"
            ),
            color=alt.Color(ClassNames.CATEGORY.name)
            .sort(None)
            .scale(domain=domains, range=range_),
            tooltip=[
                ClassNames.CATEGORY.name,
                alt.Tooltip(f"sum({ClassNames.VALUE.name})", format=".2s"),
            ],
        ).properties(width=250, height=220).configure_axisX(labelAngle=LABEL_ANGLE)
    )

    return chart


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


if __name__ == "__main__":
    df = read_breakdown(SAMPLE_CLMT_BREAKDOWN_HTML)
    chart = plot_elements(df, "example")
    chart.show()
    # map_use_category_colors(edit_breakdown_df(df))
