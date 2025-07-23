from path_extract.data.categories.use_categories import UseCategories
from path_extract.plots.breakdown.categories import make_categorical_figure
from path_extract.plots.breakdown.elements import make_element_figure
from path_extract.plots.helpers.constants import HTML, clear_fig_path
from path_extract.plots.dot_compare import make_comparison_figure
from path_extract.plots.stacked_compare import make_stack_compare_figure
from path_extract.plots.waterfall import make_waterfall_figure
from path_extract.plots.pie import make_pier_6_pie
import altair as alt
from path_extract.plots.helpers.theme import scape

# TODO: make function to reset figure paths..


def pier_6_figs():
    worse_alt = 0
    as_designed = 1
    landscape_scope = 2
    categ1 = UseCategories.SUBSTRUCTURE
    categ2 = UseCategories.HARDSCAPE
    proj_name = "pier_6"
    clear_fig_path(proj_name)
    make_categorical_figure(proj_name, worse_alt, HTML)
    make_categorical_figure(proj_name, as_designed, HTML)
    make_categorical_figure(proj_name, landscape_scope, HTML)

    make_stack_compare_figure(
        proj_name, as_designed, worse_alt, renderer=HTML, filter_categ=categ1
    )

    make_pier_6_pie(HTML)

    make_comparison_figure(proj_name, as_designed, worse_alt, renderer=HTML)


def saginaw_figs():
    proj_name = "saginaw"
    as_designed = 0
    worse_alt = 1
    categ1 = None  # UseCategories.DEMO

    clear_fig_path(proj_name)
    make_categorical_figure(proj_name, as_designed, HTML)
    make_categorical_figure(proj_name, worse_alt, HTML)

    make_stack_compare_figure(
        proj_name, as_designed, worse_alt, HTML, filter_categ=categ1
    )

    make_comparison_figure(proj_name, as_designed, worse_alt, renderer=HTML)


def bpcr_figs():
    proj_name = "bpcr"
    clear_fig_path("bpcr")
    make_categorical_figure("bpcr", 0, HTML)
    make_categorical_figure("bpcr", 1, HTML)
    make_stack_compare_figure(proj_name, 2, 3, HTML, filter_categ=None)
    make_waterfall_figure(proj_name, 2, 3, HTML)


def newtown_creek_figs():
    as_designed = 0
    area = 1
    depth = 2
    both = 3
    categ = UseCategories.HARDSCAPE
    clear_fig_path("newtown_creek")

    make_categorical_figure("newtown_creek", as_designed, HTML)
    make_categorical_figure("newtown_creek", both, HTML)

    make_stack_compare_figure(
        "newtown_creek", as_designed, area, renderer=HTML, filter_categ=categ
    )
    make_stack_compare_figure(
        "newtown_creek", as_designed, depth, renderer=HTML, filter_categ=categ
    )
    make_stack_compare_figure(
        "newtown_creek", as_designed, both, renderer=HTML, filter_categ=categ
    )
    make_comparison_figure("newtown_creek", as_designed, both, renderer=HTML)
    make_element_figure("newtown_creek", 0, HTML)


if __name__ == "__main__":
    alt.theme.enable("scape")
    # pier_6_figs()
    # bpcr_figs()
    newtown_creek_figs()
