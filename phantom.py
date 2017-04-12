import os
import sys
import time
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def wait_for(driver,indicator,case):
	if case == 'ID':
		failures = 0
		while True:
			try:
				driver.find_element_by_id(indicator)
				return True
			except:
				time.sleep(.5)
				failures += 1
				if failures == 60:
					return False
	elif case == 'TAG':
		failures = 0
		while True:
			try:
				driver.find_element_by_tag_name(indicator)
				return True
			except:
				time.sleep(.5)
				failures += 1
				if failures == 60:
					return False
	elif case == 'CLASS':
		failures = 0
		while True:
			try:
				driver.find_elements_by_class_name(indicator)
				return True
			except:
				time.sleep(.5)
				failures += 1
				if failures == 60:
					return False
	elif case == 'XPATH':
		failures = 0
		while True:
			try:
				driver.find_elements_by_xpath(indicator)
				return True
			except:
				time.sleep(.5)
				failures += 1
				if failures == 60:
					return False

# https://www.mathworks.com/matlabcentral/fileexchange/?page=1&term=type%3AFunction
matlab_url = "https://www.mathworks.com/matlabcentral/fileexchange/?page={0}&term=type%3AFunction"
login = "https://www.mathworks.com/login?uri=https%3A%2F%2Fwww.mathworks.com%2Fmatlabcentral%2Ffileexchange%2F%3Fterm%3Dtype%253AFunction&form_type=community"
dl_dir = '/path/to/Matlab_Downloads/'

display = Display(visible=0, size=(800, 600))
display.start()

chrome_options = webdriver.ChromeOptions()
dl_location = os.path.join(os.getcwd(), dl_dir)

prefs = {"download.default_directory": dl_location}
chrome_options.add_experimental_option("prefs", prefs)
chromedriver = "/path/to/chromedriver"
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)

driver.set_window_size(800, 600)
driver.get(login)

# allows access to dynamic elements in iframe
if not wait_for(driver, 'iframe','TAG'):
	print "Unable to login... Can't locate iframe"
driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
print('this far')
# enter login credentials
if not wait_for(driver, 'userId','ID'):
	print "Unable to login..."
x = driver.find_element_by_id('userId')
print(x)
driver.find_element_by_id('userId').send_keys('*********')
driver.find_element_by_id('password').send_keys('*********')
driver.find_element_by_id('submit').click()
time.sleep(10)
print('this far')
# switch back to html default
driver.switch_to.default_content()
f = open('missed.txt','w')
TOTAL_PAGES = 446
current_page = int(sys.argv[1])
index = 50
while current_page < TOTAL_PAGES:
	while index < 50:
		if not wait_for(driver,'tbody','TAG'):
			index += 1
			continue 
		table_body = driver.find_elements_by_tag_name('tbody')
		list_of_trs = table_body[0].find_elements_by_tag_name('tr')

		tr = list_of_trs[index]
		file_info = tr.find_elements_by_class_name('file_info')[0]
		file_title = file_info.find_elements_by_class_name('file_title')[0]
		link = file_title.find_elements_by_tag_name('a')[0]

		# navigate to download page
		link.click()

		if not wait_for(driver, '//a[@href]','XPATH'):
			driver.back()
			index += 1
			continue
		elems = driver.find_elements_by_xpath("//a[@href]")
		for elem in elems:
			link_text = elem.get_attribute("href")
			if link_text.endswith('zip'):
				try:
					elem.click()
					print(current_page,index,link_text)
				except:
					f.write(str(current_page) + " " + str(index) + ' ' + link_text)

		# navigate back to page of links
		driver.back()
		time.sleep(4)
		index += 1
	current_page += 5
	driver.get(matlab_url.format(current_page))
	index = 0
	
f.close()
driver.close()
display.stop()

print("Exiting ...")
