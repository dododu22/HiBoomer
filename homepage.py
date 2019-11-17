from jinja2 import Environment, FileSystemLoader
from time import sleep

def homepage(socketio, animate="None"):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template("homepage.html")
    if animate == "orangeShake":
        blueButton = "None"
        orangeButton = "shake"
    elif animate == "blueShake":
        blueButton = "shake"
        orangeButton = "None"
    else:
        blueButton = "None"
        orangeButton = "None"
    output = template.render(blueButton=blueButton, orangeButton=orangeButton)
    socketio.emit('html', {'number': output}, namespace='/test')
