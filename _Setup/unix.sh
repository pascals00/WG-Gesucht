#!/bin/bash

# Function to check and install Homebrew
ensure_homebrew_installed() {
    if ! which brew > /dev/null; then
        echo "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        echo "Homebrew is already installed."
    fi
}

# Function to check and install zsh
ensure_zsh_installed() {
    if ! which zsh > /dev/null; then
        echo "Installing zsh..."
        brew install zsh
        # Change default shell to zsh if it isn't already
        if [ "$SHELL" != "$(which zsh)" ]; then
            chsh -s $(which zsh)
        fi
    else
        echo "zsh is already installed."
    fi
}

# Function to install and configure Python
install_configure_python() {
    local required_version="3.11"
    local brew_python_path="/usr/local/opt/python@3.11/bin/python3"
    if brew list python@3.11 &>/dev/null && [ -x "$brew_python_path" ]; then
        local py_version=$($brew_python_path --version 2>&1)
        echo "Checking installed Python version: $py_version"
        if [[ "$py_version" == *"$required_version"* ]]; then
            echo "Python $required_version is already installed."
        else
            echo "Python $required_version is installed but may not be the default version."
            echo 'export PATH="/usr/local/opt/python@3.11/bin:$PATH"' >> ~/.zshrc
        fi
    else
        echo "Installing Python $required_version..."
        brew install python@3.11
        echo 'export PATH="/usr/local/opt/python@3.11/bin:$PATH"' >> ~/.zshrc
    fi
}

# Function to install Python packages from requirements.txt
install_python_packages() {
    local requirements_path="../requirements.txt"
    if [ -f "$requirements_path" ]; then
        # Create a temporary directory for the virtual environment
        local venv_dir=$(mktemp -d "/tmp/venv.XXXXXX")
        echo "Creating virtual environment in $venv_dir"
        
        # Create and activate the virtual environment
        python3 -m venv "$venv_dir"
        source "$venv_dir/bin/activate"
        
        # Install packages from requirements.txt
        pip install -r "$requirements_path"
        
        # Deactivate and remove the virtual environment
        deactivate
        echo "Removing virtual environment..."
        rm -rf "$venv_dir"
        
        echo "Setup completed!"
    else
        echo "requirements.txt not found. Please ensure it is located at $requirements_path."
        exit 1
    fi
}

# Main script execution
ensure_homebrew_installed
ensure_zsh_installed
install_configure_python
source ~/.zshrc
install_python_packages
