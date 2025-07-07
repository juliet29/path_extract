from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from path_extract.paths import PATH_TO_FIGURES, PATH_TO_INPUTS

# TODO move clmt pilot stuff to folder.. / make super object if have many .. 
DataTypes =  Literal["Breakdown", "Overview"]
BREAKDOWN = 2
OVERVIEW = 1
CLMT_PROJECTS = "250701_CLMT_Pilot_Sprint"
PILOT_PROJECTS = ["pier_6", "newtown_creek"] # TODO can use path lib to get names.. 
INFO = "info.json"
def EXP(x): return f"exp_{x}"
def HTML(x): return Path("html") / f"_{x}.html"
def CSV(x): return f"_{x}.csv"

def get_exp_num(exp_path:Path): 
    res = exp_path.stem.split("_")
    return int(res[1])

@dataclass
class CLMTPath:
    name: Literal["pier_6", "newtown_creek"]

    @property
    def input_path(self):
        p =  PATH_TO_INPUTS / CLMT_PROJECTS / self.name
        assert p.exists(), f"{self.name} does not exist in {CLMT_PROJECTS}!"
        return p
    
    @property
    def figures_path(self):
        # TODO might not exist, make it if it doesnt.. -> put function in utils.py
        return PATH_TO_FIGURES / CLMT_PROJECTS / self.name
    @property
    def experiment_paths(self):
        dirs = [i for i in self.input_path.iterdir() if i.is_dir()]
        return dirs
    
    def get_experiment_path(self, experiment_num):
        p =  self.input_path / EXP(experiment_num)
        assert p.exists(), f"No experiment with {experiment_num} exists!"
        return p
    
    def get_json(self, experiment_num: int):
        return self.get_experiment_path(experiment_num) / INFO 
    
    def get_html(self, experiment_num: int, datatype: DataTypes):
        num = OVERVIEW if datatype == "Overview" else BREAKDOWN
        # TODO wrapper function to test for existence.. 
        return self.get_experiment_path(experiment_num) / HTML(num)
    
    def get_csv(self, experiment_num: int, datatype: DataTypes):
        # TODO USE ENUM for breakdown / overview!
        num = OVERVIEW if datatype == "Overview" else BREAKDOWN
        return self.get_experiment_path(experiment_num) / CSV(num)


pier_6_paths = CLMTPath("pier_6")   
SAMPLE_CLMT_OVERVIEW_HTML = pier_6_paths.get_html(0, "Overview")
SAMPLE_CLMT_BREAKDOWN_HTML = pier_6_paths.get_html(0, "Breakdown")