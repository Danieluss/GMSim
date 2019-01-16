import eel
eel.init('web')
eel.start('main.html', block=False)

while True:
    eel.sleep(10)