from path_extract.study.plots.constants import HTML, clear_fig_path
from path_extract.study.plots.categorical import make_categorical_figure
from path_extract.study.plots.comparison import make_comparison_figure
from path_extract.study.plots.waterfall import make_waterfall_figure
from path_extract.study.plots.pie import make_pier_6_pie
import altair as alt
from path_extract.study.plots.theme import scape

# TODO: make function to reset figure paths..


def pier_6_figs():
    clear_fig_path("pier_6")
    make_categorical_figure("pier_6", 0, HTML)
    make_categorical_figure("pier_6", 1, HTML)
    make_waterfall_figure("pier_6", 1, 0, HTML)
    make_pier_6_pie(HTML)
    make_comparison_figure("pier_6", 1, 0, renderer=HTML)


def saginaw_figs():
    clear_fig_path("saginaw")
    make_categorical_figure("saginaw", 0, HTML)


def bpcr_figs():
    pass


def newtown_creek_figs():
    clear_fig_path("newtown_creek")
    make_categorical_figure("newtown_creek", 0, HTML)
    make_categorical_figure("newtown_creek", 3, HTML)
    # make_waterfall_figure("newtown_creek", 0, 1, HTML)
    # make_waterfall_figure("newtown_creek", 1, 2, HTML)
    make_waterfall_figure("newtown_creek", 0, 3, HTML)
    make_comparison_figure("newtown_creek", 0, 3, renderer=HTML)


if __name__ == "__main__":
    alt.theme.enable("scape")
    pier_6_figs()
    
