JIP Table Explorer

JIP Table Explorer is a robust Python tool designed to load, visualize, and analyze large data tables (CSV, DAT, TXT).

Unlike simply opening a file with a text editor or Notepad, JIP Table Explorer leverages the power of the Pandas library to structure your data. This allows you to sort columns, filter rows in real-time, and handle complex formats (such as scientific notation or irregular separators) that would otherwise be unreadable in a standard editor.

🚀 Key Features

More than a viewer: Sort ascending/descending by any numeric or text column simply by clicking the header.

Smart Filtering: Integrated search bar with support for Regular Expressions (RegEx) to find specific data points instantly.

Robust Loading: Intelligent algorithm that automatically detects the correct separator (commas, tabs, semicolons, or multiple spaces/scientific format).

Multi-window: Open and compare multiple files simultaneously in independent windows.

Smart Launchers: Includes automation scripts to detect your Conda installation or use your system Python.

📂 Included Files

The repository includes different execution methods and test data:

table_explorer.py: The main application script.

SAMPLE.csv: A sample data file to test sorting and filtering functionalities.

table_explorer_runner1.bat (Smart): The recommended launcher for Anaconda/Miniconda users.

table_explorer_runner2.bat (Direct): A simple launcher for users with Python in their system PATH.

⚙️ Configuration & Usage

Option 1: "Smart" Launcher (Recommended for Conda)

Use the file table_explorer_runner1.bat.

This script is ideal if you use Anaconda or Miniconda virtual environments. It automatically detects where Conda is installed on your PC and activates the necessary environment before running the program.

⚠️ Important Setup Step:

Right-click on table_explorer_runner1.bat and select Edit.

Find the line that says:

set "ENV_NAME=JIP_env"


Change JIP_env to the name of the virtual environment where you have installed the required libraries (pandas, pyqt5).

Save and close. You are now ready to double-click and run!

Option 2: "Direct" Launcher

Use the file table_explorer_runner2.bat.

Use this script if you have a standard Python installation and the python command is already configured in your Windows PATH. Simply run the script, and it will open the tool using your default Python interpreter.

Manual Execution (Terminal)

If you prefer using the command line on any operating system (Windows/Linux/Mac):

python table_explorer.py


📦 Requirements

Python 3.x

Pandas

PyQt5

Installing Dependencies

If you haven't installed the libraries in your environment yet:

pip install pandas pyqt5


Credits

Author: JIP
Co-developed with AI assistance: Google Gemini 3.0 PRO

This project was developed to streamline scientific workflows, allowing for fast and efficient tabular data exploration without the overhead of heavy spreadsheet software.