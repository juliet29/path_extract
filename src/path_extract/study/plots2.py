from path_extract.project_paths import CLMTPath, ProjectNames
from path_extract.study.dataframes import edit_breakdown_df, get_net_emissions
import polars as pl
from rich import print as rprint
import altair as alt

EXP = "ExpNum"
VAL = "EmitVal"
BROWSER = "browser"


def prep_df(project_name: ProjectNames):
    # TODO make possible to specify the desired exp_nums..
    # TODO get the names also..
    def get_exp_emissions(exp_num):
        return get_net_emissions(
            edit_breakdown_df(clmt_path.get_csv(exp_num, READ=True))
        )

    clmt_path = CLMTPath(project_name)
    exp_nums = clmt_path.get_all_experiment_nums
    emits = [(i, get_exp_emissions(i)) for i in exp_nums]
    res = pl.DataFrame({EXP: [i[0] for i in emits], VAL: [i[1] for i in emits]}).sort(
        by=VAL, descending=True
    )
    rprint(res)
    return res


def plot_comparison(df: pl.DataFrame, renderer=BROWSER):
    alt.renderers.enable(renderer)  # TODO make this a base fx..
    chart = (
        alt.Chart(df)
        .mark_point()
        .encode(x=f"{EXP}:O", y=f"{VAL}:Q")
        .properties(width=180, height=180)
    )
    return chart


if __name__ == "__main__":
    df = prep_df("pier_6")
    c = plot_comparison(df)
    c.show()
