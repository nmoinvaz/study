#!/usr/bin/env python
import sys
import os
import argparse
import copy
import xmltodict
from sys import platform
import pprint
import codecs
import re

def save_to_file(path, lines):
    with codecs.open(path, "w", "utf-8") as f:
        for line in lines:
            f.write(line + "\r\n")

def read_entire_file(path):
    with codecs.open(path, "r", "utf-8") as f:
        return f.read()

def convert_quote_line(line):
    parts = line.split("|")
    author = parts[1]
    info = "<author>" + author + "</author>"
    text = parts[0]
    text = re.sub(r'\'\'\'(.*?)\'\'\'', r"<i>\1</i>", text)
    text = re.sub(r'\'\'(.*?)\'\'', r"<i>\1</i>", text)
    if len(parts) > 2:
        book = parts[2].replace("] (", "](")
        info += ", <book>" + book + "</book>"
    info = info.replace("\r\n", "")
    info = re.sub(r'\[(.*?) (.*?)\]', r"<a href='\1'>\2</a>", info)
    line = "<quote><cite>" + text + "</cite><span>&mdash; " + info + "</span></quote>"
    return line

cur_quote = []
def convert_quote_to_html(line):
    global cur_quote
    add = None
    if len(cur_quote) == 0:
         if line.startswith("{{quote|"):
             add = line[8:]
         elif line.startswith("{{quotation|"):
             add = line[12:]
    else:
        add = line
    stop = False
    if add is not None:
        if add.strip().endswith("}}"):
            add = add[:-2]
            stop = True
        cur_quote.append(add)
    if len(cur_quote) > 0:
        ret = None
        if stop == True:
            ret = convert_quote_line("\r\n".join(cur_quote))
            cur_quote = []
        return ret
    if line.startswith("__NOTOC__"):
        line = None
    return line

xd = xmltodict.parse(read_entire_file("study.xml"), "utf-8")
for page in xd["mediawiki"]["page"]:
    #print "Reading - " + page["title"]
    name = page["title"].replace(":", "-").replace(" ", "-").lower()
    if name.startswith("talk-"):
        name = name[5:] + "-talk"

    mw_file = name + ".mw"
    md_file = mw_file[:-3] + ".md"
    md_talk_file = mw_file[:-3] + "-talk.md"
    mw_path = os.path.join("mediawiki", mw_file)
    md_path = os.path.join("docs", md_file)
    md_talk_path = os.path.join("docs", md_talk_file)

    print "* [" + page["title"] + "](" + md_path.replace("\\", "/") + ")"

    out = [ "=" + page["title"] + "=", "" ]
    for line in page["revision"]["text"]["#text"].splitlines():
        line = convert_quote_to_html(line)
        if line is not None:
            out.append(line)

    #print "Saving - " + filename
    save_to_file(mw_path, out)
    os.system("pandoc --wrap=none -f mediawiki -t markdown " + mw_path + " -o " + md_path)
    # post-processing
    lines = read_entire_file(md_path)
    out = []
    for line in lines.split("\r\n"):
        if line.startswith("<quote>"):
            line = re.sub(r'\\\[(.*?)\\\]', r"&lsqb;\1&rsqb;", line)
        out.append(line)
    if os.path.exists(md_talk_path):
        out.append("> [Additional Quotes](./" + md_talk_file.replace("\\", "/") + ")")
    save_to_file(md_path, out)
