from jinja2 import Environment, FileSystemLoader
from time import sleep

def homepage(socketio):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template("homepage.html")
    output = template.render()
    socketio.emit('html', {'number': output}, namespace='/test')
