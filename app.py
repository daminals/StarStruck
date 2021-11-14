from flask import Flask, escape, request, render_template

from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')
