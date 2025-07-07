from path_extract.clmt_pilot.dataframes import get_emissions_df
from path_extract.extract.extract import create_csvs_for_project
from path_extract.clmt_pilot.plots import plot_elements_by_category
from path_extract.constants import ExperimentInfo, ClassNames, TableNames
from path_extract.file_utils import read_csv
from path_extract.file_utils import read_json
from path_extract.project_paths import (
    CLMTPath,
    DataTypes,
    CSV,
)

import polars as pl
import altair as alt


# return None


def read_exp_info(clmt_path: CLMTPath, experiment_num: int):
    data: ExperimentInfo = read_json(clmt_path.get_json(experiment_num))
    return f"{data['project']} -- {data['experiment']}"


# def create_expression(v1, v2):
#     return (
#         pl.when(pl.col(ClassNames.ELEMENT.name) == v1)
#         .then(pl.lit(v2))
#         .otherwise(ClassNames.CATEGORY.name)
#     )


# def make_expressions_list(pairs):
#     return [create_expression(*i) for i in pairs]


def plot_experiment(clmt_path: CLMTPath, experiment_num: int, renderer="browser"):
    # TODO -> run experiments if dont exist
    name = read_exp_info(clmt_path, experiment_num)
    # rprint(name)
    df = read_csv(clmt_path.get_csv(experiment_num, "Breakdown"))
    df2 = get_emissions_df(df)

    # reorg df -> TODO put in different file..
    pairs = [("Asphalt Paving", "Category 2"), ("Stone Steps", "Cat3")]

    df3 = df2.with_columns(
        (
            pl.coalesce(
                pl.when(pl.col(ClassNames.ELEMENT.name) == cond).then(pl.lit(result))
                for cond, result in pairs
            )
        ).alias(TableNames.CUSTOM_CATEGORY.name)
    ).with_columns(
        # pl.when(pl.col(TableNames.CUSTOM_CATEGORY.name).is_null()).then(pl.col(ClassNames.CATEGORY.name))
        pl.col(TableNames.CUSTOM_CATEGORY.name).fill_null(
            pl.col(ClassNames.CATEGORY.name)
        )
    )

    # rprint(df3)
    return plot_elements_by_category(df3, name, renderer)


if __name__ == "__main__":
    clmt_path = CLMTPath("newtown_creek")
    create_csvs_for_project(clmt_path)
    # chart = plot_experiment(clmt_path, 0)
    # chart.show()
