import requests
import xmltodict
import json 

if __name__ == "__main__":
    # download rss feed from mikan.
    url = "https://mikanani.me/RSS/Classic"
    response = requests.get(url)
    with open("rss/mikan-today.xml", "wb") as file:
        file.write(response.content)
    out = xmltodict.parse(open("rss/mikan-today.xml", encoding="utf-8").read())
    # format XML 
    xmltodict.unparse(
        out, output=open("rss/mikan-today.xml", mode="w", encoding="utf-8"), pretty=True
    )
    
    # add all items
    with open("rss/all_items.json", encoding="utf-8") as file:
        all_items = json.load(file)
        all_links = [item["link"] for item in all_items]
    new_items = []
    items = out["rss"]["channel"]["item"]
    count = 0
    for item in items:
        link = item["link"]
        if link not in all_links:
            all_items.append(item)
            new_items.append(item)
            print(f"{link=} added")
            count += 1

    with open("rss/all_items.json", "w", encoding="utf-8") as file:
        json.dump(all_items, file, indent=2, ensure_ascii=False)
    print(f"Added {count} new items")