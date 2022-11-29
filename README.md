# Presentation
  OSLiFe-DiSC is an open source tool that allows users to Discover open source licenses features, Select open source licenses based on features and compare open source licenses by showing the common features and the different ones. The goal is to make open source licenses easier to understand and to pick-up for open source software.
  
  For more information please refer to the research papers about open source licenses features and the OSLiFe-DiSC tool.
  

# Requirements
You need to have python and MySQL server installed on your computer.
You need a database named oslicenses to be loaded on MySQL server.

# Get Started guide

## Step 1: install Python interpreter and MySQL
1- Download and install Python interpreter 3.10 or later from the official Website (https://www.python.org/downloads/release/python-3106/)
   - Run the following command to ensure that pip (Python packages installer) is installed.
   python -m pip install --upgrade pip

2- Download and install MySQL Server 8.0 or later from the official Website
   (https://dev.mysql.com/downloads/installer/)

## Step 2: get a copy of OSLiFe-DiSC source code
1- Clone the project on your personal computer using git,
or

1- Download and unzip source code of OSLiFe-DiSC (OSLiFe-DiSC V1.0 Source Code.zip file) on your personal computer.

## Step 3: install required packages
Required packages for the tool: (connection / mysqlclient)
- Flask
- anytree
- bs4
- mysql-connector-python
- requests
- waitress 

To install these packages either:

1- Run the command  pip install <package_name>, or

1- Install PyCharm from the official Website (https://www.jetbrains.com/pycharm/download/)
   - open the tool project (source files)
   - Click File > Settings > Python Interpreter  
     "Add interpreter" on the right side to set the python interpreter for the project
	 "+" on the left side to add each project 

## Step 4: copy the data
1- Get the path to datab folder with the tool source folder and run the following command:
"mysql -u root -p oslicenses < <path_to>osls.sql"  

2- Either modify the password for the MySQL connection on the connection.py file to your set password, or 
   set the password "Osl123disc" for the root.

## Step 5: Run OSLiFe-DiSC
1- Run python oslf.py, or

1- Run the file using pyCharm
