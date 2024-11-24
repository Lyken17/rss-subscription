from openai import OpenAI
import os
import json

api_key=os.getenv('SILICONFLOW_API_KEY')
assert api_key is not None, "Please set the SILICONFLOW_API_KEY environment"

client = OpenAI(
    base_url='https://api.siliconflow.cn/v1',
    api_key=api_key
)

def llm_parse_desc(
    desc="[ANi] MF Ghost S02 /  燃油车斗魂 第二季 - 20 [1080P][Baha][WEB-DL][AAC AVC][CHT][MP4][592.8 MB]",
    model="deepseek-ai/DeepSeek-V2-Chat",
    stream = False
):
    content = f'''Below is a torrent title for Japanese anime. Please parse and extract the following information, return in json format
    * Title: it can contains numbers, Japanese, Chinese and English characters
    * Fansub: the group name of Fansub, usually enclosed in square brackets at the beginning of the title, like [ANi] [LoliHouse], return the value without brackets
    * Season: usually a number like S01, S02, set to 1 if not available
    * Episode: usually a number, set to 1 if not available
    * Resolution: the resolution of the bangumi, numbers followed by a 'P' like 1080P, 720P, 480P
    * Size: the size of the torrent file, usually enclosed in square brackets, like [592.8 MB] or [1.2 GB], return the value without brackets
    * Extentsion: file extension of the torrent file, usually enclosed in square brackets, such as [MP4], [WebRip], return the value without brackets

    The title is:
    {desc}
    '''

    response = client.chat.completions.create(
        # model="Qwen/Qwen2.5-7B-Instruct",
        model=model,
        messages=[
            # {"role": "user", "content": "SiliconCloud公测上线，每用户送3亿token 解锁开源大模型创新能力。对于整个大模型应用领域带来哪些改变？"}
            {"role": "user", "content": content}
        ],
        stream=stream,
        response_format={"type": "json_object"}
    )
    res = response.choices[0].message.content
    try:
        r = json.loads(res)
        if isinstance(r, dict):
            return r
        else:
            return None
    except Exception as e:
        return None
            
if __name__ == "__main__":
    res = llm_parse_desc()
    # model = "deepseek-ai/DeepSeek-V2-Chat"
    model = "Qwen/Qwen2.5-7B-Instruct"
    parsed_key = f"parsed_{model}"
    
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