# Motor Movement and Imagery BCI
Brain-Computer Interface for motor movement and imagery experiments developed as Bachelor's thesis

# Installation and Run Instructions

## Activate virtual environment
1.) In Windows open up command prompt (cmd.exe)

2.) Navigate to the project folder with command: cd /path/to/project

3.) Activate the virtual environment with command: venv\Scripts\activate.bat

## Running the application
1.) While still in the same command prompt window from the previous step move to the "BCI" folder with command: cd BCI

2.) Run the BCI application with command: python main.py

## Running the classifier experiments
1.) If you are in the BCI folder navigate back to the root folder with command: cd ../classifier

2.) Otherwise navigate to the classifier folder with command: cd classifier

3.) Run the classifier experiments with command: python run_experiments.py 109 100 2 1 True

# Classifier experiments options
The classifier experiments have to be run with 5 required arguments in the following order:

1.) The number of subjects to be used from the dataset (integer)

2.) The number of epochs the training of models should be done (integer)

3.) The number of target classes in the classification (integer)

4.) What type of trials should be extracted from the data (1 or 2, where 1 => executed trials only and 2 => imagined trials only)

5.) If CPU-only mode should be used (True / False). Note that for GPU mode you will need to have CUDA installed.

## Running in Linux enviroment
Requirements: Python 3.7.7

If you want to run the progams in Linux environment you will first have to create a virtual environment for Linux.

1.) Try running the install script: ./install.sh

In case the install script does not work you can try installing manually with the following steps:

1.) Create virtualenv in the project folder with command: python -m venv env (OR python3 -m venv env)

2.) Activate virtual environment with command: source env\bin\activate

3.) Install wheel with: pip install wheel

4.) Install dependencies with command: pip install -r requirements.txt

5.) Install pyedflib with command: pip install pyedflib==0.1.17

After the virtualenv has been installed you can run the BCI application with the following steps:

1.) Navigate to the BCI folder with command: cd BCI

2.) Run BCI app with command: python main.py

And the classifier experiments with the following steps:

1.) Navigate to the classifier folder with command: cd classifier

2.) Run experiments with command: python run_experiments.py 109 100 2 1 True
