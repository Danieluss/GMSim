import eel
import json
from src import simulation
eel.init('web')

@eel.expose
def start_sim():
    simulation.run()
    eel.redraw()
    print("done")


@eel.expose
def add_target(target):
    print("add")


@eel.expose
def remove_target(targetid):
    print(targetid)


@eel.expose
def save_config(obj):
    with open('web/res/input.json', 'w') as outfile:
        json.dump(obj, outfile)

eel.start('main.html', block=False)

while True:
    eel.sleep(10)
