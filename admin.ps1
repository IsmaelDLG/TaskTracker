<#
PARAMS
#>
param(
    [Parameter(Mandatory, HelpMessage = "Please provide an action")]
    [string]$Action,

    [Parameter(HelpMessage = "Plase provide a target for the action")]
    [string]$Target
)

<#
CONSTANTS
#>

$PROJECT = ((Get-Content "setup.cfg" | Select-String -Pattern "name =" | Out-String).Replace("name =", "") -replace "\s", "")
$VERSION = ((Get-Content "setup.cfg" | Select-String -Pattern "version =" | Out-String) -replace "[a-zA-Z\s=#]", "")
$VERSION_HYPHENATED = $VERSION.Replace(".", "-")
$OUTDIR = "${PSScriptRoot}\output"
$DISTDIR = "${OUTDIR}\dist"
$PACKAGE_ENDING = ".tar.gz"

<#
FUNCTIONS
#>

Function Build {
    $BuildDir = "${PSScriptRoot}\output\dist\v$(${VERSION_HYPHENATED})"
    New-Item -ItemType Directory -Force -Path ${BuildDir} 
    python3 -m build -o ${BuildDir}
    Break
}

Function Install {
    param (
        [Parameter(HelpMessage = "Plase provide a target for the action")]
        [string]$Target
    )
    if ($Target -eq "") {
        # Install current version in config file
        "${DISTDIR}\v${VERSION_HYPHENATED}\${PROJECT}-${VERSION}${PACKAGE_ENDING}"
        $Target = $VERSION
    }
    if ( -not (Test-Path -Path $Target -PathType Leaf)) {

        if (-not(Test-Path -Path "${DISTDIR}\v$(${Target}.Replace(".","-"))\${PROJECT}-${Target}${PACKAGE_ENDING}")) {
            Write-Host "Could not find version locally, checking pip repository"
        }
        else {
            $Target = "${DISTDIR}\v$(${Target}.Replace(".","-"))\${PROJECT}-${Target}${PACKAGE_ENDING}"
        }
    }
    "Installing ${Target}..."
    python3 -m pip install $Target
}

<#
MAIN
#>

Switch (${Action}) {
    "version" { "${PROJECT} v${VERSION}"; Break }
    "build" {
        Build; Break
    }
    "update" {
        Build
        Install ${Target}; Break
    }
    "install" {
        Install ${Target}; Break
    }
}



