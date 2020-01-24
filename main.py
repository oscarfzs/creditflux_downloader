import glob
import time
import threading
import traceback
import os
from argparse import ArgumentParser

from tqdm import tqdm

from creditflux import ExtractDataPage
from creditflux import enable_downloads

path_downloads_folder = "./Downloads"
path_chromedrivers_folder = "./chromedrivers"
path_logs_folder = "./logs"
path_temp_folder = "./temp"

path_thread_temp_folder = ["./threading/thread%d" % i for i in range(1,5)]

def clear_logs():
    list = glob.glob(path_logs_folder + '/*')
    for filepath in list:
        with open(filepath, 'w') as f:
            f.write('')

def func(names, args):
    page = ExtractDataPage(dl_folder=args['dl_folder'], temp_folder=args['temp_folder'], verbose=False)

    for deal_name in tqdm(names, desc=args['thread_name']):
        try:   
            path = './Downloads/%s.xlsx' % deal_name
            page.download(deal_name, results=args['results'], dest=path)
        except:
            with open('./logs/errors', 'a') as f:
                f.write(traceback.format_exc())
            
            with open('./logs/failed', 'a') as f:
                f.write(deal_name + '\n')
            
            try:
                os.remove(path)
            except:
                pass

    page.driver.quit()
                


def download_multiple(file, 
                    results='all',
                    num_threads=2,
                    dl_folder='./Downloads'
                    ):
    if num_threads > 4:
        print("Error: Thread count may not exceed 4")

    startTime = time.time()

    with open(file, 'r') as f:
        names = [l.rstrip('\n') for l in f]
    
    subset = []
    for i in range(num_threads):
        subset.append([])

    for i in range(len(names)):
        subset[i % num_threads].append(names[i])
    

    threads = []
    for i in range(num_threads):
        args = {}
        args['results'] = results
        args['num_threads'] = num_threads
        args['thread_name'] = "Thread%d" % (i+1)
        args['temp_folder'] = path_thread_temp_folder[i]
        args['dl_folder'] = dl_folder
        t = threading.Thread(target=func, args=(subset[i], args,))
        threads.append(t)
    
    for t in threads:
        t.start()

    for t in threads:
        t.join()


    endTime = time.time()
    runTime = endTime - startTime

    print("Completed in %d seconds" % runTime)

def clear_folder(folder):
    pass