from TwitterSearch import *

try:
    tuo = TwitterUserOrder('NeinQuarterly') # create a TwitterUserOrder

    # it's about time to create TwitterSearch object again
    ts = TwitterSearch(
        consumer_key = 'aaabbb',
        consumer_secret = 'cccddd',
        access_token = '111222',
        access_token_secret = '333444'
    )

    # start asking Twitter about the timeline
    for tweet in ts.search_tweets_iterable(tuo):
        print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )

except TwitterSearchException as e: # catch all those ugly errors
    print(e)































































































'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import sys

class Twitter(object):
	def __init__(self):
		self.login("chanoh daum")


	def login(self,name):
		driver = webdriver.Firefox()
		driver.get("https://twitter.com/search-home")#https://mobile.twitter.com/session/new

		#search
		elem = driver.find_element_by_id("search-home-input")
		elem.send_keys(name)
		elem.send_keys(Keys.ENTER)
		
		#password name form
		elem = driver.find_element_by_id("session[password]")
		elem.send_keys("123123123")
		
		#send the login
		elem = driver.find_element_by_id("signupbutton")
		elem.send_keys(Keys.RETURN)

		#search user
		
		elem.send_keys(name)
		elem.send_keys(Keys.ENTER)

		
		#user name form
		elem = driver.find_element_by_id("signin-email")
		elem.send_keys("ruclawra@dodsi.com")

		#password name form
		elem = driver.find_element_by_id("signin-password")
		elem.send_keys("123123123")
		
		#send the login
		elem = driver.find_element_by_xpath("//button[@type='submit']")
		elem.send_keys(Keys.RETURN)
		
		#search user
		elem = driver.find_element_by_id("search-query")
		elem.send_keys(name)
		elem.send_keys(Keys.ENTER)		
		elem = driver.find_elements_by_class_name("AdaptiveFiltersBar-target AdaptiveFiltersBar-target--link u-textUserColor js-nav")
		
		elem = driver.find_element_by_xpath("//input[@type='submit']")
		elem.send_keys(Keys.RETURN)
	

if __name__ == "__main__":
	twitter = Twitter()
'''