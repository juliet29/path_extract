from path_extract.extract.breakdown import get_breakdown_comparison, read_breakdown
from path_extract.extract.overview import get_overview_comparison, read_overview
from path_extract.project_paths import BREAKDOWN, HTML, OVERVIEW, CLMTPath, get_exp_num


def create_csvs_for_project(clmt_path: CLMTPath):
    def make_breakdown():
        html = exp_dir / HTML(BREAKDOWN)
        df = read_breakdown(html)
        return df, get_breakdown_comparison(df)

    def make_overview():
        html = exp_dir / HTML(OVERVIEW)
        df = read_overview(html)
        return df, get_overview_comparison(df)

    for exp_dir in clmt_path.experiment_paths:
        exp_num = get_exp_num(exp_dir)

        breakdown_df, breakdown_comp = make_breakdown()
        overview_df, overview_comp = make_overview()
        assert overview_comp == breakdown_comp, (
            f"Invalid comparisons! Breakdown: {breakdown_comp}. Overview: {overview_comp}"
        )

        breakdown_df.write_csv(clmt_path.get_csv(exp_num, "Breakdown"))
        overview_df.write_csv(clmt_path.get_csv(exp_num, "Overview"))
