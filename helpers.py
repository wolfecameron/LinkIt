#this file contains all helper functions that are used for the website separately


#filters image to separate foreground from background and returns text from image
def read_photo(ocr_text):
	
	
	return parse_lines(ocr_text)


#file name should be a string input
#i.e. file.filename
#also submit allowed file extensions
'''
def allowed_file(filename, allowed_ext):
	#returns true if file name has '.' and an allowed extension
	return '.' in filename and filename.rsplit('.',1)[1].lower() in allowed_ext
'''

#takes list of URLs from find_url_tmp and eliminates anything that cannot be a URL
def elim_nonurl(cand_list):
	urls = []
	for x in cand_list:
		good_url = True
		if(len(x) < 5):
			good_url = False
		elif(' ' in x):
			good_url = False
		elif("'" in x or '"' in x):
			good_url = False
		elif(not(any(c.isalpha() for c in x))):
			good_url = False
		
		if(good_url):
			urls.append(x)

	finalString = ""
	if(len(urls) > 0):
		finalString += urls[0]
		
		for x in range(1,len(urls)):
			finalString += "\n" + urls[x]
	else:
		finalString = "No URL was found in your photo, please try again!"
	
	return finalString



#creates a cool launch sequence when you run the app from the terminal
def launch_sequence():
	print("LinkIt! Launch Sequence:")
	start = time.clock()
	print("Launching in . . . ")
	print("3")
	while(not(time.clock() - start > 1)):
		start = start
	print("2")
	start = time.clock()
	while(not(time.clock() - start > 1)):
		start = start
	print("1")
	start = time.clock()
	while(not(time.clock() - start > 1)):
		start = start
 
#splits OCR text into separate lines and checks to see if each line could contain a URL
def parse_lines(text):
	possible_urls = []
	lines = text.splitlines()
	for line in lines:
		if(line.count('.') > 0 or line.count('/') > 0):
			possible_urls.append(line)
	
	return possible_urls


def find_url_period(text):
	#finds details of URl by using # of periods, checks if followed by .com or preceded by www.
	start = 0 #holds start/end indices of URL within the string
	end = 0
	found_start = False
	found_end = False
	#finds beginning of URL
	for ind in range(len(text)):
		if(text[ind] == '.'):
			if(ind -3 >= 0 and text[ind - 3:ind] == 'www'):
				#this will place the start index at beginning of www
				start = ind - 3 
				found_start = True
			else:
				while(ind>0 and not(text[ind] == ' ' or text[ind] == '[' or text[ind] == ']')):
					ind -= 1
				start = ind
				found_start = True
			end = ind + 1
			break

	#finds end of URL
	for ind in range(end,len(text)):
		if(text[ind] == '.'):
			if(text[ind+1:ind+4] == 'com' or text[ind+1:ind+4] == 'org' or text[ind+1:ind+4] == 'edu' or text[ind+1:ind+4] == 'net'):
				end = ind + 4
				if(end < len(text) and text[end]=='/'):
					while(end < len(text) and not(text[end]=='[' or text[end] == ']' or text[end] == ' ')):
						end += 1
				found_end = True
			else:
				while(ind < len(text) and not(text[ind] == ']' or text[ind] == '[' or text[ind] == ' ')):
					ind += 1
				end = ind
				break
		
		elif(text[ind] == ']' or text[ind] == '[' or text[ind] == ' '):
			end = ind
			found_end = True
			break


	if(not(found_end)):
		end = len(text)

	#trims whitespace on the ends of URLs
	URL = text[start:end]
	if(URL[0] == ' '):
		URL = URL[1:]
	runner = 0
	while(runner < len(URL) and not(URL[runner] == ' ')):
		runner += 1

	URL = URL[:runner]
	return URL

#print read_photo(Image.open('/home/wolfecameron/Desktop/Projects/linkit_im/test7.PNG'))