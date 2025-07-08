from path_extract.clmt_pilot.dataframes import get_emissions_df
from path_extract.extract.breakdown import read_breakdown
from path_extract.paths import SAMPLE_HTML, BASE_PATH
from path_extract.constants import ClassNames, TableNames, Emissions, Headings
import polars as pl
from rich import print as rprint
import altair as alt

from path_extract.extract.overview import read_overview
from path_extract.project_paths import SAMPLE_CLMT_OVERVIEW_HTML, SAMPLE_CLMT_BREAKDOWN_HTML

from path_extract.clmt_pilot.dataframes import edit_breakdown_df


# group by category


def plot_elements_by_category(
    df: pl.DataFrame, title="", renderer="browser", show=False
):
    alt.renderers.enable(renderer)
    chart = (
        alt.Chart(df, title=title)
        .mark_bar()
        .encode(
            x=alt.X(TableNames.CUSTOM_CATEGORY.name).title("Category Names"),
            y=alt.Y(f"sum({ClassNames.VALUE.name})").title(
                "Equivalent Carbon Emissions [kg-Co2-e]"
            ),
            color=alt.Color(ClassNames.ELEMENT.name),
            tooltip=ClassNames.ELEMENT.name,
        )
    )

    if show:
        chart.show()

    return chart


def plot_experiment_summary(df:pl.DataFrame, title: str,  renderer="browser", show=False
):
    alt.renderers.enable(renderer)
    # df = edit_breakdown_df(_df)

    # rprint(df)
    res = df.group_by(ClassNames.TYPE.name).agg(pl.col(ClassNames.VALUE.name).sum())
    # rprint(res)
    df2 = res.transpose(column_names=ClassNames.TYPE.name).rename({
        Headings.EMBODIED_CARBON_EMISSIONS.value: Emissions.EMBODIED.name,
        Headings.BIOGENIC.value: Emissions.BIOGENIC.name,
        # Headings.OPERATIONAL.value: Emissions.OPERATIONAL.name,
    }).with_columns((pl.col(Emissions.EMBODIED.name) + pl.col(Emissions.BIOGENIC.name)).alias("Total"))
    df3 = df2.unpivot(variable_name=TableNames.NAME.name, value_name=ClassNames.VALUE.name)

    # rprint(df3)

    chart = alt.Chart(df3, title=title).mark_bar().encode(
        x=alt.X(TableNames.NAME.name).title("Emissions Type"),
        y=alt.Y(ClassNames.VALUE.name).title("Equivalent Carbon Emissions [kg-Co2-e]"),
        color=alt.Color(TableNames.NAME.name).title("Emissions Type")
    )
    return chart
    # chart.show()
    # data = {
    #     Emissions.EMBODIED.name: res[He]
    # }
    # rprint(res.unpivot(on=ClassNames.VALUE.name, index=ClassNames.TYPE.name))
    # group by type.. 
    # df.filter((pl.col(TableNames.NAME.name) == Emissions.EMBODIED.name) | (pl.col(TableNames.NAME.name) == Emissions.EMBODIED.name) )


if __name__ == "__main__":
    df = read_breakdown(SAMPLE_CLMT_BREAKDOWN_HTML)
    plot_experiment_summary(df, "sample")
    # alt.renderers.enable("browser")
    # uncomment below
    # df = read_breakdown(SAMPLE_HTML)
    # df2 = get_emissions_df(df)
    # plot_elements_by_category(df2)

    # res = df2.group_by(ClassNames.CATEGORY.name, maintain_order=True).agg(
    #     ClassNames.ELEMENT.name
    # )
    # rprint(res)

    # df2.write_csv(file=BASE_PATH / "test.csv")
