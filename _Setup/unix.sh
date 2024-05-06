#!/bin/bash

# Function to check Python version
check_python_version() {
    PY_VERSION=$(python3 --version)
    if [[ "$PY_VERSION" == *"3.11"* ]]; then
        echo "Python 3.11 is already installed."
    else
        echo "Installing Python 3.11..."
        # Install Python 3.11
        brew install python@3.11
        # Update PATH variable
        echo 'export PATH="/usr/local/opt/python@3.11/bin:$PATH"' >> ~/.bash_profile
        source ~/.bash_profile
    fi
}

# Install Homebrew if not installed
which -s brew
if [[ $? != 0 ]] ; then
    # Install Homebrew
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew is already installed."
fi

# Check and install Python 3.11
check_python_version

# Install required Python packages
echo "Installing required Python packages..."
pip3 install -r requirements.txt

echo "Setup completed!"
