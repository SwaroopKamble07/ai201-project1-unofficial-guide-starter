import json
import os

JSON_FILES = [
    "source4", "source5", "source6", "source7",
    "source8", "source9", "source10",
]


def extract_comments(comments, depth=0):
    lines = []
    for item in comments:
        if item["kind"] != "t1":
            continue
        data = item["data"]
        body = data.get("body", "").strip()
        if body and body not in ("[deleted]", "[removed]"):
            lines.append(body)
        replies = data.get("replies", "")
        if isinstance(replies, dict):
            children = replies["data"]["children"]
            lines.extend(extract_comments(children, depth + 1))
    return lines


def parse_thread(name):
    json_path = os.path.join("documents", f"{name}.json")
    txt_path = os.path.join("documents", f"{name}.txt")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    post_data = data[0]["data"]["children"][0]["data"]
    title = post_data.get("title", "").strip()
    selftext = post_data.get("selftext", "").strip()

    comment_nodes = data[1]["data"]["children"]
    comment_lines = extract_comments(comment_nodes)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Title: {title}\n\n")
        if selftext and selftext not in ("[deleted]", "[removed]"):
            f.write(f"Post: {selftext}\n\n")
        f.write("Comments:\n\n")
        f.write("\n\n".join(comment_lines))

    print(f"Saved {txt_path} ({len(comment_lines)} comments)")


for name in JSON_FILES:
    json_path = os.path.join("documents", f"{name}.json")
    if not os.path.exists(json_path):
        print(f"Skipping {name} — {json_path} not found")
        continue
    parse_thread(name)

print("Done.")
