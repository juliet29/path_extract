from path_extract.project_paths import ProjectNames
from path_extract.study.plots.comparison import rprint
from path_extract.study.plots.constants import (
    BROWSER,
    NUMBER_FORMAT,
    RendererTypes,
    get_exp_df, AS_DESIGNED, ALTERNATIVE
)
import polars as pl
import altair as alt
from path_extract.constants import Columns
from path_extract.categories.categories import UseCategories


# add flag to infra elements..
# just doing substructure for now.. seems like other things should be there..

LANDSCAPE_SCOPE = "Landscape Scope"
OTHER_DISCIPLINES = "Other Disciplines"
SCOPE = "Scope"


def prep_df(
    project_name: ProjectNames,
    exp_num: int,
):
    planting_categories = [
        UseCategories.PRESERVED_PLANTING.name,
        UseCategories.NEW_PLANTING.name,
    ]
    df = (
        get_exp_df(project_name, exp_num)
        .filter(~pl.col(Columns.CUSTOM_CATEGORY.name).is_in(planting_categories))
        .with_columns(
            pl.when(
                pl.col(Columns.CUSTOM_CATEGORY.name) == UseCategories.SUBSTRUCTURE.name
            )
            .then(pl.lit(OTHER_DISCIPLINES))
            .otherwise(pl.lit(LANDSCAPE_SCOPE))
            .alias(SCOPE)
        )
        .group_by(SCOPE)
        .agg(pl.col(Columns.VALUE.name).sum())
    )

    return df


def plot_pie(df: pl.DataFrame, title="", renderer: RendererTypes = BROWSER):
    alt.renderers.enable(renderer)
    base = alt.Chart(df, title=title).encode(
        alt.Theta(f"{Columns.VALUE.name}:Q").stack(True),
    )

    inner_radius = 100
    outer_radius = 200
    pie = base.mark_arc(innerRadius=inner_radius, outerRadius=outer_radius).encode(
        color=alt.Color(f"{SCOPE}:N").legend(None)
    )

    dr = 50
    scope_text = (
        base.mark_text(radius=outer_radius + dr, size=20)
        .transform_calculate(
            formattedNum=alt.expr.format(alt.datum[Columns.VALUE.name], NUMBER_FORMAT)
        )
        .transform_calculate(
            txt="split(datum.Scope + ':, ' + datum.formattedNum + ' kg-Co2-eq', ',')" # TODO better if can do w/ altair..
        )
        .encode(text=alt.Text("txt:N"))
    )

    chart = pie + scope_text
    return chart 


def pier_6_pie():
    pie_as_designed = plot_pie(prep_df("pier_6", 1), title=AS_DESIGNED)
    pie_worse_alt = plot_pie(prep_df("pier_6", 0), title=ALTERNATIVE)

    chart =  pie_as_designed | pie_worse_alt

    chart.show()






if __name__ == "__main__":
    # df = prep_df("pier_6", 1)
    # rprint(df)
    # plot_pie(df)

    pier_6_pie()

    # df = prep_df("pier_6", 0)
    # rprint(df)
    # plot_pie(df)
