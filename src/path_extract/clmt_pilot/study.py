from path_extract.extract.breakdown import read_breakdown
from path_extract.analyze.analyze import clean_df, plot_elements_by_category
from path_extract.constants import ExperimentInfo, ClassNames, TableNames
from path_extract.project_paths import (
    CLMTPath,
    DataTypes,
    CSV,
    HTML,
    get_exp_num,
    BREAKDOWN,
)
from pathlib import Path
from rich import print as rprint
import polars as pl
import json
import altair as alt


def create_csvs_for_breakdown(clmt_path: CLMTPath):
    for exp_dir in clmt_path.experiment_paths:
        exp_num = get_exp_num(exp_dir)
        # rprint(exp_dir.stem)
        # rprint(get_exp_num(exp_dir.stem))

        html = exp_dir / HTML(BREAKDOWN)
        df = read_breakdown(html)
        df.write_csv(clmt_path.get_csv(exp_num, "Breakdown"))

        # TODO read overviews! and check!


def read_csv(path: Path, file_name: str | None = None):
    if file_name:
        _path = path / file_name
    else:
        _path = path
    assert _path.exists(), f"{_path} does not exist!"
    return pl.read_csv(_path)


def read_json(path: Path, file_name: str | None = None):
    if file_name:
        _path = path / file_name
    else:
        _path = path
    assert _path.exists(), f"{_path} does not exist!"
    with open(_path, "r") as f:
        data = json.load(f)
        # print(data)
        return data
    # return None


def read_exp_info(clmt_path: CLMTPath, experiment_num: int):
    data: ExperimentInfo = read_json(clmt_path.get_json(experiment_num))
    return f"{data['project']} -- {data['experiment']}"


def create_expression(v1, v2):
    return (
        pl.when(pl.col(ClassNames.ELEMENT.name) == v1)
        .then(pl.lit(v2))
        .otherwise(ClassNames.CATEGORY.name)
    )


def make_expressions_list(pairs):
    return [create_expression(*i) for i in pairs]


def plot_experiment(clmt_path: CLMTPath, experiment_num: int, renderer="browser"):
    # TODO -> run experiments if dont exist
    name = read_exp_info(clmt_path, experiment_num)
    # rprint(name)
    df = read_csv(clmt_path.get_csv(experiment_num, "Breakdown"))
    df2 = clean_df(df)


	# reorg df -> TODO put in different file.. 
    pairs = [("Asphalt Paving", "Category 2"), ("Stone Steps", "Cat3")]

    df3 = df2.with_columns(
        (
            pl.coalesce(
                pl.when(pl.col(ClassNames.ELEMENT.name) == cond)
                .then(pl.lit(result))
                for cond, result in pairs
            )
        ).alias(TableNames.CUSTOM_CATEGORY.name)
    ).with_columns(
        # pl.when(pl.col(TableNames.CUSTOM_CATEGORY.name).is_null()).then(pl.col(ClassNames.CATEGORY.name))
        pl.col(TableNames.CUSTOM_CATEGORY.name).fill_null(pl.col(ClassNames.CATEGORY.name)))



    # rprint(df3)
    return plot_elements_by_category(df3, name, renderer)


if __name__ == "__main__":
    clmt_path = CLMTPath("newtown_creek")
    create_csvs_for_breakdown(clmt_path)
    # chart = plot_experiment(clmt_path, 0)
    # chart.show()
    



