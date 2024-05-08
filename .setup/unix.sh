#!/bin/bash

# Function to check and install Homebrew
ensure_homebrew_installed() {
    if ! command -v brew >/dev/null 2>&1; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        echo "Homebrew is already installed."
    fi
}

# Function to check and install zsh
ensure_zsh_installed() {
    if ! command -v zsh >/dev/null 2>&1; then
        echo "Installing zsh..."
        brew install zsh
        # Change default shell to zsh if it isn't already
        if [ "$SHELL" != "$(command -v zsh)" ]; then
            chsh -s $(command -v zsh)
        fi
    else
        echo "zsh is already installed."
    fi
}

# Function to install and configure Python
install_configure_python() {
    local required_version="3.11"
    local brew_python_path="/usr/local/opt/python@3.11/bin/python3"
    local cellar_python_path="/usr/local/Cellar/python@3.11/3.11.9/bin/python3.11"

    if brew list python@3.11 &>/dev/null; then
        if [ -x "$cellar_python_path" ]; then
            local py_version=$($cellar_python_path --version 2>&1)
            echo "Checking installed Python version: $py_version"
            if [[ "$py_version" == *"$required_version"* ]]; then
                echo "Python $required_version is already installed."
            else
                echo "Python $required_version is installed but may not be the default version."
            fi
        fi
        # Ensure the symlink is correctly established
        ln -sf $cellar_python_path $brew_python_path
        echo "Symlink for Python $required_version has been created."
    else
        echo "Installing Python $required_version..."
        brew install python@3.11
        # Ensure the symlink is correctly established
        ln -sf $cellar_python_path $brew_python_path
        echo "Symlink for Python $required_version has been created."
    fi
    echo 'export PATH="/usr/local/opt/python@3.11/bin:$PATH"' >> ~/.zshrc
}

#!/bin/bash

# Function to install Python packages from requirements.txt at the project root
install_python_packages() {
    # Navigate to the script's directory
    cd "$(dirname "$BASH_SOURCE")"
    
    # Move up to the project root directory, assuming the script is stored in WG-Gesucht/_Setup
    cd ..

    # Define the path to the virtual environment and requirements file
    local venv_dir=".venv"
    local requirements_path="requirements.txt"

    # Check if the requirements file exists at the project root
    if [ -f "$requirements_path" ]; then
        # Check if the virtual environment already exists, create if not
        if [ ! -d "$venv_dir" ]; then
            echo "Creating virtual environment in $venv_dir"
            python3 -m venv "$venv_dir"
        else
            echo "Virtual environment already exists."
        fi

        # Activate the virtual environment
        source "$venv_dir/bin/activate"

        # Install packages from requirements.txt
        pip install -r "$requirements_path"

        # Deactivate the virtual environment
        source "$venv_dir/bin/deactivate"

        if ! jupyter kernelspec list | grep -q 'wg_gesucht_project_env'; then
            # Install a new Jupyter kernel associated with this environment
            "$venv_dir/bin/python3" -m ipykernel install --user --name=wg_gesucht_project_env --display-name="WG-Gesucht Project"
            echo "Jupyter kernel for 'WG-Gesucht Project' environment has been installed."
        else
            echo "Jupyter kernel 'WG-Gesucht Project' already exists. No need to install."
        fi

        # Deactivate the virtual environment
        echo "Setup completed!"
    else
        echo "requirements.txt not found at the project root. Please ensure it is located at $PWD/$requirements_path."
        exit 1
    fi
}


# Main script execution
ensure_homebrew_installed
ensure_zsh_installed
install_configure_python
install_python_packages
