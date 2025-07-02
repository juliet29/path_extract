from path_extract.extract.extract import extract_data
from path_extract.analyze.analyze import clean_df, plot_elements_by_category
from path_extract.paths import PIER6, NEWTOWN, P2, P2_CSV, EXP_0, INFO
from path_extract.constants import ExperimentInfo
from pathlib import Path
from rich import print as rprint 
import polars as pl 
import json 
import altair as alt 

def create_csvs_for_p2(folder:Path):
	dirs = [i for i in folder.iterdir() if i.is_dir()]
	rprint(dirs)
	for dir in dirs:
		html_file = dir / P2
		csv_file = dir / "p2.csv"
		df = extract_data(html_file)
		df.write_csv(csv_file)
		pass
	
def read_csv(path:Path, file_name: str):
	return pl.read_csv(path / file_name)

def read_json(path:Path, file_name: str):
	_path = path / file_name
	assert _path.exists()
	with open(_path, "r") as f:
		# check = f.read()
		# rprint(check)
		data = json.load(f)
		# print(data)
		return data
	# return None

def read_exp_info(path:Path):
	data: ExperimentInfo = read_json(path, INFO)
	return f"{data["project"]} -- {data["experiment"]}"
	
def plot_experiment(path: Path, renderer="browser"):
	name = read_exp_info(path)
	# rprint(name)
	df = read_csv(path, P2_CSV)
	df2 = clean_df(df)
	plot_elements_by_category(df2, name, renderer)

	


if __name__ == "__main__":
	plot_experiment(PIER6/EXP_0)
	# df = read_csv(PIER6/EXP_0, P2_CSV)
	# df2 = clean_df(df)
	# plot_elements_by_category(df2)
	
	# rprint(df2)
	# create_csvs_for_p2(PIER6)
	# df = extract_data(SAMPLE_CLMT_HTML)
	# rprint(df.head(10))