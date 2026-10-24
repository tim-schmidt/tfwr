# Copy the game files into the TFWR save folder so nothing has to be pasted.
# Every root .py and every file in Simulations/ lands flat in the save, with
# LF line endings the way the game writes them. Files the repo no longer has
# are removed from the save; save.json and __builtins__.py are never touched.
# The game may stay open: it is built to pick up external edits.
#
#   .\Sync.ps1              sync into the "Guide" save
#   .\Sync.ps1 -Save Test   sync into another save
param([string]$Save = "Guide")

$target = Join-Path $env:USERPROFILE "AppData\LocalLow\TheFarmerWasReplaced\TheFarmerWasReplaced\Saves\$Save"
if (-not (Test-Path $target)) { throw "No save folder at $target" }

$root = $PSScriptRoot
$sources = @(Get-ChildItem (Join-Path $root "*.py")) + @(Get-ChildItem (Join-Path $root "Simulations\*.py"))
$keep = @{}
foreach ($f in $sources) {
	$text = [IO.File]::ReadAllText($f.FullName).Replace("`r`n", "`n")
	$dest = Join-Path $target $f.Name
	if (-not (Test-Path $dest) -or [IO.File]::ReadAllText($dest) -ne $text) {
		[IO.File]::WriteAllText($dest, $text, [Text.UTF8Encoding]::new($false))
		Write-Host "updated $($f.Name)"
	}
	$keep[$f.Name] = $true
}
foreach ($f in Get-ChildItem (Join-Path $target "*.py")) {
	if ($f.Name -ne "__builtins__.py" -and -not $keep.ContainsKey($f.Name)) {
		Remove-Item $f.FullName
		Write-Host "removed $($f.Name)"
	}
}
Write-Host "synced $($sources.Count) files to $target"
