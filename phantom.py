import os
import sys
import time
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# https://www.mathworks.com/matlabcentral/fileexchange/?page=1&term=type%3AFunction
matlab_url = "https://www.mathworks.com/matlabcentral/fileexchange/?page={0}&term=type%3AFunction"
login = "https://www.mathworks.com/login?uri=https%3A%2F%2Fwww.mathworks.com%2Fmatlabcentral%2Ffileexchange%2F%3Fterm%3Dtype%253AFunction&form_type=community"
dl_dir = '/home/jordan/Documents/Matlab/Matlab_Downloads/'

display = Display(visible=0, size=(800, 600))
display.start()

chrome_options = webdriver.ChromeOptions()
dl_location = os.path.join(os.getcwd(), dl_dir)

prefs = {"download.default_directory": dl_location}
chrome_options.add_experimental_option("prefs", prefs)
chromedriver = "/home/jordan/Documents/Matlab/Selenium_Drivers/chromedriver"
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)

driver.set_window_size(800, 600)
driver.get(login)
#WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//a[@href="' + filename + '"]')))

# allows access to dynamic elements in iframe
driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
time.sleep(10)

# enter login credentials
driver.find_element_by_id('userId').send_keys('jordanott365@gmail.com')
driver.find_element_by_id('password').send_keys('Jordan1@')
driver.find_element_by_id('submit').click()
time.sleep(10)

# switch back to html default
driver.switch_to.default_content()

# check if we are at the last page of links
def last_page():
	return False

page_num = 1
while not last_page():
	index = 49
	while index < 50:
		table_body = driver.find_elements_by_tag_name('tbody')
		list_of_trs = table_body[0].find_elements_by_tag_name('tr')

		tr = list_of_trs[index]
		file_info = tr.find_elements_by_class_name('file_info')[0]
		file_title = file_info.find_elements_by_class_name('file_title')[0]
		link = file_title.find_elements_by_tag_name('a')[0]

		# navigate to download page
		link.click()
		time.sleep(4)
		elems = driver.find_elements_by_xpath("//a[@href]")
		for elem in elems:
			link_text = elem.get_attribute("href")
			if link_text.endswith('zip'):
				elem.click()
				print(link_text)
		# navigate back to page of links
		driver.back()
		time.sleep(4)
		index += 1
	page_num += 1
	driver.get(matlab_url.format(page_num))
	


driver.close()
display.stop()

print("Exiting ...")