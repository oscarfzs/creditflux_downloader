**Table of Contents** 
- [Installation](#installation) 
  - [Installing Python](#installing-python)
  - [Installing Prerequisites](#installing-prerequisites)
  - [Installing Chromedriver](#installing-chromedriver)
- [Usage](#usage)
  - [Intro](#intro)
  - [Quick Start](#quick-start)


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

## Usage ##

#### Intro ####

The page from which we download the CLO excel data is encapsulated in the ExtractDataPage class. ExtractDataPage is a class which contains an instance of the Selenium Webdriver (running off of chromedriver). It also contains several Webdriver elements which represent some of the elements on the webpage. These elements can be interacted with using different ExtractDataPage object methods that can choose an option from the dropdown selection, enter the name of a CLO deal into the corresponding field, or download the excel data from the website. 

[](./pictures/extract_data_page_annotated.png?raw=true "annotated")


#### Quick Start #####

The quickest way to download excel sheets from the site is within Python's interactive mode. While inside the application folder, open up Terminal or Command Prompt and type `python -i main.py`, which will display the following:

```
$ python -i main.py
>>> 
```

First create an ExtractDataPage object:

```
>>> page = ExtractDataPage()
Connecting to https://cloi.creditflux.com/ExtractData...
Loading cookies...
Identifying filter elements...
>>>
```

To download all the results for a given CLO, invoke the `download()` method like so:

```
>>> page.download('Aurium CLO II')
Downloading Holdings...
Downloading Test Results...
Downloading Tranches...
Downloading Distributions...
Downloading Purchase/sale...
>>> 
```

By default, calling `page.download('CLO_DEAL_NAME')` will download *all* the data for that CLO, including Test Results, Tranches, Distributions, Holdings, and Purchase/sale, from the earliest record date to the present date, and the output is a single excel file with a separate sheet for each of the previously mentioned categories. The excel file will be placed within the `/Downloads` folder. To change the download location, use the function argument `dl_loc`:

```
>>> page.download('Aurium CLO II', dl_loc='/path/to/folder')
````


