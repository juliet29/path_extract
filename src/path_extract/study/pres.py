from path_extract.study.plots.constants import HTML, clear_fig_path
from path_extract.study.plots.categorical import make_categorical_figure
from path_extract.study.plots.comparison import make_comparison_figure
from path_extract.study.plots.waterfall import make_waterfall_figure
from path_extract.study.plots.pie import make_pier_6_pie
import altair as alt
from path_extract.study.plots.theme import scape

# TODO: make function to reset figure paths..


def pier_6_figs():
    worse_alt = 0
    as_designed = 1
    landscape_scope = 2
    clear_fig_path("pier_6")
    make_categorical_figure("pier_6", worse_alt, HTML)
    make_categorical_figure("pier_6", as_designed, HTML)
    make_categorical_figure("pier_6", landscape_scope, HTML)
    make_waterfall_figure("pier_6", as_designed, worse_alt, HTML)
    make_pier_6_pie(HTML)
    make_comparison_figure("pier_6", as_designed, worse_alt, renderer=HTML)


def saginaw_figs():
    proj_name = "saginaw"
    as_designed = 0
    worse_alt = 1
    clear_fig_path(proj_name)
    make_categorical_figure(proj_name, as_designed, HTML)
    make_categorical_figure(proj_name, worse_alt, HTML)
    make_waterfall_figure(proj_name, as_designed, worse_alt, HTML)
    make_comparison_figure(proj_name, as_designed, worse_alt, renderer=HTML)


def bpcr_figs():
    clear_fig_path("bpcr")
    make_categorical_figure("bpcr", 0, HTML)
    make_categorical_figure("bpcr", 1, HTML)



def newtown_creek_figs():
    clear_fig_path("newtown_creek")
    make_categorical_figure("newtown_creek", 0, HTML)
    make_categorical_figure("newtown_creek", 3, HTML)
    make_waterfall_figure("newtown_creek", 0, 1, HTML)
    make_waterfall_figure("newtown_creek", 0, 2, HTML)
    make_waterfall_figure("newtown_creek", 0, 3, HTML)
    make_comparison_figure("newtown_creek", 0, 3, renderer=HTML)


if __name__ == "__main__":
    alt.theme.enable("scape")
    bpcr_figs()
    
