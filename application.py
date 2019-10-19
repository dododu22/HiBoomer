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


__author__ = 'slynn'

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
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers
        print("Making random numbers")
        is_selected = [True, False, False]
        animate = False
        change_image=False
        i=0
        paysages = ["paysage", "paysage_2", "paysage_3"]
        paysages_index = 0
        comments = ["La bretagne ca vous gagne", "Les alpes en automnes", "La bretagne en ete c'est très beau"]
        while not thread_stop_event.isSet():
            file_loader = FileSystemLoader('templates')
            env = Environment(loader=file_loader)
            if False:
                template = env.get_template("contacts.html")
                class_select= []
                for i in range(0, len(is_selected)):
                    if is_selected[i]:
                        class_select.append("contact_selected")
                    else:
                        class_select.append("contact")
                
                output = template.render(is_selected_1=class_select[0], is_selected_2=class_select[1], is_selected_3=class_select[2])
                print(output)
                temp_list = []
                i=0
                while i<len(is_selected):
                    if is_selected[i]:
                        temp_list.append(False)
                        if i<len(is_selected)-1:
                            temp_list.append(True)
                            i+=1
                        else:
                            temp_list[0]=True
                            i+=1
                    else:
                        temp_list.append(False)
                    i+=1
                is_selected = temp_list
                print(is_selected)
                socketio.emit('html', {'number': output}, namespace='/test')
                sleep(self.delay)
            if False:
                for i in range(0, len(paysages)):
                    
                    animation_foreground="none"
                    animation_background="none"
                    image_foreground = paysages[i]
                    image_background = paysages[(i+1)%len(paysages)]
                    txtmsg_foreground = comments[i]
                    txtmsg_background = comments[(i+1)%len(paysages)]
                    template = env.get_template("photos.html")
                    output = template.render(txtmsg_foreground=txtmsg_foreground,txtmsg_background=txtmsg_background , animation_foreground=animation_foreground,
                                            animation_background=animation_background, image_foreground=image_foreground, image_background=image_background)

                    socketio.emit('html', {'number': output}, namespace='/test')
                    sleep(self.delay)

                    animation_foreground="foreground"
                    animation_background="background"

                    output = template.render(txtmsg_background=txtmsg_background,txtmsg_foreground=txtmsg_foreground, animation_foreground=animation_foreground,
                                            animation_background=animation_background, image_foreground=image_foreground, image_background=image_background)

                    socketio.emit('html', {'number': output}, namespace='/test')
                    sleep(self.delay)
            if True:
                
                template = env.get_template("call.html")
                output = template.render()
                socketio.emit('html', {'number': output}, namespace='/test')
                sleep(1000000)

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
