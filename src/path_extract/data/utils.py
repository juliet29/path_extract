import polars as pl
import path_extract.data.columns as col


def add_category_label(df: pl.DataFrame):
    return df.with_columns(
        pl.col(col.CUSTOM_CATEGORY)
        .str.replace_all("_", " ")
        .str.to_titlecase()
        .alias(col.CUSTOM_CATGEORY_LABEL)
    )
