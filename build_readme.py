import pathlib
import string
import sqlite_utils
import sys
import re

root = pathlib.Path(__file__).parent.resolve()

index_re = re.compile(
    r"<!\-\- index starts \-\->.*<!\-\- index ends \-\->", re.DOTALL)

if __name__ == "__main__":
    db = sqlite_utils.Database(root / "problems.db")
    by_topic = {}
    index = ["<!-- index starts -->"]
    for row in db["problems"].rows_where(order_by="created"):
        by_topic.setdefault(row["topic"], []).append(row)
    index = ["<!-- index starts -->"]
    for topic, rows in by_topic.items():
        index.append("## {}\n".format(topic.capitalize()))
        for row in rows:
            index.append(
                "* [{title}]({url}) - {date}".format(
                    date=row["created"].split("T")[0], **row
                )
            )
        index.append("")
    if index[-1] == "":
        index.pop()
    index.append("<!-- index ends -->")
    if "--rewrite" in sys.argv:
        readme = root / "README.md"
        index_txt = "\n".join(index).strip()
        readme_contents = readme.open().read()
        readme.open("w").write(index_re.sub(index_txt, readme_contents))
    else:
        print("\n".join(index))
