from flask import Flask, request, render_template, jsonify
from . import tagsSuggestion

app = Flask(__name__, template_folder='templates')



@app.route('/')
def home():
	return render_template('index.html')


@app.route('/suggestTags',methods=['POST'])
def get_tags_suggestion():
	try : 
	    if request.method=='POST':
	        result=request.form
	        title = result['title']
	        body_text = result['body_text']
	        body_code = result['body_code']
	        tags = tagsSuggestion.suggest_tags(title, body_text, body_code)
	        return jsonify(tags[0])
	except Exception as e:
		print(e)
		return("Error : ", str(e))