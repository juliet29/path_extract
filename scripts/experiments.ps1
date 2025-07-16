. .\setup.ps1
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
New-Setup "Newtown Creek" "$Folder_Name\Newtown-Pave-Study 1- Depth-Reduction-page_{0}.txt" $newtown_creek[2] 2;
New-Setup "Newtown Creek" "$Folder_Name\Newtown-Pave-Study 1- Depth-Reduction-page_{0}.txt" $newtown_creek[3] 3;
# ideally run the project at the same -> to create the csv upon import .. 
# "R:\00-WORKSTREAMS\CLMT\CLMT Pilot Projects\Newtown Creek\250715_Study\Newtown-Pave-Study 1- Depth-Reduction-page_2.txt"