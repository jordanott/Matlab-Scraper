# Matlab-Scraper  

Webscraper to download all function files from [MathWorks File Exchange](https://www.mathworks.com/matlabcentral/fileexchange/?page=1&term=type%3AFunction)  
### Requirements ###  
#### Selenium & VirtualDisplay ####
```
$ pip install selenium
$ sudo apt-get install xvfb xserver-xephyr vnc4server
$ sudo pip install pyvirtualdisplay
```

#### Install Drivers ####
[Chrome Driver](https://sites.google.com/a/chromium.org/chromedriver/downloads)  
[Firefox Driver](https://github.com/mozilla/geckodriver/releases)  

### About ###
* [matlab_scraper.py](https://github.com/jordanott/Matlab-Scraper/blob/master/matlab_scraper.py) uses a Firefox webdriver to scrape the Matlab site  
* [phantom.py](https://github.com/jordanott/Matlab-Scraper/blob/master/phantom.py) uses a headless Chrome webdriver to scrape the Matlab site  
