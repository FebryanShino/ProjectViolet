"""
A program to run website
"""

from flask import Flask, render_template
from threading import Thread
from Violet import bot_info

app = Flask(__name__)


@app.route('/')
def home():

  return render_template("main_website.html",
                         t_url=bot_info.twitter,
                         g_url=bot_info.github,
                         rep_url=bot_info.repository)


def run():
  app.run(host='0.0.0.0', port=8080)


def Heart():
  t = Thread(target=run)
  t.start()
