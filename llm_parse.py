import json
import os

from openai import OpenAI

api_key = os.environ.get("SILICONFLOW_API_KEY")
# print(vars(os.environ))
assert api_key is not None, "Please set the SILICONFLOW_API_KEY environment"

client = OpenAI(base_url="https://api.siliconflow.cn/v1", api_key=api_key)

# referenced from https://github.com/EstrellaXD/Auto_Bangumi/blob/81b3a4aacd41e93032d809b27a69ebdd431a4ed0/backend/src/module/parser/analyser/openai.py#L10
default_prompt = r'''
You will now play the role of a super assistant. 
Your task is to extract structured data from unstructured text content and output it in JSON format. 
If you are unable to extract any information, please keep all fields and leave the field empty or default value like `''`, `None`.
But Do not fabricate data!

the python structured data type is:

```python
@dataclass
class Episode:
    title_en: Optional[str]
    title_zh: Optional[str]
    title_jp: Optional[str]
    size: Optional[str]
    season: int
    season_raw: str
    episode: int | str
    sub: str
    group: str
    resolution: str
    source: str
```

Example:

```
input: "【喵萌奶茶屋】★04月新番★[夏日重现/Summer Time Rendering][11][1080p][繁日双语][招募翻译]"
output: {"group": "喵萌奶茶屋", "title_en": "Summer Time Rendering", "resolution": "1080p", "episode": 11, "season": 1, "title_zh": "夏日重现", "sub": "", "title_jp": "", "season_raw": "", "source": "", "size": None}

input: "【幻樱字幕组】【4月新番】【古见同学有交流障碍症 第二季 Komi-san wa, Komyushou Desu. S02】【22】【GB_MP4】【1920X1080】【1.2GB】"
output: {"group": "幻樱字幕组", "title_en": "Komi-san wa, Komyushou Desu.", "resolution": "1920X1080", "episode": 22, "season": 2, "title_zh": "古见同学有交流障碍症", "sub": "", "title_jp": "", "season_raw": "", "source": "", "size": "1.2GB"}

input: "[Lilith-Raws] 关于我在无意间被隔壁的天使变成废柴这件事 / Otonari no Tenshi-sama - 09 [Baha][WEB-DL][1080p][AVC AAC][CHT][MP4]"
output: {"group": "Lilith-Raws", "title_en": "Otonari no Tenshi-sama", "resolution": "1080p", "episode": 9, "season": 1, "source": "WEB-DL", "title_zh": "关于我在无意间被隔壁的天使变成废柴这件事", "sub": "CHT", "title_jp": "", "size": None}

input: "[ANi] Puniru is a Kawaii Slime /  噗妮露是可爱史莱姆 - 08 [1080P][Baha][WEB-DL][AAC AVC][CHT][MP4][389.5 MB]"
output: {'group': 'ANi', 'title_en': 'Puniru is a Kawaii Slime', 'resolution': '1080P', 'episode': 8, 'season': 1, 'source': 'WEB-DL', 'title_zh': ' 噗妮露是可爱史莱姆', 'sub': 'CHT', 'title_jp': '', "size": "389.5 MB"}

input: "[7³ACG] 哥布林杀手 第2季/ゴブリンスレイヤーII/Goblin Slayer S02 | 01-12 [简繁字幕] BDrip 1080p AV1 OPUS 2.0[5.5GB]"
output: {'group': '7³ACG', 'title_en': 'Goblin Slayer', 'resolution': '1080p', 'episode': "1-12", 'season': 2, 'source': 'BDrip', 'title_zh': '哥布林杀手', 'sub': '简繁字幕', 'title_jp': 'ゴブリンスレイヤーII', "size": "5.5GB"}

```
'''

promt_v1  = f"""Below is a torrent title for Japanese anime. Please parse and extract the following information, return in json format
* Title: it can contains numbers, Japanese, Chinese and English characters
* Fansub: the group name of Fansub, usually enclosed in square brackets at the beginning of the title, like [ANi] [LoliHouse], return the value without brackets
* Season: usually a number like S01, S02, set to 1 if not available
* Episode: usually a number, set to 1 if not available
* Resolution: the resolution of the bangumi, numbers followed by a 'P' like 1080P, 720P, 480P
* Size: the size of the torrent file, usually enclosed in square brackets, like [592.8 MB] or [1.2 GB], return the value without brackets
* Extentsion: file extension of the torrent file, usually enclosed in square brackets, such as [MP4], [WebRip], return the value without brackets
"""

def llm_parse_desc(
    desc="[ANi] MF Ghost S02 /  燃油车斗魂 第二季 - 20 [1080P][Baha][WEB-DL][AAC AVC][CHT][MP4][592.8 MB]",
    model="deepseek-ai/DeepSeek-V2-Chat",
    stream=False,
):

    response = client.chat.completions.create(
        # model="Qwen/Qwen2.5-7B-Instruct",
        model=model,
        messages=[
            # {"role": "user", "content": "SiliconCloud公测上线，每用户送3亿token 解锁开源大模型创新能力。对于整个大模型应用领域带来哪些改变？"}
            {"role": "system", "content": default_prompt},
            {"role": "user", "content": desc}
        ],
        stream=stream,
        response_format={"type": "json_object"},
    )
    res = response.choices[0].message.content
    try:
        r = json.loads(res)
        if not isinstance(r, dict):
            return None
        new_r = {}
        for k, v in r.items():
            new_r[k.strip()] = v
        return new_r
    except Exception as e:
        return None


if __name__ == "__main__":
    res = llm_parse_desc()
    # model = "deepseek-ai/DeepSeek-V2-Chat"
    model = "Qwen/Qwen2.5-7B-Instruct"
    parsed_key = f"parsed_{model.replace('/', '--')}"

    with open("rss/all_items.json", encoding="utf-8") as file:
        all_items = json.load(file)
    new_all_items = []
    for idx, item in enumerate(all_items):
        print("---" * 20, idx, len(all_items), "---" * 20)
        if parsed_key in item:
            print(f"Skip {item['link']}")
        else:
            print(f"Parsing {item['link']} {model=}")
            print(item["description"])
            res = llm_parse_desc(item["description"], model=model)
            if res is not None:
                item[parsed_key] = res
            print(res)
            # input("Press Enter to continue...")
            
        new_all_items.append(item)

    with open("rss/all_items.json", "w", encoding="utf-8") as file:
        json.dump(new_all_items, file, indent=2, ensure_ascii=False)
