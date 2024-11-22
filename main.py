import json
import xml.etree.ElementTree as ET
import xmltodict
import requests
import requests
# Example usage
if __name__ == "__main__":
    # xml_file_path = 'class.xml'
    url = "https://mikanani.me/RSS/Classic"
    response = requests.get(url)
    with open("class.xml", "wb") as file:
        file.write(response.content)
    out = xmltodict.parse(open("class.xml", mode="r", encoding="utf-8").read())
    new_items = [] 
    items = out["rss"]["channel"]["item"]
    for item in items:
        print(json.dumps(item, indent=2, ensure_ascii=False))
        print(item["title"])
        if "lolihouse" in item["title"].lower():
            new_items.append(item)
    out["rss"]["channel"]["item"] = new_items
    xmltodict.unparse(out, output=open("rss/lolihouse.xml", mode="w", encoding="utf-8"), pretty=True)
