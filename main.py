import json

def readBookmarks():
    with open("Bookmarks.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    data = data['roots']['bookmark_bar']

    unwanted_keys = ['date_added', 'date_modified', 'id', 'guid', 'meta_info', 'date_last_used']

    data = remove_unwanted_keys(data, unwanted_keys)
    
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

def remove_unwanted_keys(obj, unwanted_keys):
    if isinstance(obj, dict):
        for key in list(obj.keys()):
            if key in unwanted_keys:
                del obj[key]
            else:
                obj[key] = remove_unwanted_keys(obj[key], unwanted_keys)
    elif isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = remove_unwanted_keys(obj[i], unwanted_keys)
    return obj


def json_to_markdown(obj, level=0):
    markdown = ""
    indent = "  " * level
    if isinstance(obj, dict):
        if "name" in obj and "type" in obj:
            if obj["type"] == "url":
                markdown += f"{indent}- [{obj['name']}]({obj['url']})\n"
            elif obj["type"] == "folder":
                markdown += f"{indent}- **{obj['name']}**\n"
                if "children" in obj:
                    for child in obj["children"]:
                        markdown += json_to_markdown(child, level + 1)
    elif isinstance(obj, list):
        for item in obj:
            markdown += json_to_markdown(item, level)
    return markdown


with open("data.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

markdown_output = json_to_markdown(data["root"])

with open('bookmarks.md', 'w', encoding='utf-8') as file:
    file.write(markdown_output)

print("Bookmarks have been successfully converted to markdown.")