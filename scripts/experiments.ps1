. .\setup.ps1
$SRC_PATH = "C:\Users\juliet.intern\_SCAPECode\pathfinder\src\path_extract"


# $pier_6 = @{
#     0 = 'EDC original scope'
#     1 = 'Entire project'
#     2 = 'Landscape only'
# }
# for (($i = 0);  ($i -lt $pier_6.Count);, ($i++)){
#     $value = $pier_6[$i]
#     New-Setup "Pier 6" "$value\Page {0} Pathfinder.txt" $value $i;
# }



# $newtown_creek = @{
#     0 = 'baseline'
# }
# for (($i = 0);  ($i -lt $newtown_creek.Count);, ($i++)){
#     $value = $newtown_creek[$i]
#     New-Setup "Newtown Creek" "Newtown-Creek-page_{0}.txt" $value $i;
# }

# $BPCR = @{
#     0 = 'paving'
# }
# for (($i = 0);  ($i -lt $BPCR.Count);, ($i++)){
#     $value = $BPCR[$i]
#     New-Setup "BPCR" "BPCR_Scorecard_Paving_P{0}.txt" $value $i;
# }


# $SAGINAW = @{
#     0 = 'Baseline'
# }
# for (($i = 0);  ($i -lt $SAGINAW.Count);, ($i++)){
#     $value = $SAGINAW[$i]
#     New-Setup "Saginaw" "$value\Saginaw Riverfront Park-Page {0}.txt" $value $i;
# }



## Newtown Creek Complete.. 
$Folder_Name = "250715_Study"
$newtown_creek = @{
    0 = 'baseline'
    1 = 'depth_reduction'
    2 = 'area_reduction'
    3 = 'depth_area_reduction'
}
New-Setup "Newtown Creek" "Newtown-Creek-page_{0}.txt" $newtown_creek[0] 0;
New-Setup "Newtown Creek" "$Folder_Name\Newtown-Pave-Study 1- Depth-Reduction-page_{0}.txt" $newtown_creek[1] 1;
New-Setup "Newtown Creek" "$Folder_Name\Newtown-Pave-Study-2-Area-Reduction-page_{0}.txt" $newtown_creek[2] 2;
New-Setup "Newtown Creek" "$Folder_Name\Newtown-Pave-Study-3-Depth+Area-Reduction-page_{0}.txt" $newtown_creek[3] 3;
uv run "$SRC_PATH\extract\extract.py" "newtown_creek"


# "R:\00-WORKSTREAMS\CLMT\CLMT Pilot Projects\Newtown Creek\250715_Study\Newtown-Pave-Study-2-Area-Reduction-page_2.txt"t"
