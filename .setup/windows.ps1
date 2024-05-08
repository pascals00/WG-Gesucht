# Set the version and download URL for Python
$version = "3.11.9"
$url = "https://www.python.org/ftp/python/$version/python-$version-amd64.exe"

try {
    # Download and install Python
    $installPath = "$($env:ProgramFiles)\Python$version"
    Invoke-WebRequest -Uri $url -OutFile "python-$version.exe" -ErrorAction Stop
    Start-Process "python-$version.exe" -ArgumentList "/quiet", "TargetDir=$installPath" -Wait -ErrorAction Stop

    # Add Python to the system PATH
    $envVariable = [Environment]::GetEnvironmentVariable("Path", "Machine")
    if ($envVariable -notcontains $installPath) {
        [Environment]::SetEnvironmentVariable("Path", "$envVariable;$installPath", "Machine")
        Write-Host "Added Python to PATH."
    }

    Write-Host "Python $version installed successfully."

    # Confirm Python installation and add Python and Scripts folder to PATH for current session
    $pythonExePath = "$installPath\python.exe"
    $scriptsPath = "$installPath\Scripts"
    $env:Path += ";$installPath;$scriptsPath"

    # Verify Python installation
    & $pythonExePath --version

    # Install Python packages from requirements.txt
    Write-Host "Installing Python packages from requirements.txt..."
    & "$scriptsPath\pip.exe" install -r ..\requirements.txt

    Write-Host "Python required packages installed successfully."
}
catch {
 Write-Host "An error occurred: $_"
}
finally {
 # Clean up
 if (Test-Path "python-$version.exe") {
     Remove-Item "python-$version.exe"
 }
}

# It may be necessary to restart the system or log off and back on for path changes to take effect
Write-Host "Please restart your system to ensure all changes take effect, especially PATH updates."
