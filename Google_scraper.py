from google import search
import urllib2
import re
from time import gmtime, strftime

class Google(object):
	def __init__(self,email):
		url_list = self.google_search(email)#['http://lists.numenta.org/mailman/options/nupic_lists.numenta.org/roilipman--at--gmail.com',
                                      #'https://github.com/google/shaka-player/blob/master/AUTHORS',
                                                                            #'https://github.com/google/shaka-player/pull/231/files',
                                                                            #'https://github.com/google/shaka-player/pull/163/files',
                                                                            #'https://github.com/google/shaka-player/blob/master/CONTRIBUTORS',
                                                                            #'https://github.com/Peer5/shaka-player/blob/master/CONTRIBUTORS',
                                                                            #'http://whois.easycounter.com/roilipman.com',
                                                                            #'http://comments.gmane.org/gmane.org.google.api.calendar/8203',
                                                                            #'http://www.targettalk.org/viewtopic.php?f=6&t=19624','http://pastebin.com/PJGX1EfH']
		forums_list = self.forum_parser(url_list)
		phone_list = self.phone_parser(url_list)
		self.write_file(phone_list,forums_list)

	#Google search
	def google_search(self,email):
		url_list = []		
		for url in search(email, stop=3):
			# if "facebook" not in url:
			url_list.append(url)
		return url_list

	#Forums filter
	def forum_parser(self,url_list):
		forums_list = []
		for url in url_list:
			if "github.com" in url:
				forums_list.append(url)
			elif "stackoverflow.com" in url:
				forums_list.append(url)
			elif "pastebin.com" in url:
				forums_list.append(url)
		return forums_list


	#open the urls
	def phone_parser(self,url_list):
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
		phone_list = []
		for url in url_list:
			req = urllib2.Request(url, None, headers)
			page = urllib2.urlopen(req).read()
			phone = re.findall('05\d{1}-?\d{3}-?\d{4}',str(page))
			if len(phone) != 0:
				phone_list.append(phone)
		return phone_list

	def write_file(self,phone_list,forum_list):
		f = open("/var/www/cgi-bin/History/Google_scrapper.html",'w') #the caller function path
		f.write("<div id='forum' class='col3'>\n<h1 >Associated Forums</h1>\n")
		for forum in forum_list:
			f.write("<li>" + forum + "</li>\n")
		f.write("</div>")
		
		f.write("<div id='phone' class='col4'>\n<h1>Associated Phone</h1>\n")		
		final_phone = []
		for phone_number in phone_list:			
			for phone in phone_number:
				final_phone.append(phone)
				
		temp = set(final_phone)
		final_phone = list(temp)
		for phone in final_phone:
			f.write("<li>" + str(phone) + "</li>\n")
		f.write("</div>")
		

		f.close()