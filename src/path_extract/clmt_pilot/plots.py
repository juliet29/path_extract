from path_extract.clmt_pilot.dataframes import get_emissions_df
from path_extract.extract.breakdown import read_breakdown
from path_extract.paths import SAMPLE_HTML, BASE_PATH
from path_extract.constants import ClassNames, TableNames
import polars as pl
from rich import print as rprint
import altair as alt


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
            color=alt.Color(ClassNames.ELEMENT.name).legend(None),
            tooltip=ClassNames.ELEMENT.name,
        )
    )

    if show:
        chart.show()

    return chart


if __name__ == "__main__":
    # alt.renderers.enable("browser")
    # uncomment below
    df = read_breakdown(SAMPLE_HTML)
    df2 = get_emissions_df(df)
    plot_elements_by_category(df2)

    res = df2.group_by(ClassNames.CATEGORY.name, maintain_order=True).agg(
        ClassNames.ELEMENT.name
    )
    rprint(res)

    df2.write_csv(file=BASE_PATH / "test.csv")
