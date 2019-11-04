from jinja2 import Environment, FileSystemLoader
from time import sleep


def change_contact(right, is_selected, socketio, animate, buttonAnimation):
    rightArrow = "None"
    leftArrow = "None"
    orangeButton = "None"
    blueButton = "None"
    val=-1
    if right:
        val=1
    if animate:	    
        index = get_true_index(is_selected)
        is_selected[index]=False
        index=(index+val)%len(is_selected)
        is_selected[index]=True
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template("contacts.html")
    class_select= []
    display= []

    for i in range(0, len(is_selected)):
        if is_selected[i]:
            class_select.append("contact_selected")
            display.append("")
        else:
            class_select.append("contact")
            display.append("none")
    print(buttonAnimation)
    if buttonAnimation == "rightArrow":
        rightArrow = "background"
    elif buttonAnimation == "leftArrow":
        leftArrow = "background"
    elif buttonAnimation == "orangeButton":
        orangeButton = "shake"
    elif buttonAnimation == "blueButton":
        blueButton = "shake"
    output = template.render(is_selected_1=class_select[0], is_selected_2=class_select[1], is_selected_3=class_select[2],
                            display_1=display[0], display_2=display[1], display_3=display[2], rightArrow=rightArrow, leftArrow=leftArrow, orangeButton= orangeButton,
                            blueButton=blueButton)
    print(is_selected)
        
    socketio.emit('html', {'number': output}, namespace='/test')
    sleep(0.5)

    return is_selected

def get_true_index(list_bool):
    for i in range(0, len(list_bool)):
        if list_bool[i]:
            return i
