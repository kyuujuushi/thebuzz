from flask import Flask, render_template

the_buzz = Flask(__name__)

@the_buzz.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    the_buzz.run()
