import json
import os
import re
from time import time


def main():

    # fetch latest version
    os.system("git pull origin master")

    # load json
    with open("index.json", encoding="utf-8") as index_file:
        index = json.load(index_file)

    # search for missing keys
    for file in os.listdir("pages"):
        if file in index:
            continue

        print(f"Missing index found: {file}")
        name = input("Insert title of the post: ")
        tags = input("Insert tags of the post: ")
        index[file] = {
            "name": name,
            "tags": re.split("\s+", tags),
            "date": int(time()),
        }

    # save json
    with open("index.json", encoding="utf-8", mode="w") as index_file:
        json.dump(index, index_file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
