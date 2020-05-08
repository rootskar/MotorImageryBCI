# Motor Movement and Imagery BCI
Brain-Computer Interface for motor movement and imagery experiments developed as Bachelor's thesis by Karel Roots

# Requirements

1.) Windows 10 or Linux (only classifier experiments) with 64-bit Python version 3.7.7 with pip.

2.) To run experiments with the BCI application Emotiv EPOC 2014 device (https://www.emotiv.com/files/Emotiv-EPOC-Product-Sheet-2014.pdf) is required.

3.) Dependencies installed separately or using the virtual environment installation instructions: 

* Tensorflow 2.1.0
* PyQT5 5.9.2
* SciKit-learn 0.22.1
* SciPy 1.4.1
* Numpy 1.18.1
* mlxtend 0.17.2
* statsmodels 0.11.1
* pyEDFlib 0.1.17

# Installation Instructions

For Windows you can try running "install.bat" file in the project root folder.

However, if this doesn't work you can try creating the virtual environment manually with the following steps:

## Create new virtual environment
1.) In Windows open up command prompt (cmd.exe)

2.) Navigate to the project folder with command: cd /path/to/project

3.) Create the virtual environment with command: python -m venv venv

4.) Activate the virtual environment with command: venv\Scripts\activate.bat

5.) Install the requirements with command: pip install -r requirements.txt

6.) Install pyEDFlib (needs to be installed separately) with command: pip install pyedflib==0.1.17

NB! After virtual environment is installed you need to activate the virtual environment every time you open a new command prompt window and want to run the BCI application or the classifier experiments.

# Running the BCI application
1.) You can run the application by running the "run.bat" file in the project-root/BCI folder

If the run.bat method does not work you try manually by following the steps:

1.) Open up command prompt and navigate to the project root folder with command: cd /path-to-project/

2.) Activate the virtual environment with command: venv\Scripts\activate.bat

3.) Navigate to the BCI folder with command: cd BCI

4.) Run the BCI application with command: python main.py

## BCI application options

* Current subject ID - This should be the id of the subject performing the experiment. The ID is used to associate the subject when saving the transfer learning models and statistics

* Number of tasks to perform - This is the number of tasks that will be shown to the subject during the experiment. If the number is even, the subject will be shown equal amount of left and right hand tasks.

* Run type - This is the experiment type to be used during the experiment (executed or imagined tasks)

* Classifier model - This is the primary classifier model used to perform predictions and to re-train the model with transfer learning

* Show predictions - If this option is enabled, the user is shown the result of the prediction after each task

* Enable transfer learning - If this option is enabled, the chosen model weights will be updated with transfer learning method. That means all the data collected during the experiment will be used to re-train the chosen model and the model will be saved in a separate file.

* Evaluate all models - If this option is enabled, all classifier models that are loaded by the application are evaluated (in addition to the primary classifier that is chosen) and the statistics are saved for all models. If the "enable transfer learning" option is also checked, then all models are also used for transfer learning.

* Enable debug mode - If this option is enabled then EEG data is randomly generated and the Emotiv EPOC device is not used. This is useful for testing the application without any device connected.

# Running the classifier experiments
You can run the classifier experiments with default options by running the "run.bat" file in the project-root/classifier folder

If the run.bat method does not work or you want to specify custom options you can try manually running by following the steps:

1.) Open up command prompt and navigate to the project root folder with command: cd /path-to-project/

2.) Activate the virtual environment with command: venv\Scripts\activate.bat

3.) Navigate to the classifier folder with command: cd classifier

4.) Run the classifier experiments with command: python run_experiments.py 109 100 2 1 True

## Classifier experiments options
The classifier experiments have to be run with 5 required arguments in the following order:

1.) The number of subjects to be used from the dataset (integer)

2.) The number of epochs the training of models should be done (integer)

3.) The number of target classes in the classification (integer)

4.) What type of trials should be extracted from the data (1 or 2, where 1 => executed trials only and 2 => imagined trials only)

5.) If CPU-only mode should be used (True / False). Note that for GPU mode you will need to have CUDA installed.

# Running the application in Linux environment
Requirements: 64-bit Python 3.7.7 (sudo apt-get install python3.7) and python3-venv (sudo apt-get install python3-venv python3.7-venv)

If you want to run the progams in Linux environment you will first have to create a virtual environment for Linux.

You can try running the install script: ./install.sh

However in case the install script does not work you can try installing manually with the following steps:

1.) Create virtualenv in the project folder with command: python3 -m venv env

2.) Activate virtual environment with command: source env/bin/activate

3.) Install wheel with (if not installed): pip install wheel

4.) Install dependencies with command: pip install -r requirements.txt (OR "pip3 install -r requirements.txt" if running Ubuntu or Fedora)

5.) Install pyedflib with command: pip install pyedflib==0.1.17 (OR "pip3 install -r requirements.txt" if running Ubuntu or Fedora)

## Running BCI application in Linux:

The BCI application is not supported in Linux environment due to the latest version of CyKIT EEG streaming library not being supported in Linux.

## Running the classifier experiments in Linux:

1.) Navigate to the classifier folder with: cd classifier

2.) Run the classifier experiments with: ./run.sh

If the run.sh script does not work or you want to specify custom options you can try manually running by following the steps:

1.) Navigate to the classifier folder with command: cd classifier

2.) Run experiments with command: python3 run_experiments.py 109 100 2 1 True
