from time import sleep
from jinja2 import Environment, FileSystemLoader
from contacts import get_true_index
import os


def change_photo(photo_selected, comments, right, socketio, animate):
    paysages = os.listdir("static/photos")
    # if new photos arrived
    nb_false = len(paysages) - len(photo_selected)
    notification_opacity = 0
    if nb_false>0:
        notification_opacity = 1
    photo_selected = photo_selected + ([False]*nb_false)
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    position=get_true_index(photo_selected)
    direction=1
    if right:
        direction=-1
    image_foreground = paysages[position]
    image_background = paysages[(position+direction)%len(paysages)]
    txtmsg_foreground = comments[paysages[position].split(".")[0]]["comment"]
    txtmsg_background = comments[(paysages[(position+direction)%len(paysages)]).split(".")[0]]["comment"]
    contact_foreground = comments[paysages[position].split(".")[0]]["contact"]
    contact_background = comments[(paysages[(position+direction)%len(paysages)]).split(".")[0]]["contact"]
    date_foreground = comments[paysages[position].split(".")[0]]["date"]
    date_background = comments[(paysages[(position+direction)%len(paysages)]).split(".")[0]]["date"]
    template = env.get_template("photos.html")
    # output = template.render(txtmsg_foreground=txtmsg_foreground,txtmsg_background=txtmsg_background , animation_foreground=animation_foreground,
    #                         animation_background=animation_background, image_foreground=image_foreground, image_background=image_background, notification_opacity=notification_opacity,
    #                         contact_foreground=contact_foreground, contact_background=contact_background, date_foreground=date_foreground, date_background=date_background)

    # socketio.emit('html', {'number': output}, namespace='/test')
    # sleep(delay)
    if not animate:
        animation_foreground="none"
        animation_background="none"
    else:
        animation_foreground="foreground"
        animation_background="background"

    output = template.render(txtmsg_background=txtmsg_background,txtmsg_foreground=txtmsg_foreground, animation_foreground=animation_foreground,
                            animation_background=animation_background, image_foreground=image_foreground, image_background=image_background, notification_opacity=notification_opacity,
                            contact_foreground=contact_foreground, contact_background=contact_background, date_foreground=date_foreground, date_background=date_background)

    socketio.emit('html', {'number': output}, namespace='/test')
    photo_selected[position]=False
    photo_selected[(position+direction)%len(photo_selected)]=True
    print(photo_selected)
    return photo_selected