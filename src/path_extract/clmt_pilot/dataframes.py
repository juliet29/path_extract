from path_extract.constants import ClassNames, Headings, TableNames
from rich import print as rprint
from path_extract.file_utils import read_csv
from path_extract.project_paths import CLMTPath, SAMPLE_CLMT_PATH
import polars as pl
from path_extract.clmt_pilot.revised_categories import create_pairs
from path_extract.categories.assign import assign_dict, check_assign_dict
from path_extract.categories.categories import UseCategories


def get_emissions_df(df: pl.DataFrame):
    d = df.filter(
        pl.col(ClassNames.VALUE.name) > 0
    )  # strong filter for right now where dont have valid data..

    d = df.filter(pl.col(ClassNames.SECTION.name) == Headings.CARBON_IMPACT.value)
    # rprint(d)
    return d



def include_use_categories(df: pl.DataFrame):
    check_assign_dict()
    pairs = create_pairs(assign_dict)
    # rprint(pairs)
    d = df.with_columns(
        (
            pl.coalesce(
                # this syntax should allow to fail smoothly if element is NOT in dataframe.. 
                pl.when(pl.col(ClassNames.CATEGORY.name) == cond).then(pl.lit(result.name))
                for cond, result in pairs
            )
        ).alias(TableNames.CUSTOM_CATEGORY.name)
    ).with_columns(
        pl.col(TableNames.CUSTOM_CATEGORY.name).fill_null(
            pl.col(ClassNames.CATEGORY.name)
        )
    ).sort(by=pl.col(TableNames.CUSTOM_CATEGORY.name).map_elements(lambda x: UseCategories[x].value[0], return_dtype=pl.Int64))
    return d



def edit_breakdown_df(df):
    df1 = get_emissions_df(df)
    # df2 = reorganize_element_categories(df1)
    df2 = include_use_categories(df1)
    return df2

if __name__ == "__main__":
    # clmt_path = CLMTPath("newtown_creek")
    df = read_csv(SAMPLE_CLMT_PATH.get_csv(0))
    # rprint(sorted(list(df[ClassNames.ELEMENT.name].unique())))
    d = edit_breakdown_df(df)
    rprint(d)