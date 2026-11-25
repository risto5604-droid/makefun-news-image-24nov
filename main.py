#!/usr/bin/env python3
"""make.fun entry: "Sum up 24 November's world news in one image".

Copies the pre-rendered infographic (news.png, 1024x1024) to
/output/entry.png. Standard library only, no network access, fully
deterministic: the output bytes are identical on every run.
"""
import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.png")
DST_DIR = "/output"
DST = os.path.join(DST_DIR, "entry.png")


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    print("wrote", DST)


if __name__ == "__main__":
    main()
