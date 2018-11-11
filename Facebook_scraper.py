###############################################
#			Facebook Search Script #
#				written by Matan .R.  #
###############################################
from bs4 import BeautifulSoup
import re
from pprint import pprint
import os
import sys
# import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from bottle import static_file


#hebrew
reload(sys)
sys.setdefaultencoding('utf-8')

class Facebook(object):
	def __init__(self,email):		
		soup,driver,flag = self.login(email)
		if flag == 1:
			driver.quit()			
			f = open("/var/www/cgi-bin/History/Facebook_scrapper.html",'w')
			html = '<div id="facebook" class="col1">\n<h1> Facebook </h1>\n'
			f.write(html)
			f.write('<font size="3" color="red">The Email you enter may not linked to any Facebook Account ! \n </div>') #This is the closest result.</font>
			f.close()
		else:	
			self.img_parser(soup,flag)
			self.place_parser(soup)
			self.birthday_parser(soup)
			self.phone_parser(soup)
			self.gender_parser(soup)
			self.relationship_parser(soup)
			self.likes_perser(driver)
		# self.print_html()
		
	#like parser
	def likes_perser(self,driver):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		f = open("/var/www/cgi-bin/History/Facebook_scrapper.html",'a')

		# get likes
		try:
			elem = driver.find_element_by_xpath("//a[contains(.,'Likes')]")
			elem.send_keys(Keys.RETURN)
			like_html = driver.page_source.encode('utf-8')
			like_soup = BeautifulSoup(like_html,"lxml")
			# likes = []
			likes = like_soup.find_all('span')
			f.write("</div><div class='col2'><h2>Likes : </h2>\n")
			for like in likes:
				f.write("<li>" + str(like) + "</li>\n")		
			f.write("</div>\n")
		
		except:
			f.write("<div class='col2'><h2>Likes :</h2> No likes found</div>\n")

		driver.quit()
		f.close()
		
	


	#alt parse
	def img_parser(self,soup,flag):
		reload(sys)
		sys.setdefaultencoding('utf-8')		
		f = open("/var/www/cgi-bin/History/Facebook_scrapper.html",'w')
		html = '<div id="facebook" class="col1">\n<h1> Facebook </h1>\n'
		f.write(html)		
		about_lst = []
		img_list = soup.find_all('img')
		for img in img_list:		
			if re.findall('alt="(.*?)"',str(img)):
				parse = re.findall('alt="(.*?)"',str(img))
				for i in parse:
					i = unicode(i,"utf-8")
					about_lst.append(i)
		
		img = str(img_list[1])
		img = re.sub(r'height="(.*?)"','',img)
		img = re.sub(r'width="(.*?)"','',img)
		img = re.sub(r'class="(.*?)"','class="profile"',img)
		f.write(img) 

		f.write("<div><h2>Name : </h2>" + str(about_lst[1]) + "</div>\n")
		f.write("<div><h2>Work Education & Family : </h2>")
		for i in about_lst[2:]:
			f.write("<p>" + i + "</p>")
		f.write("</div>")
		f.close()

	

	#place parse
	def place_parser(self,soup):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		f = open("/var/www/cgi-bin/History/Facebook_scrapper.html",'a')
		place = re.findall('Current City(.*?)</a>',str(soup),re.MULTILINE)
		place_parse = re.findall('>\D+$',str(place),re.MULTILINE)
		if place_parse:
			f.write("<div><h2>Lives in : </h2>" + str(place_parse)[3:-4] + "</div>\n")
			# return place_parse[0]
		else:
			f.write("<div><h2>Lives in : </h2> No place found</div>\n")
		f.close()

	


	#Birthday
	def birthday_parser(self,soup):
		f = open("/var/www/cgi-bin/History/Facebook_scrapper.html",'a')
		birth = re.findall('Birthday(.*?)</tr>',str(soup),re.MULTILINE)
		birth_temp = re.findall('>(.*?)</div></td>',str(birth),re.MULTILINE)
		try:
			birth_parse = re.findall('>.*?$',str(birth_temp[1]),re.MULTILINE)
			f.write("<div><h2>Birthday : </h2>" + str(birth_parse)[3:-2] + "</div>\n")
		except:
			f.write("<div><h2>Birthday : </h2> No birthday found</div>\n")
		f.close()
		


	

	#phone parser
	def phone_parser(self,soup):
		reload(sys)
		sys.setdefaultencoding('utf-8')
		f = open("/var/www/cgi-bin/History/Facebook_scrapper.html",'a')
		phone = re.findall('\d+-\d+-\d+',str(soup),re.MULTILINE)
		if phone:
			f.write("<div><h2>Phone number : </h2>" + str(phone) + "</div>\n")
		else:
			f.write("<div><h2>Phone number : </h2> No phone found</div>\n")
		f.close()


	


	#Gender parser
	def gender_parser(self,soup):
		f = open("/var/www/cgi-bin/History/Facebook_scrapper.html",'a')
		gender = re.findall('Gender(.*?)</div></td></tr>',str(soup),re.MULTILINE)
		gender = str(gender)
		gender_parse = re.findall("(Male|Female)",gender,re.MULTILINE)
		if gender_parse:
			f.write("<div><h2>Gender : </h2>" + str(gender_parse)[2:-2] + "</div>\n")
		else:
			f.write("<div><h2>Gender : </h2> No gender found</div>\n")
		f.close()

	

	#Relationship parser
	def relationship_parser(self,soup):	
		reload(sys)
		sys.setdefaultencoding('utf-8')
		f = open("/var/www/cgi-bin/History/Facebook_scrapper.html",'a')
		if (re.findall('In a relationship',str(soup))):
			rs = re.findall('In a relationship',str(soup))
			name_parse = re.findall('In a relationship with(.*?)</a>',str(soup))
			name = re.findall('>\w+$',str(name_parse))
			f.write("<div><h2>Relationship : </h2> " + str(rs)[2:-2] + " with " + str(name) + "</div>\n")
		elif (re.findall('Relationship\<(.*?)relationship',str(soup))):
			rs = re.findall('Relationship\<(.*?)relationship',str(soup))
			rs_parse = re.findall('(Single|Married|Engaged)',str(rs))
			if rs_parse[0] == "Married":		
				rs_name = re.findall('Married to(.*?)</a>',str(rs))
				name = re.findall('>\D+$',str(rs_name))
				f.write("<div><h2>Relationship : </h2>" + str(rs_parse)[2:-2] + " To " + str(name)[3:-4] + "</div>\n")
			elif rs_parse[0] == "Engaged":
				rs_name = re.findall('Engaged to(.*?)</a>',str(rs))
				name = re.findall('>\D+$',str(rs_name))
				f.write("<div><h2>Relationship : </h2>" + str(rs_parse)[2:-2] + " To " + str(name)[3:-4] + "</div>\n")
			elif (re.findall('Single',str(soup))):
				f.write("<div><h2>Relationship : </h2> Single</div>\n")
			else:
				f.write("<div><h2>Relationship : </h2> Relationship Not recognize</div>\n")
		else:
			f.write("<div><h2>Relationship : </h2> No relationship found.</div>\n")
		f.close()
		

	
	#login proccess
	def login(self,email):
		driver = webdriver.Firefox()
		driver.get("http:/m.facebook.com")


		#user name form
		elem = driver.find_element_by_name("email")
		elem.send_keys("Enter your email")

		#password name form
		elem = driver.find_element_by_name("pass")
		elem.send_keys("Enter you password")

		#send the login
		elem = driver.find_element_by_name("login")
		elem.send_keys(Keys.RETURN)

		#search user
		elem = driver.find_element_by_name("query")
		elem.send_keys(email) 
		elem = driver.find_element_by_xpath("//input[@type='submit']")
		elem.send_keys(Keys.RETURN)


		#select user
		source = driver.page_source
		links = re.findall('fref=search.>.*?</a>',source,re.MULTILINE)

		link_text = []
		for link in links:
			parse = re.search('>.*?<',link,re.MULTILINE)
			parse = parse.group(0)[1:-1]
			link_text.append(parse)

		'''
		pprint(link_text)
		selection = raw_input("Please select one of the above : ")
		'''

		flag = 0

		#Check if the Email is valid
		try:
			elem = driver.find_element_by_xpath("//a[contains(.,'{}')]".format(link_text[0]))
			elem.send_keys(Keys.RETURN)

		except:
			flag = 1

		#data collector - About
		profile_html = driver.page_source.encode('utf-8')
		soup = BeautifulSoup(profile_html,"lxml")

		return soup,driver,flag

		

		
		#profile picture parser
		'''
		action = ActionChains(driver)
		elem = driver.find_element_by_xpath("//img[@alt='{}']".format(link_text[0]))
		action.context_click(elem).perform( )
		elem.send_keys(Keys.ARROW_DOWN)
		elem.send_keys(Keys.ARROW_DOWN)
		elem.send_keys(Keys.ARROW_DOWN)
		elem.send_keys(Keys.ARROW_DOWN)
		elem.send_keys(Keys.ARROW_DOWN)
		elem.send_keys(Keys.ARROW_DOWN)
		elem.send_keys(Keys.ARROW_DOWN)
		elem.send_keys(Keys.ARROW_DOWN)
		elem.send_keys(Keys.ARROW_DOWN)
		elem.send_keys(Keys.ARROW_DOWN)
		elem.send_keys(Keys.RETURN)
		'''		





































































































'''
string_soup = str(soup)
about = re.findall('>Timeline(.*?)>Block this person<',string_soup,re.MULTILINE)
about = str(about)
print about
print
print 
	#Work
work = re.findall('work(.*?)</a>',about,re.MULTILINE) #class="da bn r"
work = str(work)
work_parse = re.findall('alt="(.*?)"',work)
print "Work at : "+str(work_parse)


	#Education
education = re.findall('education(.*?)class="da bn r"',about,re.MULTILINE)
education = str(education)
education_parse = re.findall('alt="(.*?)"',education,re.MULTILINE)
print "Education : "+str(education_parse)

	#Living place
place = re.findall('Current City(.*?)</a>',about,re.MULTILINE)
place = str(place)
print place
place_parse = re.findall('>\w<',place,re.MULTILINE)
print "Lives in : "+str(place_parse)


	#Gender
gender = re.findall('Gender(.*?)</div></td></tr>',about,re.MULTILINE)
gender = str(gender)
gender_parse = re.findall('"dp">(.*?)\Z',gender,re.MULTILINE)
print "Gender : "+str(gender_parse)

	
	#relationship
relation = re.findall('In a(.*?)</div>',about,re.MULTILINE)



	#phone
phone = re.findall('dir="ltr">(.*?)</span>',about,re.MULTILINE)












#Pictures

os.makedirs("C:\Facebook_info\\"+link_text[0])

f = open('C:\Facebook_info\\'+link_text[0]+'\Link to profile.txt','a')
f.write(driver.current_url)

driver.get_screenshot_as_file('C:\Facebook_info\\'+link_text[0]+'\About.png')


elem = driver.find_element_by_link_text("Likes")
elem.send_keys(Keys.RETURN)
driver.get_screenshot_as_file('C:\Facebook_info\\'+link_text[0]+'\Likes.png')

#Pelephone
def pelephone(driver):
	driver.get("http://www.pelephone.co.il//digital/3G/Corporate/digital/support/general_info/find_number/.aspx")
	elem = driver.find_element_by_id("ctl00_ContentPlaceHolderLeft_txtLastName")
	elem.send_keys(about_lst[1])
	elem = driver.find_element_by_id("ctl00_ContentPlaceHolderLeft_txtCity")
	elem.send_keys(place_split[0][1:])
	elem = driver.find_element_by_xpath("//a[@class='btn_search btn']")
	elem.send_keys(Keys.RETURN)
	profile_html = driver.page_source.encode('utf-8')
	soup = BeautifulSoup(profile_html,"lxml")
	print(soup.prettify())
'''
