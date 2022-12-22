from flask import Flask, render_template, redirect, url_for, request, Markup
from Data import *
import random
import copy

app = Flask(__name__)


@app.route("/")
def index():
	return render_template("index.html",
		book_svg=Markup(open("images/book.svg").read()),
		boy_svg=Markup(open("images/oily_boy.svg").read()),
		logo_svg=Markup(open("images/giganigga.svg").read()),
		mans_svg=Markup(open("images/oily_mans.svg").read()),
		feather_svg=Markup(open("images/feather.svg").read()),
	)

@app.route("/tests-list")
def tests_list():
	l = []
	urls = []
	for i in data:
		l.append(data[i])
		urls.append(i)
	return render_template("tests-list.html", data=l, urls=urls)

@app.route("/theory")
@app.route("/theory/<title>")
def theories_list(title=None):
	l = []
	urls = []
	for i in data:
		l.append(data[i])
		urls.append(i)
	if title == None:
		return render_template("theories-list.html", l=l, urls=urls, data=None, title=title)	
	return render_template("theories-list.html", l=l, urls=urls, data=data[title], title=title)

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/test/<title>")
def test(title):
	if title not in data:
		return redirect(url_for("tests_list"))
	data2 = copy.deepcopy(data)
	random.shuffle(data2[title]["tests"])
	return render_template("test.html", title=title, data_og=data[title], data=data2[title])

@app.route("/meme")
def meme():
	return '<img src="https://sun9-71.userapi.com/impg/F5YoLqJqWzKKDAWDMVXIUkdl35hFfVTbV-oqIQ/xVksvEtmNzk.jpg?size=752x1009&quality=96&sign=d7911b0eca2374ff138587624543de70&type=album" width=100% height=100% style="display: inline;">'

@app.route("/check-test", methods=["POST"])
def check_test():
	d = request.form
	d = dict(filter(lambda x:x[1], d.items()))
	if len(d) == 0:
		return redirect(url_for("test", title=tuple(request.form.keys())[-1]))


	user_answers = {}
	title = list(request.form.keys())[-1]
	count = 0
	tests_ids = []
	for element in request.form:
		if element == title: break
		answer = "".join(request.form.getlist(element)).lower().strip()
		if answer == '': continue
		elif answer == data[title]["tests"][int(element)]["correct"]: count +=1
		user_answers[int(element)] = answer
		tests_ids.append(int(element))


	result = count / (len(d)-1) * 100

	return render_template("check.html", tests_ids=tests_ids, tests=data[title]["tests"], result=round(result, 2), user_answers=user_answers, theory=data[title]["content"])


if __name__ == '__main__':
	app.run(debug=True)