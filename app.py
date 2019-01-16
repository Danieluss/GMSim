import eel
eel.init('web')


@eel.expose
def start_sim():
    print("ok")


eel.start('main.html', block=False)

while True:
    eel.sleep(10)
