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
    python -m build -o ${BuildDir}
}

Function Install {
    if ($Target -eq "") {
        # Install current version in config file
        # "${DISTDIR}\v${VERSION_HYPHENATED}\${PROJECT}-${VERSION}${PACKAGE_ENDING}"
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
    python -m pip install $Target
}

function CleanBuild () {
    if ($Target -eq "") {
        # Install current version in config file
        # "${DISTDIR}\v${VERSION_HYPHENATED}\${PROJECT}-${VERSION}${PACKAGE_ENDING}"
        $Target = $VERSION
    }
    if ( -not (Test-Path -Path $Target -PathType Leaf)) {

        if (-not(Test-Path -Path "${DISTDIR}\v$(${Target}.Replace(".","-"))\${PROJECT}-${Target}${PACKAGE_ENDING}")) {
            Write-Host "Could not find version  ${DISTDIR}\v$(${Target}.Replace(".","-"))\${PROJECT}-${Target}${PACKAGE_ENDING}"
        }
        else {
            $Target = "${DISTDIR}\v$(${Target}.Replace(".","-"))"
        }
    }
    Remove-Item -Recurse -Force $Target
}

<#
MAIN
#>

Switch (${Action}) {
    "version" { "${PROJECT} v${VERSION}" }

    "build" {
        CleanBuild ""
        Build
        break
    }
    "install" {
        Install ${Target}
        break
    }
    "update" {
        Build
        Install ${Target}
        break
    }
    "uninstall" {
        pip uninstall tasktracker
        break
    }
    "clean" {
        CleanBuild ${Target}
        break
    }

}



