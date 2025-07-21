from path_extract.constants import Columns
from path_extract.study.dataframes import edit_breakdown_df
from path_extract.utils import set_difference
from path_extract.study.plots.data_compare import (
    get_names,
    check_elements,
    check_sums,
    get_diff,
    print_names_ordered,
    calc_diff,
)

import polars as pl
from rich import print as rprint

from path_extract.project_paths import CLMTPath, ProjectNames


def compare_two_experiments0(baseline: pl.DataFrame, alternative: pl.DataFrame):
    pass
    # TODO assert that have edited breakdown df.

    # baseline_elements = baseline[Columns.ELEMENT.name].unique()
    # alternative_elements = alternative[Columns.ELEMENT.name].unique()
    # missing_from_baseline = set_difference(baseline_elements, alternative_elements)
    # missing_from_alternative = set_difference(alternative_elements, baseline_elements)
    # rprint(
    #     f"missing from baseline: {missing_from_baseline} missing from alternative: {missing_from_alternative}"
    # )
    # to_add_to_baseline = baseline.filter(pl.col(Columns.ELEMENT.name).is_in(missing_from_baseline))
    # rprint("new in baseline:", to_add_to_baseline)
    # # TODO check that the missing are all in the joined df..

    # all_elemement_df = baseline.extend(to_add_to_baseline)
    # with pl.Config(tbl_rows=-1):
    #     rprint(f"all element df: {all_elemement_df[Columns.ELEMENT.name].unique().sort()}")

    # df = (
    #     all_elemement_df.join(
    #         alternative,
    #         on=[
    #             Columns.SECTION.name,
    #             Columns.TYPE.name,
    #             Columns.CATEGORY.name,
    #             Columns.ELEMENT.name,
    #             Columns.UNIT.name,
    #             Columns.CUSTOM_CATEGORY.name,
    #         ],
    #         how="right",
    #         suffix="_ALT",
    #     )
    #     .with_columns(pl.col(Columns.VALUE.name).fill_null(strategy="zero"))
    #     .rename(
    #         {
    #             Columns.VALUE.name: Columns.BASELINE.name,
    #             Columns.VALUE_ALT.name: Columns.ALT.name,
    #         }
    #     )

    # with pl.Config(tbl_rows=-1):
    #     rprint(f"baseline elements: {baseline[Columns.ELEMENT.name].unique().sort()}")
    # rprint("new in baseline:", to_add_to_baseline) # TODO make some modifications to this to make it approp..

    # col_diff =  set_difference(missing_from_alternative + missing_from_baseline, df[Columns.ELEMENT.name].unique().to_list())
    # rprint(f"\ncol diff: {col_diff}") # TODO assert len of col_diff == 0

    # rprint(
    #     f"baseline: {baseline.shape}, alternative: {alternative.shape}, joined: {df.shape}"
    # )

    # df2 = (
    #     df.with_columns(
    #         VALUE_DIFF=pl.col(Columns.ALT.name) - pl.col(Columns.BASELINE.name)
    #     )
    #     .filter(pl.col(Columns.VALUE_DIFF.name) != 0)
    #     .select(
    #         [
    #             pl.col(Columns.CUSTOM_CATEGORY.name),
    #             pl.col(Columns.CATEGORY.name),
    #             pl.col(Columns.ELEMENT.name),
    #             pl.col(Columns.VALUE_DIFF.name),
    #         ]
    #     )
    #     .sort(by=Columns.CUSTOM_CATEGORY.name)
    # )

    # with pl.Config(tbl_rows=-1):
    #     rprint(df2)

    # return df2


# TODO share with pres works
def get_exp_df(
    project_name: ProjectNames,
    exp_num: int,
):
    clmt_path = CLMTPath(project_name)
    init_df = clmt_path.read_csv(exp_num)
    return edit_breakdown_df(init_df)


def initial_join(base: pl.DataFrame, alt: pl.DataFrame):
    df = base.join(
        alt,
        on=[
            Columns.SECTION.name,
            Columns.TYPE.name,
            Columns.CATEGORY.name,
            Columns.ELEMENT.name,
            Columns.UNIT.name,
            Columns.CUSTOM_CATEGORY.name,
        ],
        how="left",
        suffix="_ALT",
    )

    return df


def secondary_extend(intermed: pl.DataFrame, base: pl.DataFrame, alt: pl.DataFrame):
    def get_missing_from_base():
        names_in_joined = get_names(intermed, Columns.ELEMENT.name)
        alt_names = get_names(alt, Columns.ELEMENT.name)
        return set_difference(alt_names, names_in_joined)

    missing_from_base = get_missing_from_base()

    df_to_add = (
        alt.filter(pl.col(Columns.ELEMENT.name).is_in(missing_from_base))
        .with_columns(pl.col(Columns.VALUE.name).alias(Columns.VALUE_ALT.name))
        .with_columns(pl.lit(0, dtype=pl.Int64).alias(Columns.VALUE.name))
    )
    return intermed.extend(df_to_add).fill_null(0)


def compare_two_experiments(
    project_name: ProjectNames, base_exp_num: int, alt_exp_num: int
):
    base = get_exp_df(project_name, base_exp_num)
    alt = get_exp_df(project_name, alt_exp_num)
    # rprint(base.head())

    # print_names_ordered(base, "base")

    intermed = initial_join(base, alt)
    # print_names_ordered(intermed, "intermed")
    df = secondary_extend(intermed, base, alt)

    check_elements(df, base, alt, name_col=Columns.ELEMENT.name)
    check_sums(
        df, base, alt, val1_col=Columns.VALUE.name, val2_col=Columns.VALUE_ALT.name
    )

    # rprint(d)

    with_diff = calc_diff(
        df, val1_col=Columns.VALUE.name, val2_col=Columns.VALUE_ALT.name
    )
    return get_diff(with_diff).sort(
        by=[Columns.CUSTOM_CATEGORY.name, Columns.VALUE_DIFF.name, Columns.ELEMENT.name]
    )


if __name__ == "__main__":
    d = compare_two_experiments("pier_6", 1, 0)
    rprint(get_diff(d))
    d = compare_two_experiments("pier_6", 0, 1)
    rprint(get_diff(d))
