import yaml
import json

from quokka.controller.utils import log_console

with open("../data/devices.json", "r") as json_in:
    json_devices = json_in.read()

devices = json.loads(json_devices)
with open("../data/devices.yaml", "w") as yaml_out:
    yaml_out.write(yaml.dump(devices))

print("\nyaml pretty version:")
with open("../data/devices.yaml", "r") as yaml_in:
    yaml_devices = yaml_in.read()
print(yaml.dump(yaml.safe_load(yaml_devices), indent=4))
