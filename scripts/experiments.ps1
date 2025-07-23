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



function ReadSaginaw {
    # $SHome = "P:\2433 - Saginaw Riverfront Park\03_Research\07_CLMT\Pathfinder\OPT 2-importing soil"
    # $SDest = "R:\00-WORKSTREAMS\CLMT\CLMT Pilot Projects\Saginaw\Pathfinder_Data\OPT 2-importing soil"
    # Copy-Item "$Shome\Pg1.txt" $TextDestPath\pg1.txt
    # Copy-Item "$Shome\pg2.txt" $TextDestPath\pg2.txt
    ## Saginaw. 
    $Folder_Name = "Pathfinder_Data"
    $saginaw = @{
        0 = 'reuse'
        1 = 'import'
    }
    New-Setup "Saginaw" "$Folder_Name\OPT 1-reuse of soil\Saginaw Riverfront Park-Page {0}.txt" $saginaw[0] 0;
    New-Setup "Saginaw" "$Folder_Name\OPT 2-importing soil\pg{0}.txt" $saginaw[1] 1
    uv run "$SRC_PATH\extract\extract.py" "saginaw"
}

# ReadSaginaw

function ReadNewtownCreek {
    $Folder_Name = "250722_Study"
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

    
}


#### ----------------- MAIN --------------------
. .\setup.ps1
$SRC_PATH = "C:\Users\juliet.intern\_SCAPECode\path_extract\src\path_extract"
ReadNewtownCreek


# "R:\00-WORKSTREAMS\CLMT\CLMT Pilot Projects\Newtown Creek\250715_Study\Newtown-Pave-Study-2-Area-Reduction-page_2.txt"t"
