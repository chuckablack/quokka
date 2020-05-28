import yaml
import json

with open("../data/inventory.json", "r") as json_in:
    json_inventory = json_in.read()

inventory = json.loads(json_inventory)
with open("../data/inventory.yaml", "w") as yaml_out:
    yaml_out.write(yaml.dump(inventory))

print("\nyaml pretty version:")
with open("../data/inventory.yaml", "r") as yaml_in:
    yaml_inventory = yaml_in.read()
print(yaml.dump(yaml.safe_load(yaml_inventory), indent=4))
