from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from path_extract.paths import PATH_TO_FIGURES, PATH_TO_INPUTS


DataTypes =  Literal["Breakdown", "Overview"]
CLMT_PROJECTS = "250701_CLMT_Pilot_Sprint"
PILOT_PROJECTS = ["pier_6", "newtown_creek"] # TODO can use path lib to get names.. 
INFO = "info.json"
def EXP(x): return f"exp_{x}"
def HTML(x): return Path("html") / f"_{x}.html"
def CSV(x): return f"_{x}.csv"

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
    
    def get_experiment_path(self, experiment_num):
        p =  self.input_path / EXP(experiment_num)
        assert p.exists(), f"No experiment with {experiment_num} exists!"
        return p
    
    def get_json(self, experiment_num: int):
        return self.get_experiment_path(experiment_num) / INFO 
    
    def get_html(self, experiment_num: int, datatype: DataTypes):
        num = 1 if datatype == "Overview" else 2
        # TODO wrapper function to test for existence.. 
        return self.get_experiment_path(experiment_num) / HTML(num)
    
    def get_csv(self, experiment_num: int, datatype: DataTypes):
        num = 1 if datatype == "Overview" else 2
        return self.get_experiment_path(experiment_num) / CSV(num)


pier_6_paths = CLMTPath("pier_6")   
SAMPLE_CLMT_OVERVIEW_HTML = pier_6_paths.get_html(0, "Overview")
SAMPLE_CLMT_BREAKDOWN_HTML = pier_6_paths.get_html(0, "Breakdown")