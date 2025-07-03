function Test-MrParameter {

    param (
        [Parameter(Mandatory)]
        [string] $SourceFolder,
        
        [Parameter(Mandatory)]
        [string] $SourceFileName,

        [Parameter(Mandatory)]
        [string] $DestFolder, # should have a default 

        [Parameter(Mandatory)]
        [string] $Project,

        [Parameter(Mandatory)]
        [string] $ExpName,
        
        [Parameter(Mandatory)]
        [string] $ExpNumber
    )

    New-Item -Path $DestFolder\$Project\$ExpName
}
