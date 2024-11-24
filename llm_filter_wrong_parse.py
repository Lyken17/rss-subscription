import json
import os

all_items = json.load(open("rss/all_items.json"))
key = "parsed_Qwen--Qwen2.5-7B-Instruct"
for item in all_items:
    if key not in item:
        continue

    skip = False
    parsed_info = item[key]
    for k, v in parsed_info.items():
        if k.strip() != k:
            skip = True
    if skip:
        item.pop(key)
        print(item)
        continue

open("rss/all_items.json", "w").write(json.dumps(all_items, indent=2, ensure_ascii=False))
