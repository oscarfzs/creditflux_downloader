**Table of Contents** 
- [Installation](#installation) 
  - [Installing Python](#installing-python)
  - [Installing Prerequisites](#installing-prerequisites)
  - [Installing Chromedriver](#installing-chromedriver)


## Installation

#### **Installing Python**

If you already have Python 3.x installed, you may skip this step. However, you should make sure that you have the correct version of Python installed. To check which version of Python you are running, open up Terminal (Mac OS) or Command Prompt (Windows) and type:

```
$ python --version
```

which will display which version you are on (e.g. `$ 3.6.0`). Also check to make sure your version of `pip` is updated and corresponds to the version of Python that you are using. Type `pip --version` to see which version you are on. It should look something like `pip 20.0.1 from path/to/pip (python 3.6)` where `path/to/pip` corresponds to the filepath of wherever pip is located. 

If you do not have Python 3.x installed, download and install from here: 

https://www.python.org/downloads/

#### **Installing Prerequisites**

The following are the prerequisite packages that must be installed in order for the application to work:

```
decorator==4.4.1
et-xmlfile==1.0.1
jdcal==1.4.1
numpy==1.18.1
openpyxl==3.0.3
pandas==0.25.3
py==1.8.1
python-dateutil==2.8.1
pytz==2019.3
retry==0.9.2
selenium==3.141.0
six==1.14.0
tqdm==4.41.1
urllib3==1.25.8
xlrd==1.2.0
```
The names of these packages are located in `requirements.txt`, and they can all be installed using `pip` like so:

```
$ pip install -r requirements.txt
```

#### **Installing Chromedriver**

The Chromedriver is an executable file that mimics an instance of Google Chrome. 

*To install it on Mac OS*, you need to copy the `chromedriver` file into `/usr/bin` or `/usr/local/bin`. This adds the chromedriver to the system's PATH, so that later on a Selenium Webdriver knows where to locate it. To add the file to PATH, open up Terminal while in the application folder and type:

```
$ cp chromedrivers/mac/chromedriver /usr/local/bin
```

*To install it on Windows*, you do not need to move/copy any files. Later on, you will need to give the filepath of the windows chromedriver file to the `ExtractDataPage` object so that the Webdriver can use it.


