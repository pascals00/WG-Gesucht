# WG-Gesucht: Web Crawler Project

Welcome to the WG-Gesucht Web Crawler Project. This repository includes a set of tools designed to extract and analyze data from WG-Gesucht, enabling users to understand housing market trends more efficiently.

## Project Structure

This project is organized into several key directories:

- **.setup**: Contains setup scripts for Unix and Windows environments.
- **.venv**: Directory for the virtual environment.
- **DataAnalysis**: Jupyter notebooks for data cleaning and analysis.
- **README.md**: This file, providing an overview and setup instructions.
- **WebCrawlerApp**: Python scripts for web crawling.
- **requirements.txt**: Lists all Python libraries that the project depends on.

### Detailed Directory Contents

- **WebCrawlerApp**
  - `RoomInfoCrawler.py`: Extracts detailed information about rooms.
  - `RoomUrlCrawler.py`: Gathers URLs of rooms from WG-Gesucht.
  - `data`: Folder to store output data.
  - `helpers`: Helper scripts and utilities.

- **DataAnalysis**
  - `DataCleaning.ipynb`: Notebook for cleaning the gathered data.
  - `PriceAnalysis.ipynb`: Analysis of room prices.
  - `MakroAnalysis.ipynb`: Macro-level analysis of the housing market.
  - `PriceDeterminantsAnalysis.ipynb`: Investigates what factors influence room prices.
  - `data`: Data resulting from web crawlers.
  - `src`: Source files for analysis functions.

## Installation Process

Follow these steps to set up the WG-Gesucht Web Crawler Project environment:

### Prerequisites

- **IDE**: Visual Studio Code is recommended for an optimal development experience.
- **Python Version**: Ensure Python 3.11 is installed on your system.

### Setup Instructions

1. **Clone the Repository**: Start by cloning this repository to your local machine.
2. **Operating System Specific Setup**:
   - **Unix/Linux/MacOS**:
     - Navigate with the terminal to the `.setup` directory from project root.
     - Run the setup script:
       ```bash
       cd .setup
       ./unix.sh
       ```
   - **Windows**:
     - Open the `.setup` folder in PowerShell.
     - Execute the following command:
       ```powershell 
        cd .setup
       ./windows.ps1
       ```
3. **Restart IDE**: Once the scripts have completed, restart Visual Studio Code to refresh the environment.
4. **Virtual Environment**: 
   - Activate the virtual environment located in `.venv`.
   - Ensure the Python version is set to 3.11 in your IDE.
5. **Install Dependencies**: Install all required Python libraries by running:
