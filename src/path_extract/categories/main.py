from enum import StrEnum
from rich import print as rprint
from path_extract.project_paths import CLMT_PROJECTS_INPUTS,  CLMTPath, ProjectNames
from pathlib import Path

from path_extract.utils import get_path_subdirectories

#TODO get list of all categories from all projects 
# map them to new categories associated with the use

class UseCategories(StrEnum): # also review what is in path finder.. 
    DEMO = "Demolition and Site Preparation"
    NEW_PlANTING = "New Planting" # TODO 'on-structure'
    PRESERVED_PLANTING = "Preserved Planting"
    SUBSTRUCTURE = "Substructure"
    HARDSCAPE = "Hardscape"
    ACCESSORIES = "Accessories"




def get_categories():
    def get_project_csvs(project: Path):
        clmt_path = CLMTPath(project.stem) # type: ignore # TODO fix this type issue -> breakdown / pverview + type names should probably be an enum 




    projects = get_path_subdirectories(CLMT_PROJECTS_INPUTS) #TODO make this a util and replace it where it is used


    # get all projects 
    # fore each project, get all csvs (run if have not already been run)
    # get the materials list  
