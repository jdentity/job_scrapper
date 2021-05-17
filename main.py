from flask import Flask, render_template, request, redirect, send_file
from livereload import Server
from stackoverflow import get_jobs as get_sof
from wework import get_jobs as get_wework
from remoteok import get_jobs as get_remoteok
from exporter import save_to_file

app = Flask("SuperScrapper")
db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    word = request.args.get('word')
    jobs = []
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs += get_sof(word)
            jobs += get_wework(word)
            jobs += get_remoteok(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template("report.html", searchingBy=word, resultsNumber=len(jobs), jobs=jobs)


@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_file(jobs)
        return send_file(f"{word}.csv")
    except:
        return redirect("/")


app.run(host="127.0.0.1")
server = Server(app.wsgi_app)
server.serve()
