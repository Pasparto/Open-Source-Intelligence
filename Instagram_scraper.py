from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import urllib
from pprint import pprint
import re
from time import gmtime, strftime
import os

class Instagram(object):
	def __init__(self,target):		
		self.search_target(target)
	

	#parse the url list to name
	def name_parser(self,urls):
		names = []
		for name in urls:
			name = re.findall("n/(.*?)$",name)
			names.append(name)
		return names

	#search the target and collect the urls
	def search_target(self,target):
		driver = webdriver.Firefox()
		driver.get("http://websta.me/search/" + target)	
		
		elem = driver.find_elements_by_class_name("username")
		elem2 = driver.find_elements_by_class_name("profimg")
		

		#list of profiles link
		urls = []		
		for link in elem:
			urls.append(link.get_attribute('href'))
		
		driver.close()
		
		
		src_list = self.get_img(elem2)
		self.print_users(urls,src_list)

	#print list of usrs and open the chosen profile
	def print_users(self,urls,src_list):		
		f = open("/var/www/cgi-bin/History/instagram_scrapper.html",'w')
		html = '<div id="instagram" class="hid">\n<h1>Instagram</h1>\n'
		f.write(html)
		names = self.name_parser(urls)
		f.write("<h2>Please select user to watch his profile :</h2>\n") 
		counter = 1
		if not names:
			f.write('<h3>Sorry, No result on this target on Instagram</h3>\n')
		else:
			for name in names:
				f.write('<img src="' + src_list[counter - 1] + '">\n')
				f.write("<li>" + str(counter) + ".\t" + str(name)[3:-2] + "</li>\n")
				f.write('<a href="' + urls[counter - 1] + '">Profile Link</a>\n')
				f.write('<br>') 
				counter += 1
		f.close()

	def get_img(self,elem):
		src_list = []
		for src in elem:
			# print src.get_attribute('src')
			# urllib.urlretrieve(src.get_attribute('src'))
			src_list.append(src.get_attribute('src'))
		return src_list
