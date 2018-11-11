#check if the target in the history
def history_check(self,target):		
		#variable for path
		Dir = "Put your History path here"

		for fileList in os.walk(Dir):
			for history_file in fileList:
				if str(target) in str(history_file):
					return 1
		return 0

	#Main
	def history_action(self,target):
		flag = self.history_check(target)

		if flag == 1:
			handle = open("History\\" + str(target) + ".txt","r") # where is the history files
			date = handle.readline()
			print "I have search result for " + target + " from " + date 
			chose = raw_input("Do you want to see the old result ? Yes/No \n")
			while chose != 0:
				if chose.lower() == "yes":
					urls = []
					for line in handle:
						urls.append(line)
					self.print_users(urls)
					chose = 0
				elif chose.lower() == "no":
					self.search_target(target)
					chose = 0
				else:
					chose = raw_input("Wrong input ... Please try agin ? Yes/No \n")
		else:
			self.search_target(target)

	#write the history file
	def history_writter(self,target,urls):
		handle = open("History\\" + str(target) + ".txt","w")
		handle.write(strftime("%Y-%m-%d %H:%M:%S \n", gmtime()))
		for url in urls:
			handle.write(url + "\n")
			url = urls[int(chose) - 1]
		driver = webdriver.Firefox()
		driver.get(url)

			chose = 1
		while chose != 999:
			chose = raw_input("Select another user :\nTo exit press 999 \n")
			if int(chose) == 999:
				break
			else:
				url = urls[int(chose) - 1]
				driver = webdriver.Firefox()
				driver.get(url)
