from path_extract.extract.extract import create_csvs_for_project
from path_extract.clmt_pilot.plots import plot_elements_by_category
from path_extract.clmt_pilot.dataframes import edit_breakdown_df
from path_extract.constants import ExperimentInfo
from path_extract.file_utils import read_csv
from path_extract.file_utils import read_json
from path_extract.project_paths import (
    CLMTPath, get_exp_num_from_path
)

import altair as alt


# return None

# TODO think about sort order.. of columns.. 


def read_exp_info(clmt_path: CLMTPath, experiment_num: int):
    data: ExperimentInfo = read_json(clmt_path.get_json(experiment_num))
    return f"{data['project']} -- {data['experiment']}"


def plot_experiment(clmt_path: CLMTPath, experiment_num: int, renderer="browser"):
    name = read_exp_info(clmt_path, experiment_num)

    df = read_csv(clmt_path.get_csv(experiment_num, "Breakdown"))
    df_to_plot = edit_breakdown_df(df)

    # rprint(df3)
    return plot_elements_by_category(df_to_plot, name, renderer)

def plot_all_project_experiments(clmt_path: CLMTPath, renderer="browser"):
    charts = []
    for path in clmt_path.experiment_paths:
        exp_num = get_exp_num_from_path(path)
        chart = plot_experiment(clmt_path, exp_num, renderer)
        charts.append(chart)
    all_chart = alt.hconcat(*charts).resolve_scale(y="shared").resolve_legend()
    return all_chart


# TODO compare overview of project experiments.. -> calc byself? 

if __name__ == "__main__":
    clmt_path = CLMTPath("pier_6")
    # create_csvs_for_project(clmt_path) # TODO run automatically if csvs dont exist.. 
    chart = plot_all_project_experiments(clmt_path)
    chart.show()
