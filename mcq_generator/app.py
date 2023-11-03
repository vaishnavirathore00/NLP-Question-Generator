from flask import Flask, request, render_template, flash, redirect, url_for,session, Response, render_template_string
from objective import ObjectiveTest



app = Flask(__name__)

import nltk
nltk.download("all")
nltk.download("punkt")
# exit()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/test_generate', methods=["POST"])
def test_generate():
	if request.method == "POST":
		inputText = request.form["itext"]
		testType = request.form["test_type"]
		noOfQues = request.form["noq"]
		if testType == "objective":
			objective_generator = ObjectiveTest(inputText,noOfQues)
			question_list, answer_list = objective_generator.generate_test()
			testgenerate = zip(question_list, answer_list)
			return render_template('generatedtestdata.html', cresults = testgenerate)
		else:
			flash('Error Ocuured!')
			return redirect(url_for('/'))

if __name__ == "__main__":
	app.run(debug=True)