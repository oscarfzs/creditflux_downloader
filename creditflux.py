import glob
import os
import shutil
import time
import calendar
from datetime import date

import pickle
import pandas as pd
from retry import retry

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException

def enable_downloads(browser, download_dir):
        #add missing support for chrome "send_command"  to selenium webdriver
        browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        browser.execute("send_command", params)

class ExtractDataPage:
    _EXCEL_MAX_ROWS = 5000
    _download_wait_time = 3

    url = "https://cloi.creditflux.com/ExtractData"

    # Dropdowns
    _dropdown_xpaths = {
                                  'displayType':'//*[@id="displayType"]',
                                  'startMonth':'//*[@id="periodEndDateMonth1"]',
                                   'startYear':'//*[@id="periodEndDateYear1"]',
                                    'endMonth':'//*[@id="periodEndDateMonth2"]',
                                     'endYear':'//*[@id="periodEndDateYear2"]',
    }

    # Filters
    _filter_xpaths = {
                                        'CLO':'//*[@id="dealId_chzn"]',
                                    'manager':'//*[@id="managerId_chzn"]',
                                   'arranger':'//*[@id="arrangerId_chzn"]',
                                    'trustee':'//*[@id="trusteeId_chzn"]',
                             'managerCounsel':'//*[@id="managerCounselId_chzn"]',
                            'arrangerCounsel':'//*[@id="arrangerCounselId_chzn"]',
                                    'CLOTags':'//*[@id="tagId_chzn"]'
    }

    _filter_selection_xpaths = {
                                        'CLO':'//*[@id="dealId_chzn"]/div/ul',
                                    'manager':'//*[@id="managerId_chzn"]/div/ul',
                                   'arranger':'//*[@id="arrangerId_chzn"]/div/ul',
                                    'trustee':'//*[@id="trusteeId_chzn"]/div/ul',
                             'managerCounsel':'//*[@id="managerCounselId_chzn"]/div/ul',
                            'arrangerCounsel':'//*[@id="arrangerCounselId_chzn"]/div/ul',
                                    'CLOTags':'//*[@id="tagId_chzn"]/div/ul'
    }

    # Download Button
    _element_id_download_button = "excel"

    def __init__(self, 
                dl_folder='./Downloads', 
                temp_folder='./temp', 
                headless=True, 
                verbose=True):
        self._verbose = verbose

        self.driver = self._init_driver(dl_loc=temp_folder, headless=headless)

        self._path_downloads_folder = dl_folder
        self._path_temp_folder = temp_folder

        self.connect()
        self.load_session()
        self.driver.refresh()

        time.sleep(5)

        if self._verbose:
            print("Identifying filter elements...")

        self.display_type = Select(self.driver.find_element_by_xpath(self._dropdown_xpaths['displayType']))
        self.start_month = Select(self.driver.find_element_by_xpath(self._dropdown_xpaths['startMonth']))
        self.start_year = Select(self.driver.find_element_by_xpath(self._dropdown_xpaths['startYear']))
        self.end_month = Select(self.driver.find_element_by_xpath(self._dropdown_xpaths['endMonth']))
        self.end_year = Select(self.driver.find_element_by_xpath(self._dropdown_xpaths['endYear']))

        self.CLO_field = self.driver.find_element_by_xpath(self._filter_xpaths['CLO'])

        self.download_button = self.driver.find_element_by_id(self._element_id_download_button)
        
    def _init_driver(self, dl_loc, headless=True):
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": dl_loc,
                'download.prompt_for_download':"false"
                }
        #'download.directory_upgrade':True,
        if headless:
            options.add_argument("--headless")

        options.add_experimental_option("prefs", prefs)

        return webdriver.Chrome(options=options)
    
    def login(self, login_url):
        if self._verbose:
            print("Logging in with url: %s" % login_url)

        self.driver.get(login_url) 
        self.driver.get(self.url)
        self.save_session()
    
    def connect(self):
        if self._verbose:
            print("Connecting to %s..." % self.url)

        self.driver.get(self.url) 

    def save_session(self, filename="cookies.pickle"):
        if self._verbose:
            print("Saving cookies...")

        cookies = self.driver.get_cookies()

        for c in cookies:
            if 'expiry' in c.keys():
                c['expiry'] = int(c['expiry'])

        with open(filename, 'wb') as file:
            pickle.dump(cookies, file)
        
        file.close()

    def load_session(self, filename="cookies.pickle"):
        if self._verbose:
            print("Loading cookies...")

        with open(filename, 'rb') as file:
            cookies = pickle.load(file)
        
        for c in cookies:
            self.driver.add_cookie(c)

    @retry(ElementClickInterceptedException, tries=4, delay=1, jitter=1)
    def select_CLO(self, name):
        #wait = WebDriverWait(self.driver, 10)
        self.CLO_field.click()
        xpath = self._filter_selection_xpaths['CLO']
        '''
        selection = wait.until(EC.element_to_be_clickable((By.XPATH, 
                                                            xpath +
                                                            '/li[contains(text(), "%s")]' % name)))
        '''
        
        selection = self.driver.find_element_by_xpath(xpath + '/li[contains(text(), "%s")]' % name)

        selection.click()


    def select_date_range(self, dateRange):
        self.start_month.select_by_value(dateRange[0])
        self.start_year.select_by_value(dateRange[1])
        self.end_month.select_by_value(dateRange[2])
        self.end_year.select_by_value(dateRange[3])

    def handle_selections(self, CLO, results, dateRange):
        if CLO != None:
            self.select_CLO(CLO)
        if results != None:
            self.display_type.select_by_visible_text(results)
        if dateRange != None:
            self.select_date_range(dateRange)

    def print_selected_CLOs(self):
        elements = self.driver.find_elements_by_class_name('search-choice')
        print([el.find_element_by_tag_name('span').text for el in elements])
    
    def clear_fields(self):
        self.clear_CLO_field()
        self.driver.find_element_by_xpath('//*[@id="main"]/form/div[1]/div/p[1]/label').click()

    def clear_CLO_field(self):
        elements = self.CLO_field.find_elements_by_class_name('search-choice-close')
        for button in elements:
            button.click()

    """
    Functions for downloading files from the page
    """

    def download(self, 
                CLO=None,
                results='Holdings',
                startMonth='1',
                startYear='1999',
                endMonth=None,
                endYear=None,
                dest=None):

        # Downloads the data for one CLO deal
        # Will automatically check if the first downloaded excel sheet reaches the
        # 5000 line limit that the creditflux website imposes. If so, then it is possible
        # that there is more data yet to be downloaded, and the code will try to find which 
        # date ranges to download from. All the downloaded data for the CLO will then be merged into 
        # one single excel sheet.

        if dest == None:
            dest = self._path_downloads_folder + '/%s.xlsx' % CLO
        
        if endMonth == None or endYear == None:
            current_date = date.today()
            endMonth = str(current_date.month)
            endYear = str(current_date.year)

        dateRange = [startMonth, startYear, endMonth, endYear]
        self.handle_selections(CLO, results, dateRange)
        
        self.download_button.click()

        filepath = self.newest(self._path_temp_folder)

        df = pd.read_excel(filepath, header=[1])

        if len(df) == self._EXCEL_MAX_ROWS:
            oldestDate, trimmed_df = self.trimmed(df)
            newDateRange = dateRange.copy()
            newDateRange[2] = str(oldestDate.month)
            newDateRange[3] = str(oldestDate.year)

            try:
                os.remove(filepath)
            except FileNotFoundError:
                pass

            self._redownload(dest, newDateRange, trimmed_df)
        else:
            shutil.move(filepath, dest)

            try:
                os.remove(filepath)
            except FileNotFoundError:
                pass

            self.clear_fields()

    def _redownload(self, dest, dateRange, old_df):
        self.select_date_range(dateRange)
        self.download_button.click()

        filepath = self.newest(self._path_temp_folder)

        df = pd.read_excel(filepath, header=[1])

        merged_df = self.merged(old_df, df)

        if len(df) == self._EXCEL_MAX_ROWS:
            oldestDate, trimmed_df = self.trimmed(merged_df)
            newDateRange = dateRange.copy()
            newDateRange[2] = str(oldestDate.month)
            newDateRange[3] = str(oldestDate.year)

            try:
                os.remove(filepath)
            except FileNotFoundError:
                pass

            self._redownload(dest, newDateRange, trimmed_df)
        else:
            merged_df.to_excel(dest, index=False)

            try:
                os.remove(filepath)
            except FileNotFoundError:
                pass
            
            self.clear_fields()

    @retry((ValueError, FileNotFoundError), tries=4, delay=2, jitter=1)
    def newest(self, folder):
        list = glob.glob(folder + '/*')
        filepath = max(list, key=os.path.getctime)
        while filepath.find('.crdownload') >= 0:
            time.sleep(1)
            list = glob.glob(folder + '/*')
            filepath = max(list, key=os.path.getctime)

        return filepath
        
    def merged(self, df1, df2, dateColumn='As Of'):
        return pd.concat([df1,df2], ignore_index=True)

    def trimmed(self, df, dateColumn='As Of'):
        N = len(df[dateColumn])
        oldestDate = df[dateColumn][N-1]
        
        return oldestDate, df[df[dateColumn] != oldestDate]






    




