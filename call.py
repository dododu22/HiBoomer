from jinja2 import Environment, FileSystemLoader
from time import sleep

def call(contact, socketio, delay):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template("call.html")
    output = template.render(contact=contact)
    socketio.emit('html', {'number': output}, namespace='/test')
    sleep(delay)
