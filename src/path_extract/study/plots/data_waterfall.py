from path_extract.constants import Columns
from path_extract.study.dataframes import edit_breakdown_df
from path_extract.utils import set_difference


import polars as pl
from rich import print as rprint

from path_extract.project_paths import CLMTPath


def compare_two_experiments(baseline: pl.DataFrame, alternative: pl.DataFrame):
    # TODO assert that have edited breakdown df.

    baseline_elements = baseline[Columns.ELEMENT.name].unique()
    alternative_elements = alternative[Columns.ELEMENT.name].unique()
    missing_from_baseline = set_difference(baseline_elements, alternative_elements)
    missing_from_alternative = set_difference(alternative_elements, baseline_elements)
    rprint(
        f"missing from baseline: {missing_from_baseline} missing from alternative: {missing_from_alternative}"
    )
    to_add_to_baseline = baseline.filter(pl.col(Columns.ELEMENT.name).is_in(missing_from_baseline))
    rprint("new in baseline:", to_add_to_baseline) 
    # TODO check that the missing are all in the joined df..

    all_elemement_df = baseline.extend(to_add_to_baseline)
    with pl.Config(tbl_rows=-1):
        rprint(f"all element df: {all_elemement_df[Columns.ELEMENT.name].unique().sort()}")
    
    

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
    )

    
    # with pl.Config(tbl_rows=-1):
    #     rprint(f"baseline elements: {baseline[Columns.ELEMENT.name].unique().sort()}")
    rprint("new in baseline:", to_add_to_baseline) # TODO make some modifications to this to make it approp..

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


if __name__ == "__main__":
    # TODO make test -> typical use case
    # df = read_csv(SAMPLE_CLMT_PATH.get_csv(0))
    # d = edit_breakdown_df(df)
    # rprint(d)

    # compare two experiments
    clmt_path = CLMTPath("pier_6")
    baseline = edit_breakdown_df(clmt_path.read_csv(0))
    alternative = edit_breakdown_df(clmt_path.read_csv(1))
    compare_two_experiments(baseline, alternative)