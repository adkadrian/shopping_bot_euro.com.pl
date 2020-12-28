# Selenium
# https://sites.google.com/a/chromium.org/chromedriver/downloads
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

#########################################################################
# 							DEFINE FUNCTIONS							#
#########################################################################

# define login fuction to pass username and password and click login button
def log_in(login, password):
	field_username = WebDriverWait(driver, 5).until(
		EC.presence_of_element_located((By.ID, "j_username"))
		)

	field_password = WebDriverWait(driver, 5).until(
		EC.presence_of_element_located((By.ID, "j_password"))
		)

	button_login = WebDriverWait(driver, 5).until(
		EC.presence_of_element_located((By.CLASS_NAME, "selenium-O-login-button"))
		)

	field_username.send_keys(login)
	field_password.send_keys(password)
	button_login.click()

# define check_prize function to compare product price with expected
# if product_prize is equal or less than expected function returns True else False
def check_price(price, time):
	product_price = WebDriverWait(driver, 5).until(
		EC.presence_of_element_located((By.CLASS_NAME, "product-price"))
		)

	refresh_time = None
	
	if time > 0:
		refresh_time = time
	else:
		refresh_time = None

	product_price = product_price.get_attribute('innerHTML')

	product_price = re.findall('[1-9]+\.?[1-9]{2}?', product_price)[0]

	is_price_ok = False
	print(is_price_ok)

	if float(product_price) <= price:

		is_price_ok = True
		return is_price_ok

	elif float(product_price) > price and refresh_time is not None:
		
		while is_price_ok != True:
			
			if float(product_price) <= price:

				is_price_ok = True

			elif is_price_ok != True:

				time.sleep(refresh_time)
				driver.refresh()
	else:
		return is_price_ok

# define fuction to add product to cart
def add_to_cart():
	button_add_to_cart = WebDriverWait(driver, 5).until(
		EC.presence_of_element_located((By.XPATH, "//div/button[@class='add-product-to-cart js-add-product-to-cart']"))
		)

	driver.execute_script("arguments[0].click();", button_add_to_cart)


# define function which will choose warranty type
def choose_warranty(warranty_type):

	if warranty_type == None:
		btn_warranty_next = WebDriverWait(driver, 5).until(
			EC.presence_of_element_located((By.XPATH, "//form/div[@class='warranty-actions']/button[@title='Dalej']"))
			)

		time.sleep(1)
		driver.execute_script("arguments[0].click();", btn_warranty_next)

	btn_next = WebDriverWait(driver, 5).until(
		EC.presence_of_element_located((By.XPATH, "//div[@class='product-button']/a"))
		)
	
	time.sleep(1)
	driver.execute_script("arguments[0].click();", btn_next)

# define function to choose delivery mathod
def choose_delivery_method(delivery_method):

	if delivery_method == 'curier':

		btn_delivery = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "//li[@id='HOME-delivery']/div[@class='input']"))
			)

		driver.execute_script("arguments[0].click();", btn_delivery)

# define order function to click order button and login
def order(username, password):

	btn_order = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.XPATH, "//div[@class='navigate-error']/a[@class='dalej btn btn-second selenium-O-next-button']"))
		)	
	
	driver.execute_script("arguments[0].click();", btn_order)

	log_in(username, password)


#########################################################################
# 							MAIN PROGRAM								#
#########################################################################


##################### VARIABLES #########################################

# define path to the web browser driver
PATH = "/home/adk/Documents/chromedriver"
driver = webdriver.Chrome(PATH)

# replace "login" by your login
login = "login"
# replace "**************" by your password
password = "**************"

# define home url and product category and name
home_url = "https://www.euro.com.pl/"

# prooduct category from url 
product_category = "opaski-monitorujace-aktywnosc/"
# product name from url
product_name = "xiaomi-opaska-mi-band-5-xiaomi.bhtml"
product_url = home_url + product_category + product_name

# define expected product prize
product_price = 140

# set refresh time when product price is to high
refresh_time = 0

# set warranty type from values [None, '', '']
warranty_type = None

# set delivery_method from values ['curier', '', '']
delivery_method = 'curier'


##################### LOGIC #########################################

# open browser on product web page
driver.get(product_url)

# check if product price is equal or less than expected
is_price_ok = check_price(product_price, refresh_time)

# add product to cart if price is good
if is_price_ok:
	add_to_cart()
	choose_warranty(warranty_type)
	choose_delivery_method(delivery_method)
	order(login, password)
else:
	webdriver.exit()