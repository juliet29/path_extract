import pyprojroot

BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))



PATH_TO_INPUTS = BASE_PATH / "inputs"
SAMPLE_HTML = PATH_TO_INPUTS / "sample.html"
PATH_TO_CLMT_PROJECTS = PATH_TO_INPUTS / "250701_CLMT_Pilot_Sprint"


PIER6 =  PATH_TO_CLMT_PROJECTS/ "p1_pier6"
NEWTOWN = PATH_TO_CLMT_PROJECTS/  "p2_newtown"
P1 = "p1.html"
P2 = "p2.html"
P2_CSV = "p2.csv"
EXP_0 = "exp_0"
EXP_1 = "exp_1"
EXP_2 = "exp_2"

SAMPLE_CLMT_HTML = PATH_TO_CLMT_PROJECTS / PIER6 / EXP_0 / P2
