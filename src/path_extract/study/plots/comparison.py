from path_extract.BROWSER import BROWSER
from path_extract.project_paths import CLMTPath, ProjectNames
from path_extract.study.dataframes import edit_breakdown_df, get_net_emissions
import polars as pl
from rich import print as rprint
import altair as alt
from path_extract.study.plots.constants import (
    CARBON_EMIT_LABEL,
    HTML,
    NUMBER_FORMAT,
    POINT_SIZE,
)
from typing import NamedTuple, TypedDict

from path_extract.study.plots.constants import RendererTypes, DEF_DIMENSIONS

EXP_NUM = "num"
EXP_NAME = "name"
VAL = "values"
PCT_CHANGE = "pct_change"

BASELINE = "As Designed"
ALTERNATIVE = "Alternative"


class ExpeMetaData(NamedTuple):
    num: int
    name: str


class MultiExperimentMetaData(TypedDict):
    num: list[int]
    name: list[str]


def create_multi_exp_dict(exps: list[ExpeMetaData]) -> MultiExperimentMetaData:
    return {EXP_NAME: [i.name for i in exps], EXP_NUM: [i.num for i in exps]}


def prep_df(project_name: ProjectNames, exps: list[ExpeMetaData]):
    def get_experiment_emissions(exp_num: int):
        return get_net_emissions(edit_breakdown_df(clmt_path.read_csv(exp_num)))

    clmt_path = CLMTPath(project_name)

    exp_meta_data = create_multi_exp_dict(exps)
    emissions = [get_experiment_emissions(i) for i in exp_meta_data[EXP_NUM]]

    res = dict({VAL: emissions}, **exp_meta_data)  # TODO want value sat the end?
    df = (
        pl.DataFrame(res)
        .with_columns(pl.col(VAL).pct_change().alias(PCT_CHANGE))
        .with_columns(pl.col(PCT_CHANGE).fill_null(strategy="max"))
    )

    rprint(df)
    return df

    # df = pl.DataFrame({EXP_NUMS: experiment_nums, EXP_NAMES: names, VAL: emissions})
    # # TODO option to add names to the experiment numbers? / an additional column..
    # rprint(df)
    # return df


def create_interm_df(df: pl.DataFrame):
    # TODO make schema
    # get first row
    # new values is the average..
    mean = df[VAL].mean()
    d = df.filter(pl.col(EXP_NAME) == BASELINE).with_columns(pl.lit(mean).alias(VAL))
    # rprint(d)

    # rprint(df[VAL].mean())

    return d


def calc_percentage_change(original, new):
    # return ((new - original) / original) * 100
    return new * 10


def plot_comparison(df: pl.DataFrame, renderer=BROWSER):
    alt.renderers.enable(renderer)  # TODO make this a base fx..
    # need to compute where the text should be.. => halfway between the two values..

    chart = alt.Chart(df)

    line = (
        chart.mark_line(point=alt.OverlayMarkDef(size=POINT_SIZE))
        .encode(
            x=alt.X(f"{EXP_NAME}:O").sort(None),
            y=alt.Y(f"{VAL}:Q").axis(format=NUMBER_FORMAT).title(CARBON_EMIT_LABEL),
        )
        .properties(**DEF_DIMENSIONS)
    )

    # amount = alt.datum[PCT_CHANGE]
    # calc_text_amount = (
    #     alt.expr.if_(
    #         amount > 0,
    #         "+",
    #         "",
    #     )
    #     + amount
    # )

    label = chart.encode(
        x=alt.datum(ALTERNATIVE),
        y=alt.Y(f"{VAL}:Q").aggregate("mean"),
        text=alt.Text(f"{PCT_CHANGE}:Q").format(".0%"),
    ).mark_text(
        dx=-20,
        fontSize=30,
    )
    chart = line + label
    chart.show()


if __name__ == "__main__":
    as_designed = ExpeMetaData(1, BASELINE)
    worse_alt = ExpeMetaData(0, ALTERNATIVE)

    df = prep_df("pier_6", [as_designed, worse_alt])
    # create_interm_df(df)
    plot_comparison(df)
    # c = plot_comparison(df)
    # c.show()
