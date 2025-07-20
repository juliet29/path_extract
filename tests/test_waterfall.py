from rich import print as rprint
from path_extract.study.plots.data_compare import get_names
from path_extract.study.plots.data_compare import get_expected_elements
from path_extract.utils import are_sets_equal
from path_extract.study.plots.data_compare import (
    baseline,
    small_alt,
    large_alt,
    compare_two_datafames,
)
import pytest


def test_small_baseline_df():
    df = compare_two_datafames(baseline, small_alt)
    df_names = get_names(df)
    rprint(df_names)
    expected_names = get_expected_elements(baseline, small_alt)
    are_sets_equal(df_names, expected_names)


# @pytest.mark.skip()
def test_large_baseline_df():
    df = compare_two_datafames(baseline, large_alt)
    df_names = get_names(df)
    expected_names = get_expected_elements(baseline, large_alt)
    are_sets_equal(df_names, expected_names)

    # the columns in the final df should be the union ..


if __name__ == "__main__":
    # rprint(baseline, small_alt, large_alt)
    rprint(get_expected_elements(baseline, large_alt))
