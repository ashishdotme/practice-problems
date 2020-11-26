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
    for row in db["problems"].rows_where(order_by="created_utc desc limit 1000"):
        index.append(
            "* **{topic}** - [{title}]({url}) - *last updated at {date}*".format(
                topic=row["topic"].capitalize(),
                title=string.capwords(row["title"].replace("-", " ")),
                date=row["updated"].split("T")[0],
                url=row["url"]
            )
        )
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
