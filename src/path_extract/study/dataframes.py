from path_extract.constants import Headings, Columns
from path_extract.file_utils import read_csv
from path_extract.project_paths import CLMTPath
import polars as pl
from path_extract.study.plots.revised_categories import create_pairs
from path_extract.categories.assign import assign_dict, check_assign_dict
from path_extract.categories.categories import UseCategories


def get_emissions_df(df: pl.DataFrame):
    d = df.filter(pl.col(Columns.VALUE.name) != 0).filter(
        pl.col(Columns.SECTION.name) == Headings.CARBON_IMPACT.value
    )
    # rprint(d)

    # NOTE: sometimes
    # there are duplicate elements in pathfinder, do a groupby early on
    grouped = d.group_by(pl.col(Columns.ELEMENT.name)).agg(
        pl.col(Columns.VALUE.name).sum(),
    )
    d2 = (
        d.join(
            grouped,
            on=[Columns.ELEMENT.name],
            suffix="_ALT",
        )
        .unique(subset=[Columns.ELEMENT.name, Columns.VALUE_ALT.name])
        .drop(Columns.VALUE.name)
        .rename({Columns.VALUE_ALT.name: Columns.VALUE.name})
    )

    # with pl.Config(tbl_rows=-1):
    #     rprint(df[TableNames.ELEMENT.name].unique().sort())
    return d2


def include_use_categories(df: pl.DataFrame):
    check_assign_dict()
    pairs = create_pairs(assign_dict)
    # rprint(pairs)
    d = (
        df.with_columns(
            (
                pl.coalesce(
                    # this syntax should allow to fail smoothly if element is NOT in dataframe..
                    pl.when(pl.col(Columns.CATEGORY.name) == cond).then(
                        pl.lit(result.name)
                    )
                    for cond, result in pairs
                )
            ).alias(Columns.CUSTOM_CATEGORY.name)
        )
        .with_columns(
            pl.col(Columns.CUSTOM_CATEGORY.name).fill_null(
                pl.col(Columns.CATEGORY.name)
            )
        )
        .sort(
            by=pl.col(Columns.CUSTOM_CATEGORY.name).map_elements(
                lambda x: UseCategories[x].value[0], return_dtype=pl.Int64
            )
        )
    )
    return d


def edit_breakdown_df(df: pl.DataFrame):
    df1 = get_emissions_df(df)
    # df2 = reorganize_element_categories(df1)
    df2 = include_use_categories(df1)
    return df2


def get_net_emissions(df: pl.DataFrame):
    # TODO assert that have edited breakdown df..
    # TODO write tests here!
    # with pl.Config(tbl_rows=-1):
    #     rprint(df)
    res = df[Columns.VALUE].sum()
    return res


if __name__ == "__main__":
    # TODO make test -> typical use case
    # df = read_csv(SAMPLE_CLMT_PATH.get_csv(0))
    # d = edit_breakdown_df(df)
    # rprint(d)

    # compare two experiments
    clmt_path = CLMTPath("pier_6")
    baseline = edit_breakdown_df(clmt_path.read_csv(0))
    alternative = edit_breakdown_df(clmt_path.read_csv(1))
    get_net_emissions(baseline)
    # compare_two_experiments(baseline, alternative)
