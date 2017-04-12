from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# https://www.mathworks.com/matlabcentral/fileexchange/?page=1&term=type%3AFunction
matlab_url = "https://www.mathworks.com/matlabcentral/fileexchange/?page={0}&term=type%3AFunction"
login = "https://www.mathworks.com/login?uri=https%3A%2F%2Fwww.mathworks.com%2Fmatlabcentral%2Ffileexchange%2F%3Fterm%3Dtype%253AFunction&form_type=community"

profile = webdriver.FirefoxProfile()
# setting preferences
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", '/home/jordan/Documents/Matlab_Downloads')
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/zip, none")

# creating driver
driver = webdriver.Firefox(firefox_profile=profile)

# navigate to login page
driver.get(login)

# allows access to dynamic elements in iframe
driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
time.sleep(5)

# enter login credentials
driver.find_element_by_id('userId').send_keys('***********')
driver.find_element_by_id('password').send_keys('***********')
driver.find_element_by_id('submit').click()
time.sleep(10)

# switch back to html default
driver.switch_to.default_content()

# check if we are at the last page of links
def last_page():
	return True

while not last_page():
	index = 0
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
	
time.sleep(2)

driver.quit()
# buttons = []
