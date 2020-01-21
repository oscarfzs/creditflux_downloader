import time
import threading
import traceback
import os

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


def func(names, dl_folder, thread_name='Thread'):
    page = ExtractDataPage(temp_folder=dl_folder, verbose=False)

    for n in tqdm(names, desc=thread_name):
        try:    
            path = './Downloads/%s.xlsx' % n
            page.download(dest=path, CLO=n, results='Holdings', 
                            dateRange=['1','1999','1','2020'])
        except:
            with open('./logs/log.txt', 'a') as f:
                f.write(traceback.format_exc())
            
            try:
                os.remove(path)
            except:
                pass


    
    page.driver.quit()
                


def run(file, num_threads=4):
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
