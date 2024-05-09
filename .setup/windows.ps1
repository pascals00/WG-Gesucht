# Set the version and download URL for Python
$version = "3.11.9"
$url = "https://www.python.org/ftp/python/$version/python-$version-amd64.exe"

try {
    # Download and install Python
    $installPath = "$($env:ProgramFiles)\Python$version"
    Invoke-WebRequest -Uri $url -OutFile "python-$version.exe" -ErrorAction Stop
    Start-Process "python-$version.exe" -ArgumentList "/quiet InstallAllUsers=1 TargetDir=$installPath Include_test=0" -Wait -ErrorAction Stop

    # Add Python to the system PATH
    $envVariable = [Environment]::GetEnvironmentVariable("Path", "Machine")
    if (-not $envVariable.Contains($installPath)) {
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

    # Navigate to the script's directory
    Push-Location -Path (Split-Path -Path $MyInvocation.MyCommand.Definition -Parent)

    # Move up to the project root directory
    Set-Location ..

    # Define the path to the virtual environment and requirements file
    $venvDir = ".venv"
    $requirementsPath = "requirements.txt"

    # Check if the requirements file exists at the project root
    if (Test-Path $requirementsPath) {
        # Check if the virtual environment already exists, create if not
        if (-not (Test-Path $venvDir)) {
            Write-Host "Creating virtual environment in $venvDir"
            & $pythonExePath -m venv $venvDir
        } else {
            Write-Host "Virtual environment already exists."
        }

        # Activate the virtual environment
        $venvScriptsPath = "$venvDir\Scripts"
        & "$venvScriptsPath\Activate.ps1"

        # Install packages from requirements.txt
        & "$venvScriptsPath\pip.exe" install -r $requirementsPath

        Write-Host "Python required packages installed successfully."

        # Check if the Jupyter kernel already exists, create if not
        if (-not (& "$venvScriptsPath\python.exe" -m jupyter kernelspec list | Select-String "wg_gesucht_project_env")) {
            # Install a new Jupyter kernel associated with this environment
            & "$venvScriptsPath\python.exe" -m ipykernel install --user --name=wg_gesucht_project_env --display-name="WG-Gesucht Project"
            Write-Host "Jupyter kernel for 'WG-Gesucht Project' environment has been installed."
        } else {
            Write-Host "Jupyter kernel 'WG-Gesucht Project' already exists. No need to install."
        }

        # Deactivate the virtual environment
        Write-Host "Setup completed!"
    } else {
        Write-Host "requirements.txt not found at the project root. Please ensure it is located at $(Get-Location)\$requirementsPath."
        exit 1
    }
}
catch {
    Write-Host "An error occurred: $_"
}
finally {
    # Clean up
    if (Test-Path "python-$version.exe") {
        Remove-Item "python-$version.exe"
    }

    # It may be necessary to restart the system or log off and back on for path changes to take effect
    Write-Host "Please restart your system to ensure all changes take effect, especially PATH updates."
    Pop-Location
}
