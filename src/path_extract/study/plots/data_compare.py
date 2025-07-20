from enum import StrEnum
from typing import NamedTuple
from rich import print as rprint
import polars as pl

from path_extract.utils import are_sets_equal, set_difference, set_union

NAME = "name"
VAL = "val"
VAL2 = "val2"


class Fruit(StrEnum):
    GRAPES = "grapes"
    APPLES = "apples"
    PEARS = "pears"
    ORANGES = "oranges"
    PEACHES = "peaches"


class FruitPair(NamedTuple):
    fruit: str
    value: float


pairs = [
    FruitPair(i.value, k)
    for i, k in [
        (Fruit.GRAPES, 10.0),
        (Fruit.APPLES, 14.0),
        (Fruit.PEARS, 12.0),
        (Fruit.ORANGES, 8.0),
        (Fruit.PEACHES, 12.0),
    ]
]


def create_df(pairs: list[FruitPair], mult=1.0):
    return pl.DataFrame(
        {NAME: [i.fruit for i in pairs], VAL: [i.value * mult for i in pairs]}
    )


baseline = create_df(pairs[0:3])
small_alt = create_df(pairs[0:2], mult=0.5)
large_alt = create_df(pairs, mult=2)


def get_names(df: pl.DataFrame):
    return df[NAME].unique().to_list()


def get_expected_elements(base: pl.DataFrame, alt: pl.DataFrame):
    return set_union(get_names(base), get_names(alt))


def check_elements(joined_df: pl.DataFrame, base: pl.DataFrame, alt: pl.DataFrame):
    expected_names = get_expected_elements(base, alt)
    joined_names = get_names(joined_df)
    are_sets_equal(expected_names, joined_names)


def check_sums(joined_df: pl.DataFrame, base: pl.DataFrame, alt: pl.DataFrame):
    assert joined_df[VAL].sum() == base[VAL].sum()
    assert joined_df[VAL2].sum() == alt[VAL].sum()


def compare_two_datafames(base: pl.DataFrame, alt: pl.DataFrame):
    df = base.join(alt, on=[NAME], how="left", suffix="2")

    base_names = get_names(base)
    alt_names = get_names(alt)
    missing_from_base = set_difference(alt_names, base_names)
    df_to_add = (
        alt.filter(pl.col(NAME).is_in(missing_from_base))
        .with_columns(pl.col(VAL).alias(VAL2))
        .with_columns(val=pl.lit(0.0))
    )

    rprint(df, df_to_add)

    d = df.extend(df_to_add)

    check_sums(d, base, alt)
    check_elements(d, base, alt)

    return d


if __name__ == "__main__":
    r = compare_two_datafames(baseline, large_alt)
    rprint(r)
