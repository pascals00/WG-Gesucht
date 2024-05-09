# Set the version and download URL for Python
$version = "3.11.6"
$url = "https://www.python.org/ftp/python/$version/python-$version-amd64.exe"
$downloadPath = "$env:USERPROFILE\Downloads\python-$version-amd64.exe"


try {
    # Download Python installer to the Downloads folder
    Invoke-WebRequest -Uri $url -OutFile $downloadPath -ErrorAction Stop
    Write-Host "Python installer downloaded to $downloadPath."

    # Install Python (defaulting to the location where Python usually installs)
    Start-Process $downloadPath -ArgumentList "/quiet PrependPath=1" -Wait
    Write-Host "Python $version installed successfully."

    # The path where Python is actually installed
    $actualInstallPath = "$env:LOCALAPPDATA\Programs\Python\Python311"

    # Verify Python installation
    $pythonExePath = "$actualInstallPath\python.exe"
    if (Test-Path $pythonExePath) {
        Write-Host "Python installation verified at $pythonExePath"
    } else {
        throw "Python executable not found at expected location: $pythonExePath"
    }

    # Add Python to the system PATH for current session
    $scriptsPath = "$actualInstallPath\Scripts"
    $env:Path += ";$actualInstallPath;$scriptsPath"

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
        $venvScriptsPath = "$venvDir\Scripts\Activate.ps1"
        . $venvScriptsPath

        # Install packages from requirements.txt
        & "$venvDir\Scripts\pip.exe" install -r $requirementsPath
        Write-Host "Python required packages installed successfully."

        # Check if the Jupyter kernel already exists, create if not
        if (-not (& "$venvDir\Scripts\python.exe" -m jupyter kernelspec list | Select-String "wg_gesucht_project_env")) {
            # Install a new Jupyter kernel associated with this environment
            & "$venvDir\Scripts\python.exe" -m ipykernel install --user --name=wg_gesucht_project_env --display-name="WG-Gesucht Project"
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
    if (Test-Path $downloadPath) {
       Remove-Item $downloadPath
    }

    # It may be necessary to restart the system or log off and back on for path changes to take effect
    Write-Host "Please restart your system to ensure all changes take effect, especially PATH updates."
    Pop-Location
}
