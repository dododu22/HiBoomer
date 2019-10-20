"""
Demo Flask application to test the operation of Flask with socket.io

Aim is to create a webpage that is constantly updated with random numbers from a background python process.

30th May 2014

===================

Updated 13th April 2018

+ Upgraded code to Python 3
+ Used Python3 SocketIO implementation
+ Updated CDN Javascript and CSS sources

"""




# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
from jinja2 import Environment, FileSystemLoader
from contacts import change_contact
from photos import change_photo
from homepage import homepage
from call import call
import os
from test_gdrive import GDriveThread

__author__ = ''

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

class RandomThread(Thread):
    def __init__(self):
        self.delay = 3
        super(RandomThread, self).__init__()

    def randomNumberGenerator(self):
        #infinite loop of magical random numbers
        contact_selected = [True, False, False]
        paysages = os.listdir("static/photos")
        photo_selected = [False] * len(paysages)
        photo_selected[0]=True
        comments = ["La Bretagne ça vous gagne", "Les alpes en automne!", "La bretagne en été c'est très beau", "Posé en Y dans mon char à voile", "Quel soleil Mamie!", "Le printemps est la!"]
        thread2 = GDriveThread()
        thread2.start()
        while not thread_stop_event.isSet():
            if False:
                contact_selected=change_contact(True, contact_selected, socketio, self.delay)
            if True:
                photo_selected = change_photo(photo_selected, comments, True, socketio, self.delay)
            if False:
                call("doran", socketio, 100)
            if False:
                homepage(socketio, self.delay)

    def run(self):
        self.randomNumberGenerator()


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = RandomThread()
        thread.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
