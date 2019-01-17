import eel
eel.init('web')


@eel.expose
def start_sim():
    print("ok")


@eel.expose
def add_target(target):
    print("add")


@eel.expose
def remove_target(targetid):
    print("rem")


eel.start('main.html', block=False)

while True:
    eel.sleep(10)
