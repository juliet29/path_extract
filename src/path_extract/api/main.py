from pathlib import Path
from path_extract.extract.breakdown import read_breakdown

def create_carbon_df(html_file: Path):
    assert html_file.suffix == ".html"
    # going to assume the file exists if we are getting it from marimo .. 
    df = read_breakdown(html_file)