from time import sleep
from jinja2 import Environment, FileSystemLoader
from contacts import get_true_index

def change_photo(photo_selected, paysages, comments, right, socketio, delay):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    animation_foreground="none"
    animation_background="none"
    position=get_true_index(photo_selected)
    direction=1
    if right:
        direction=-1
    image_foreground = paysages[position]
    image_background = paysages[(position+direction)%len(paysages)]
    txtmsg_foreground = comments[position]
    txtmsg_background = comments[(position+direction)%len(paysages)]
    template = env.get_template("photos.html")
    output = template.render(txtmsg_foreground=txtmsg_foreground,txtmsg_background=txtmsg_background , animation_foreground=animation_foreground,
                            animation_background=animation_background, image_foreground=image_foreground, image_background=image_background)

    socketio.emit('html', {'number': output}, namespace='/test')
    sleep(delay)

    animation_foreground="foreground"
    animation_background="background"

    output = template.render(txtmsg_background=txtmsg_background,txtmsg_foreground=txtmsg_foreground, animation_foreground=animation_foreground,
                            animation_background=animation_background, image_foreground=image_foreground, image_background=image_background)

    socketio.emit('html', {'number': output}, namespace='/test')
    sleep(delay)
    photo_selected[position]=False
    photo_selected[(position+direction)%len(photo_selected)]=True
    print(photo_selected)
    return photo_selected