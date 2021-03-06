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
    json_targets = open("web/res/targets.json").read()
    out = json.loads(json_targets)
    out["targets"].update(target)
    json_targets = open("web/res/targets.json", "w")
    json.dump(out, json_targets)
    print(out)

@eel.expose
def remove_target(targetid):
    target = targetid.split(" ")[0];
    print(target)
    json_targets = open("web/res/targets.json").read()
    out = json.loads(json_targets)
    try:
        del out["targets"][target]
    except KeyError:
        print("Key "+target+" not found")
    json_targets = open("web/res/targets.json", "w")
    json.dump(out, json_targets)
    print(out)

@eel.expose
def save_config(obj):
    with open('web/res/input.json', 'w') as outfile:
        json.dump(obj, outfile)


eel.start('main.html', block=False)

while True:
    eel.sleep(10)
