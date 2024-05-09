# WG-Gesucht: Web Crawler Project

Welcome to the WG-Gesucht Web Crawler Project. This repository includes a set of tools designed to extract and analyze data from WG-Gesucht, enabling users to understand housing market trends more efficiently.

## Project Structure

This project is organized into several key directories:

- **.setup**: Contains setup scripts for Unix and Windows environments.
- **DataAnalysis**: Jupyter notebooks for data cleaning and analysis.
- **WebCrawlerApp**: Python scripts for web crawling.
- **requirements.txt**: Lists all Python libraries that the project depends on.

### Detailed Directory Contents

- **WebCrawlerApp**
  - `RoomUrlCrawler.py`: First, Gathers URLs of rooms from WG-Gesucht.
  - `RoomInfoCrawler.py`: Second, Extracts detailed information about rooms. 
  - `data`: Folder to store output data.
  - `helpers`: Helper scripts and utilities.

- **DataAnalysis**
  - `DataCleaning.ipynb`: Notebook for cleaning the gathered data.
  - `MakroAnalysis.ipynb`: Macro-level analysis of the WG-Gesucht data. 
  - `PriceAnalysis.ipynb`: Analysis of room prices.
  - `PriceDeterminantsAnalysis.ipynb`: Investigates what factors influence room prices.
  - `data`: Processed data from web crawlers.
  - `src`: Additional files for analysis functions.

## Installation Process

Follow these steps to set up the WG-Gesucht Web Crawler Project environment:

### Prerequisites

- **IDE**: Visual Studio Code is recommended for an optimal development experience.

### Setup Instructions

1. **Clone the Repository**: Start by cloning this repository to your local machine.
2. **Operating System Specific Setup, Automated Pyhton Installation**:
   - **Unix/Linux/MacOS**:
     - Open the Terminal in VSCode. 
     - Now, you should be in the following directory: WG-Gesucht
     - Navigate with the terminal to the `.setup` directory from project root.
        ```bash
       cd .setup
       ```
     - Run the setup script for the installation of Python via HomeBrew and Zsh:
       ```bash
       ./unix.sh
       ```
   - **Windows**:
     - Open Windows Explorer. 
     - Navigate to the folder where the Repository is installed. 
     - Open the folder `.setup`. 
     - Start the `windows.ps1`script by right klicking the mouse and choose start with PowerShell. 

3. **Restart IDE**: Once the scripts have completed, restart Visual Studio Code to refresh the environment. 
4. **Virtual Environment**: 
   - The virtual Environment should be avaiable with Python 3.11.
   - To run the Crawler, choose the virtual Enviroment. 
   - To run the Notebooks, choose as a Kernel: WG-Gesucht Project.

## Usage

- Execute the web crawlers to gather data.
- Analyze the collected data using the provided Jupyter notebooks.

## Contributing

Contributions to this project are welcome. Please create a pull request with your proposed changes.

