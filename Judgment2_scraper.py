from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from translate import Translator
import sys
from bs4 import BeautifulSoup
import re

class Judgments(object):
	def __init__(self,target):
		self.judgment_search(target)
		
	def split(self,target):
		split_name = []
		split_name = target.split(" ")
		return split_name

	def translate(self,target):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		
		#Variables section
		translate_name = []
		split_name = self.split(target)
		translator = Translator(to_lang="iw")

		for name in split_name:			
			translation = translator.translate(name)
			translate_name.append(translation) 
		
		return translate_name

	def judgment_search(self,target):
		translate_name = self.translate(target)
		driver = webdriver.Firefox()
		driver.get("http://www.takdin.co.il/Search/?RestoreModel=True") #israeli judgments website

		elem = driver.find_element_by_id("WordsPanel.AllWords[0]")
		elem.send_keys("\"")
		for name in translate_name:
			elem.send_keys(name + " ")
		elem.send_keys(Keys.BACK_SPACE)
		elem.send_keys("\"")

		elem = driver.find_element_by_id("search-form-button")
		elem.send_keys(Keys.RETURN)
		driver.quit()

		profile_html = driver.page_source.encode('utf-8')
		soup = BeautifulSoup(profile_html,"lxml")
		self.source_parser(soup)

	def source_parser(self,soup):
		# content = re.findall('<ol>(.*?)<div class="ad">',soup)
		f = open("/var/www/cgi-bin/History/judgment_scrapper.html",'w') # path for the caller function
		f.write("<div id='jud'><h2>Associated judgment</h2>\n")
		
		doc_list = soup.find_all('li')
		for doc in doc_list:
			f.write(doc)
		f.write("</div>")
		f.close()	

