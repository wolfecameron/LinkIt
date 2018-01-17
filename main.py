from flask import Flask, render_template, request, redirect, url_for, flash
from helpers import read_photo, elim_nonurl, launch_sequence, parse_lines, find_url_period
from google.cloud import vision
from google.cloud.vision import types




#used to decide if launch sequence should run or not

launch = False

app = Flask(__name__)
app.debug = True
app.secret_key = 'AOSJGOIE!#19247102//fasf!+'


#holds all allowable file extensions
EXTENSIONS = set(['pdf','png','jpg','jpeg'])



@app.route('/')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/submit')
def submit():
	
	return render_template("pic_submit.html")


@app.route('/upload_photo', methods = ['POST','GET'])
def upload_photo():
	
	#only runs if something is being posted
	if request.method == 'POST':
		if 'file' not in request.files:
			return render_template('pic_submit.html', error = "ERROR: No File, or an unsecure file, was submitted.")
		
		vision_client = vision.ImageAnnotatorClient()
		file = request.files['file']

		content = file.read()
		'''
    	with open("photo_post_read.jpg", "wb") as new_image:
        	new_image.write(content)
		'''
		#3image = vision_client.image(content=content)
		#ocr = image.detect_text()
		'''
		#opens/closes photo and reads data from the upload to be input into cloud vision API
		with io.open(file, 'rb') as image_file:
			content = image_file.read()
		'''
		
		
		#performs parsing algorithm from helpers.py on picture to identify cadidate URLs
		#Image file is automatically closed after handling
		
		image = types.Image(content=content)
		ocr = vision_client.text_detection(image=image)
		text = ocr.text_annotations
		text_list = str(text[0])
		text_list = text_list.split()
		check = 0

		extracted_data = []

		for x in text_list:
			if('description' in x and check == 0):
				check += 1
			elif('bounding_poly' in x and check == 1):
				check += 1

			if(check == 1):
				extracted_data.append(x)
			if(check == 2):
				break

		candidate_URLs = []
		for text in extracted_data:
			candidate_URLs.append(find_url_period(text))


		finalString = elim_nonurl(candidate_URLs)	
			

		
		'''
		textList = read_photo(ocr)
		parsed = []
		for x in textList:
			parsed.append(find_url_period(x))

		finalString = elim_nonurl(parsed)
		'''		


		return render_template('display_link.html', link=finalString)
	
	else:
		
		return render_template('pic_submit.html', error = "ERROR: No File, or an unsecure file, was submitted.")
	
	return render_template("pic_submit.html")




@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500









if __name__ == "__main__":
	'''
	if(launch):
		#makes a cool little launch sequence in the terminal for extra suspense 
		launch_sequence()
		launch = False #makes sure launching sequence doesn't keep running
	'''
	app.run()



