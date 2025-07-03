# . .\setup.ps1
# $pier_6 = @{
#     0 = 'EDC original scope'
#     1 = 'Entire project'
#     2 = 'Landscape only'
# }
# for (($i = 0);  ($i -lt $pier_6.Count);, ($i++)){
#     $value = $pier_6[$i]
#     New-Setup "Pier 6" "$value\Page {0} Pathfinder.txt" $value $i;
# }



$newtown_creek = @{
    0 = 'baseline'
}
for (($i = 0);  ($i -lt $newtown_creek.Count);, ($i++)){
    $value = $newtown_creek[$i]
    New-Setup "Newtown Creek" "Newtown-Creek-page_{0}.txt" $value $i;
}



# TODO make this work!
# function New-Project {
#     param (
#         [hashtable] $NamesDict,
#         [string] $FilePattern,
#         [string] $ProjectName
#     )

#     for (($i = 0);  ($i -lt $NamesDict.Count);, ($i++)){
#     $value = $NamesDict[$i]
# 	New-Setup "Pier 6" "$value\Page {0} Pathfinder.txt" $value $i;
# }
# }
