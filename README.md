**Installing Packages**

There are several python packages to install, which can be done by opening up Terminal while in the application folder and typing:

```
$ pip install -r requirements.txt
```


**Installing Chromedriver**

The Chromedriver is an executable file that mimics an instance of Google Chrome. To install it, you need to copy the `chromedriver` file into `/usr/bin` or `/usr/local/bin`. To do so, open up Terminal while in the application folder and type:

```
$ cp chromedrivers/mac/chromedriver /usr/local/bin
```

To download a list of deals, open up the Python Interpreter:

```
$ python3 -i main.py

Python 3.7.1 (default, Dec 14 2018, 13:28:58) 
[Clang 4.0.1 (tags/RELEASE_401/final)] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

Type the following:

```
>>> run('names/names_20.txt', num_threads=3)
```

This will start three threads that will start downloading the listed deals in the file `names/names_20.txt`. You can use any text file that contains deal names separated by newline characters.

```
>>> run('names/names_20.txt', 3)
Thread 2:   0%|                                                                                    | 0/7 [00:00<?, ?it/s]
Thread 1:   0%|                                                                                    | 0/7 [00:00<?, ?it/s]
Thread 3:   0%|                                                                                    | 0/6 [00:00<?, ?it/s]
```

If any errors/exceptions are encountered along the way, they will be written to the file `logs/errors`, and the deal names which are not downloaded will be listed in `logs/failed`.
