import json
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

import pytz
import requests
import xmltodict

if __name__ == "__main__":
    with open("rss/all_items.json", encoding="utf-8") as file:
        all_items = json.load(file)
        all_links = [item["link"] for item in all_items]

    # filter by date
    beijing_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))
    beijing_time = datetime.now().replace(tzinfo=pytz.timezone("Asia/Shanghai"))
    print(f"Current Beijing time: {beijing_time}")
    new_items = {1: [], 7: [], 30: []}
    for item in all_items:
        date_str = item["torrent"]["pubDate"]
        date_str = date_str.split(".")[0]  # ignore ms
        parsed_date = datetime.fromisoformat(date_str).astimezone(
            timezone(timedelta(hours=8))
        )
        for k, v in new_items.items():
            if (beijing_time - parsed_date).days < k:
                new_items[k].append(item)

    # composite recent k days
    template_rss = xmltodict.parse(open("rss/mikan-today.xml", encoding="utf-8").read())
    for k, items in new_items.items():
        out = template_rss.copy()
        out["rss"]["channel"]["title"] = f"mikan-recent-{k}-days"
        out["rss"]["channel"]["description"] = f"mikan-recent-{k}-days"
        out["rss"]["channel"]["item"] = items
        print(f"mikan-recent-{k}-days: {len(items)}")
        xmltodict.unparse(
            out,
            output=open(f"rss/mikan-recent-{k}.xml", mode="w", encoding="utf-8"),
            pretty=True,
        )

        lolihouse_items = []
        for item in items:
            if "lolihouse" in item["title"].lower():
                lolihouse_items.append(item)
        out = template_rss.copy()
        out["rss"]["channel"]["title"] = f"lolihouse-recent-{k}-days"
        out["rss"]["channel"]["description"] = f"lolihouse-recent-{k}-days"
        out["rss"]["channel"]["item"] = lolihouse_items
        print(f"lolihouse-recent-{k}-days: {len(lolihouse_items)}")
        xmltodict.unparse(
            out,
            output=open(f"rss/lolihouse-recent-{k}.xml", mode="w", encoding="utf-8"),
            pretty=True,
        )
