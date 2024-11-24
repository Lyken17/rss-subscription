import os
import json


all_items = json.load(open("rss/all_items.json", "r"))
key = "parsed_Qwen/Qwen2.5-7B-Instruct"
for item in all_items:
    # "Fansub": "Baha"
    try:
        if item[key]["Fansub"] == "Baha":
            item.pop(key)
    except KeyError:
        pass
open("rss/all_items.json", "w").write(json.dumps(all_items, indent=2))