# Motor Movement and Imagery BCI
Brain-Computer Interface for motor movement and imagery experiments developed as Bachelor's thesis by Karel Roots

# Requirements

1.) Windows 10 or Linux with 64-bit Python version 3.7.7 with pip

2.) Dependencies installed separately or using the virtual environment provided with the repo: 

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

# Running the classifier experiments
1.) You can run the application by running the "run.bat" file in the project-root/classifier folder

If the run.bat method does not work you try manually by following the steps:

1.) Open up command prompt and navigate to the project root folder with command: cd /path-to-project/

2.) Activate the virtual environment with command: venv\Scripts\activate.bat

3.) Navigate to the BCI folder with command: cd classifier

4.) Run the classifier experiments with command: python run_experiments.py 109 100 2 1 True

## Classifier experiments options
The classifier experiments have to be run with 5 required arguments in the following order:

1.) The number of subjects to be used from the dataset (integer)

2.) The number of epochs the training of models should be done (integer)

3.) The number of target classes in the classification (integer)

4.) What type of trials should be extracted from the data (1 or 2, where 1 => executed trials only and 2 => imagined trials only)

5.) If CPU-only mode should be used (True / False). Note that for GPU mode you will need to have CUDA installed.

# Running the application in Linux environment
Requirements: 64-bit Python 3.7.7 and python3-venv (sudo apt-get install python3-venv)

If you want to run the progams in Linux environment you will first have to create a virtual environment for Linux.

You can try running the install script: ./install.sh

However in case the install script does not work you can try installing manually with the following steps:

1.) Create virtualenv in the project folder with command: python3 -m venv env

2.) Activate virtual environment with command: source env/bin/activate

3.) Install wheel with (if not installed): pip install wheel

4.) Install dependencies with command: pip install -r requirements.txt (OR "pip3 install -r requirements.txt" if running Ubuntu or Fedora)

5.) Install pyedflib with command: pip install pyedflib==0.1.17

After the virtualenv has been installed you can start the BCI application with the following steps:

1.) Navigate to the BCI folder with: cd BCI

2.) Run the application with: ./run.sh

If the run.sh script does not work you can try to run the application manually with the following steps:

1.) In the project root folder activate virtual environment with command: source env/bin/activate

2.) Navigate to the BCI folder with command: cd BCI

3.) Run BCI app with command: python3 main.py

And the classifier experiments with the following steps:

1.) Navigate to the BCI folder with: cd classifier

2.) Run the classifier experiments with: ./run.sh

If the run.sh script does not work you can try to run the application manually with the following steps:

1.) Navigate to the classifier folder with command: cd classifier

2.) Run experiments with command: python3 run_experiments.py 109 100 2 1 True
