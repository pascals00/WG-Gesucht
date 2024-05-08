#!/bin/bash

echo "Warning: This script will attempt to uninstall all Python installations from your system."
read -p "Are you sure you want to proceed? (y/n) " confirmation
if [[ $confirmation != "y" && $confirmation != "Y" ]]; then
    echo "Uninstallation canceled."
    exit 1
fi

# Function to uninstall specific Python versions installed via Homebrew
uninstall_python_homebrew() {
    echo "Checking for Python versions installed via Homebrew..."
    local installed_pythons=$(brew list | grep 'python@')
    if [ -n "$installed_pythons" ]; then
        echo "Found installed Python versions:"
        echo "$installed_pythons"
        for py in $installed_pythons; do
            echo "Uninstalling $py..."
            brew uninstall --force $py
            if [ -d "/usr/local/Cellar/$py" ]; then
                echo "Error: Could not remove $py keg! Removing manually..."
                sudo rm -rf "/usr/local/Cellar/$py"
            fi
        done
        brew cleanup
        echo "Python versions uninstalled from Homebrew."
    else
        echo "No specific Python versions installed via Homebrew found."
    fi
}


# Function to uninstall Python installed manually or by other means
uninstall_python_manual() {
    echo "Checking for manually installed Python versions..."
    # Potential Python installation directories
    directories=("/Library/Frameworks/Python.framework/Versions"
                 "/usr/local/bin"
                 "/usr/bin")

    for dir in "${directories[@]}"; do
        if [[ -d $dir ]]; then
            echo "Searching in $dir..."
            # Find any 'python' executables or directories and remove them
            find $dir -iname "python*" -exec sudo rm -rf {} +;
        fi
    done
    echo "Manually installed Python versions (if any) have been removed."
}

# Function to uninstall Python from Anaconda if present
uninstall_python_anaconda() {
    echo "Checking for Anaconda installed Python versions..."
    if which conda >/dev/null; then
        echo "Uninstalling Anaconda Python..."
        conda deactivate
        sudo rm -rf $(conda info --base)
        sudo rm -rf ~/anaconda3 ~/miniconda3
        echo "Anaconda Python has been uninstalled."
    else
        echo "No Anaconda Python found."
    fi
}

# Uninstall Python versions managed by Pyenv
uninstall_pyenv() {
    echo "Checking for Pyenv managed Python versions..."
    if type pyenv >/dev/null 2>&1; then
        echo "Uninstalling Pyenv managed Python versions..."
        for version in $(pyenv versions --bare); do
            pyenv uninstall -f $version
        done
        echo "Removing Pyenv..."
        rm -rf $(pyenv root)
        sed -i '' '/pyenv init/d' ~/.zshrc  # Adjust this line depending on your shell
    else
        echo "Pyenv not found."
    fi
}

uninstall_conda() {
    echo "Checking for Anaconda at /usr/local/anaconda3..."
    if [ -d "/usr/local/anaconda3" ]; then
        echo "Anaconda installation found. Uninstalling..."

        # Deactivate any active conda environment
        source /usr/local/anaconda3/bin/activate
        conda deactivate

        # Remove all conda environments
        echo "Removing all conda environments..."
        conda env list | grep -v '^#' | awk '{print $1}' | xargs -L1 conda env remove --name

        # Clean up conda installation
        conda clean --all -y
        
        # Uninstall Anaconda
        conda install -y anaconda-clean
        anaconda-clean --yes
        
        echo "Anaconda has been uninstalled."

        # Remove the conda and anaconda base installation directory
        echo "Removing Anaconda directory..."
        sudo rm -rf /usr/local/anaconda3

        # Clean up any initialization in shell configuration files
        sed -i '' '/anaconda3/d' ~/.zshrc
        sed -i '' '/conda init/d' ~/.zshrc

        echo "Anaconda directories and initializations have been cleaned up."
    else
        echo "No Anaconda installation found at /usr/local/anaconda3."
    fi
}


# Execute uninstall functions
uninstall_pyenv
uninstall_conda

echo "Python uninstallation complete. Please manually verify removal and clean up any remaining configurations."

# Execute uninstall functions
uninstall_python_homebrew
uninstall_python_manual
uninstall_python_anaconda

echo "Please remember to manually check your PATH settings and remove any Python-related entries."
echo "All done. It is recommended to restart your computer to complete the cleanup."
