from flask import Flask, render_template, request, redirect, url_for, flash
from PIL import Image
import os
from helpers import read_photo, allowed_file, elim_nonurl, launch_sequence, parse_lines, find_url_period




#used to decide if launch sequence should run or not

launch = False

app = Flask(__name__)
app.debug = True
app.secret_key = 'AOSJGOIE!#19247102//fasf!+'


#holds all allowable file extensions
EXTENSIONS = set(['pdf','png','jpg','jpeg'])

#specifies folder that images will be uploarded into
UPLOAD_FOLDER = '/UPLOADS'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
			return redirect(request.url)

		file = request.files['file']
		
		if file and allowed_file(file.filename, EXTENSIONS):
			img = Image.open(file)
			
			#performs parsing algorithm from helpers.py on picture to identify cadidate URLs
			
			textList = read_photo(img)
			parsed = []
			for x in textList:
				parsed.append(find_url_period(x))
			
			finalString = elim_nonurl(parsed)
			

			return render_template('display_link.html', link=finalString)
	else:
		
		return render_template('pic_submit.html', error = "ERROR: No File, or an unsecure file, was submitted.")
	return render_template("pic_submit.html")













if __name__ == "__main__":
	'''
	if(launch):
		#makes a cool little launch sequence in the terminal for extra suspense 
		launch_sequence()
		launch = False #makes sure launching sequence doesn't keep running
	'''
	app.run()



