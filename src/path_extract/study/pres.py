from email.mime import base
from path_extract.constants import RendererTypes
from path_extract.study.dataframes import edit_breakdown_df
from path_extract.project_paths import CLMTPath, ProjectNames
from pathlib import Path
from path_extract.constants import HTML, BROWSER, RendererTypes

from path_extract.study.plots import plot_elements, plot_use_categories
import altair as alt
from path_extract.study.plots2 import get_net_emissions
from path_extract.study.waterfall import prep_dataframe, make_waterfall_chart
from rich import print as rprint 


def make_waterfall_figure(project_name: ProjectNames, base_exp_num: int,alt_exp_num: int, renderer: RendererTypes = BROWSER):
    clmt_path = CLMTPath(project_name)
    df = prep_dataframe(project_name, base_exp_num, alt_exp_num)
    chart = make_waterfall_chart(df)
    if renderer == HTML:
        chart.save(
            clmt_path.figures_path / f"exp{base_exp_num}_{alt_exp_num}_waterfall.png", format="png", ppi=200
        )
    else:
        chart.show()




def make_categ_figure(
    project_name: ProjectNames, exp_num: int, renderer: RendererTypes = BROWSER
):
    clmt_path = CLMTPath(project_name)
    init_df = clmt_path.get_csv(exp_num, READ=True)  # TODO change to read or get
    assert not isinstance(init_df, Path)
    df = edit_breakdown_df(init_df)

    c_categories = plot_use_categories(df, "", renderer)
    if renderer == HTML:
        c_categories.save(
            clmt_path.figures_path / f"exp{exp_num}_categ.png", format="png", ppi=200
        )
    else:
        c_categories.show()


def make_project_figures():
    # pier 6
    make_categ_figure("pier_6", 0, HTML)
    make_categ_figure("pier_6", 1, HTML)
    make_waterfall_figure("pier_6", 0, 1, HTML)


    # saginaw
    make_categ_figure("saginaw", 0, HTML)

    # bpcr

    #newton creek 
    make_categ_figure("newtown_creek", 0, HTML)
    make_categ_figure("newtown_creek", 3, HTML)
    make_waterfall_figure("newtown_creek", 0, 1, HTML)
    make_waterfall_figure("newtown_creek", 1, 2, HTML)
    make_waterfall_figure("newtown_creek", 0, 3, HTML)

def percentage_increase(original, new):
    return ((new - original)/ original)*100

    
def get_project_comparisons(project_name: ProjectNames, base_exp_num: int,alt_exp_num: int):
    def get_emit(exp_num:int):
        init_df = clmt_path.get_csv(exp_num, READ=True)  
        assert not isinstance(init_df, Path)
        return get_net_emissions(edit_breakdown_df(init_df))

    clmt_path = CLMTPath(project_name)
    base_emit = get_emit(base_exp_num)
    alt_emit = get_emit(alt_exp_num)
    p_inc = percentage_increase(base_emit, alt_emit)

    rprint(f"Project: {project_name} | Percentage Increase: {round(p_inc)} | Base Emit ({base_exp_num}): {round(base_emit)} | Alt Emit ({round(alt_emit)})\n")




if __name__ == "__main__":
    # pier 6
    get_project_comparisons("pier_6", 0, 1,)
    get_project_comparisons("newtown_creek", 3,1)
    # get_project_comparisons("pier_6", 0, 1,)
