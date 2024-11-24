import requests
import xmltodict

if __name__ == "__main__":
    url = "https://mikanani.me/RSS/Classic"
    response = requests.get(url)
    with open("rss/mikan-today.xml", "wb") as file:
        file.write(response.content)
    out = xmltodict.parse(open("rss/mikan-today.xml", encoding="utf-8").read())
    # format XML 
    xmltodict.unparse(
        out, output=open("rss/mikan-today.xml", mode="w", encoding="utf-8"), pretty=True
    )