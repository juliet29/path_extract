from path_extract.constants import ClassNames, Headings, TableNames
from rich import print as rprint
from path_extract.file_utils import read_csv
from path_extract.project_paths import CLMTPath, SAMPLE_CLMT_PATH
import polars as pl
from path_extract.clmt_pilot.revised_categories import revised_categories, create_pairs


def get_emissions_df(df: pl.DataFrame):
    d = df.filter(
        pl.col(ClassNames.VALUE.name) > 0
    )  # strong filter for right now where dont have valid data..

    d = df.filter(pl.col(ClassNames.SECTION.name) == Headings.CARBON_IMPACT.value)
    # rprint(d)
    return d


def reorganize_categories(df: pl.DataFrame):
    pairs = create_pairs(revised_categories)
    d = df.with_columns(
        (
            pl.coalesce(
                # this syntax should allow to fail smoothly if element is NOT in dataframe.. 
                pl.when(pl.col(ClassNames.ELEMENT.name) == cond).then(pl.lit(result))
                for cond, result in pairs
            )
        ).alias(TableNames.CUSTOM_CATEGORY.name)
    ).with_columns(
        # pl.when(pl.col(TableNames.CUSTOM_CATEGORY.name).is_null()).then(pl.col(ClassNames.CATEGORY.name))
        pl.col(TableNames.CUSTOM_CATEGORY.name).fill_null(
            pl.col(ClassNames.CATEGORY.name)
        )
    )
    return d

def edit_breakdown_df(df):
    df1 = get_emissions_df(df)
    df2 = reorganize_categories(df1)
    return df2

if __name__ == "__main__":
    clmt_path = CLMTPath("newtown_creek")
    df = read_csv(SAMPLE_CLMT_PATH.get_csv(0))
    # rprint(sorted(list(df[ClassNames.ELEMENT.name].unique())))
    d = edit_breakdown_df(df)
    rprint(d)