from path_extract.extract.extract import extract_data
from path_extract.paths import PIER6, NEWTOWN, P2, P2_CSV
from pathlib import Path
from rich import print as rprint 

def create_csvs_for_p2(folder:Path):
	dirs = [i for i in folder.iterdir() if i.is_dir()]
	rprint(dirs)
	for dir in dirs:
		html_file = dir / P2
		csv_file = dir / "p2.csv"
		df = extract_data(html_file)
		df.write_csv(csv_file)
		pass


if __name__ == "__main__":
	pass
	create_csvs_for_p2(PIER6)
	# df = extract_data(SAMPLE_CLMT_HTML)
	# rprint(df.head(10))