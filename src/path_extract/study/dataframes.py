from path_extract.constants import Headings, Columns
from rich import print as rprint
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


def compare_two_experiments(baseline: pl.DataFrame, alternative: pl.DataFrame):
    # TODO assert that have edited breakdown df.

    # baseline_elements = baseline[Columns.ELEMENT.name].unique()
    # alternative_elements = alternative[Columns.ELEMENT.name].unique()
    # missing_from_baseline = set_difference(baseline_elements, alternative_elements)
    # missing_from_alternative = set_difference(alternative_elements, baseline_elements)
    # rprint(
    #     f"missing from baseline: {missing_from_baseline} missing from alternative: {missing_from_alternative}"
    # )
    # TODO check that the missing are all in the joined df..

    df = (
        baseline.join(
            alternative,
            on=[
                Columns.SECTION.name,
                Columns.TYPE.name,
                Columns.CATEGORY.name,
                Columns.ELEMENT.name,
                Columns.UNIT.name,
                Columns.CUSTOM_CATEGORY.name,
            ],
            how="right",
            suffix="_ALT",
        )
        .with_columns(pl.col(Columns.VALUE.name).fill_null(strategy="zero"))
        .rename(
            {
                Columns.VALUE.name: Columns.BASELINE.name,
                Columns.VALUE_ALT.name: Columns.ALT.name,
            }
        )
    )

    # new_in_baseline = baseline.filter(pl.col(Columns.ELEMENT.name).is_in(missing_from_baseline))
    # with pl.Config(tbl_rows=-1):
    #     rprint(f"baseline elements: {baseline[Columns.ELEMENT.name].unique().sort()}")
    # rprint("new in baseline:", new_in_baseline) # TODO make some modifications to this to make it approp..

    # col_diff =  set_difference(missing_from_alternative + missing_from_baseline, df[Columns.ELEMENT.name].unique().to_list())
    # rprint(f"\ncol diff: {col_diff}")

    # rprint(
    #     f"baseline: {baseline.shape}, alternative: {alternative.shape}, joined: {df.shape}"
    # )

    df2 = (
        df.with_columns(
            VALUE_DIFF=pl.col(Columns.ALT.name) - pl.col(Columns.BASELINE.name)
        )
        .filter(pl.col(Columns.VALUE_DIFF.name) != 0)
        .select(
            [
                pl.col(Columns.CUSTOM_CATEGORY.name),
                pl.col(Columns.CATEGORY.name),
                pl.col(Columns.ELEMENT.name),
                pl.col(Columns.VALUE_DIFF.name),
            ]
        )
        .sort(by=Columns.CUSTOM_CATEGORY.name)
    )

    with pl.Config(tbl_rows=-1):
        rprint(df2)

    return df2


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
