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

path_thread1_temp_folder = "./threading/thread1"
path_thread2_temp_folder = "./threading/thread2"
path_thread3_temp_folder = "./threading/thread3"
path_thread4_temp_folder = "./threading/thread4"


def func(names, temp_folder, thread_name='Thread'):
    page = ExtractDataPage(temp_folder=temp_folder, verbose=False)

    for deal_name in tqdm(names, desc=thread_name):
        try:   
            path = './Downloads/%s.xlsx' % deal_name
            page.download(deal_name, dest=path)
        except:
            with open('./logs/errors', 'a') as f:
                f.write(traceback.format_exc())
            
            with open('./logs/failed', 'a') as f:
                f.write(deal_name)
            
            try:
                os.remove(path)
            except:
                pass

    page.driver.quit()
                


def run(file, num_threads=3):
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
        t = threading.Thread(target=func, args=(subset[i], 
                                                './threading/thread%d' % (i+1), 
                                                'Thread %d' % (i+1))
        )
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