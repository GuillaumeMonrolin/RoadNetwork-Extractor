# RoadNetwork Exctractor

This software is a road network generator for wood laser engraving.

# How to use software with Bash/Batch files helper 
## Install
### Windows
Double click on the .BAT file `install_windows.bat`

### Unix
Execute `./install_unix.sh`
You may add permissions to this file to execute it with the command `chmod 755 install_unix.sh`

## Start App
### Windows
Double click on the .BAT file `start_app.windows.bat`

### Unix 
Execute `./start_app_unix.sh`

# How to use software from terminal

## Installation
### Create a new python virtual environment
``` shell
cd <PROJECT_DIRECTORY>
pip install --upgrade pip
python3 -m pip install --user virtualenv
python -m -venv venv
```

### Install dependencies

#### Windows

```
.\venv\Scripts\activate
python -m pip install -r requirements.txt
```

#### Unix based OS (MacOS or Linux)

```
source venv/scripts/activate
python -m pip install -r requirements.txt
```

## Activate you virtual environment 

### Windows
```
.\venv\Scripts\activate
```

### Unix based OS
```
source venv/scripts/activate
```

## Launch Application
Your virtual environment must be activated.

```
python main.py
```

# How to use the software 