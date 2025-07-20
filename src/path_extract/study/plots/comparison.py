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
from prefixed import Float

from path_extract.study.plots.constants import RendererTypes, DEF_DIMENSIONS

EXP_NUM = "num"
EXP_NAME = "name"
VAL = "value"
FORMATTED_VALUE = "formatted_val"
PCT_CHANGE = "pct_change"

BASELINE = "As Designed"
ALTERNATIVE = "Alternative"
EXPERIMENT_NAMES = "Experiment Names"


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
        .with_columns(
            pl.col(VAL).map_elements(lambda x: f"{Float(x):.2h}").alias(FORMATTED_VALUE)
        )
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

    font_size = 20
    font_size_plus = font_size + 10

    chart = alt.Chart(df)

    line = (
        chart.mark_line(point=alt.OverlayMarkDef(size=POINT_SIZE))
        .encode(
            x=alt.X(f"{EXP_NAME}:O").sort(None).axis(labels=False).title(EXPERIMENT_NAMES),
            y=alt.Y(f"{VAL}:Q").axis(format=NUMBER_FORMAT).title(CARBON_EMIT_LABEL),
        )
        .properties(**DEF_DIMENSIONS)
    )

    prc_change = chart.encode(
        x=alt.datum(ALTERNATIVE),
        y=alt.Y(f"{VAL}:Q").aggregate("mean"),
        text=alt.Text(f"{PCT_CHANGE}:Q").format("+,.0%"),
    ).mark_text(
        dx=-20,
        fontSize=font_size_plus,
    )

    init_dx = -0
    init_dy = 20
    text_align = "left"

    label = (
        line.transform_calculate(
            label_name="datum.name + ': '+ datum.formatted_val + ' kg-CO2-eq'"
        )
        .encode(text=alt.Text("label_name:N"))
        .mark_text(
            lineBreak=r"\n",
            align=text_align,
            dx=init_dx,
            dy=init_dy,
            fontSize=font_size,
        )
    )

    chart = line  + prc_change  + label

    chart.show()


if __name__ == "__main__":
    as_designed = ExpeMetaData(1, BASELINE)
    better_alt = ExpeMetaData(0, ALTERNATIVE)
    df = prep_df("pier_6", [as_designed, better_alt])
    plot_comparison(df)



    # as_designed = ExpeMetaData(0, BASELINE)
    # better_alt = ExpeMetaData(2, ALTERNATIVE)
    # df = prep_df("newtown_creek", [as_designed, better_alt])


    

