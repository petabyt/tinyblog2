# pip3 install marko bottle
import os, html, re, marko
from datetime import date
from bottle import *

def getIndex():
    fp = open("index.html", "r")
    index = fp.read()
    fp.close()
    return index

def getMatch(a):
    return a.groups(0)[0]

def sanitizeTitle(title):
    title = title.lower()
    title = re.sub(r'[^a-z 0-9/-]', '', title)
    title = title.replace(" ", "-")
    title = title.replace("/", "-")
    return title

# Parse as tbmd, a very special version of markdown
# return url, date, text
def parse(text, showMore):
    url = ""
    dateStr = ""

    lines = text.split("\n")

    # post metadata length in lines
    metadataLength = 0

    # Parse custom url if present
    if text[0] == ":":
        url = lines[0][1:]
        metadataLength += 1
    else:
        url = sanitizeTitle(lines[metadataLength])
    
    title = lines[metadataLength]
    metadataLength += 1

    dateStr = lines[metadataLength]
    metadataLength += 1

    # Set offset to whatever is after metadata
    offset = 0
    for i in range(0, metadataLength):
        offset += len(lines[i]) + 1

    # Skip trailing whitespace
    while text[offset] == "\n" or text[offset] == " ":
        offset += 1

    text = text[offset:]

    text = html.escape(text)

    if showMore:
        text = text.replace("---", "<hr>")
    else:
        text = re.sub(r"---(.+)", r"<a href='" + url + "'>Read more</a>", text, flags=re.S)

    text = re.sub(r"## (.+)", r"<h2>\1</h2>", text)
    text = re.sub(r"# (.+)", r"<h1>\1</h1>", text)

    inBetween = "([^\n|\[\]\(\)]+)";

    # Images
    text = re.sub(r"\!\[([^\n|\[\]\(\)]+)\]\(([^\n|\[\]\(\)]+)\)",
        r"<a href='\2'><img width='300' src='\2' alt='\1' title='\1'></a>", text)
    
    # Links
    text = re.sub(r"(?!\!)\[([^\n|\[\]\(\)]+)\]\(([^\n|\[\]\(\)]+)\)",
        r"<a href='\2'>\1</a>", text)
    
    # Code blocks
    text = re.sub(r"```\n([^```]+)```", r"<code class='long'>\1</code>", text)
    
    # Single code blocks
    text = re.sub(r"\`([^\n`]+)\`", r"<code>\1</code>", text)
    
    # Bold, then italics
    text = re.sub(r"\*\*([^\n\*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*([^\n\*]+)\*", r"<i>\1</i>", text)
    
    text = text.replace("\n", "<br>")
    
    text = "<h1>" + title + "</h1>" + text

    return url, title, dateStr, text

def getPosts():
    content = ""
    files = os.listdir("posts/")

    for i in range(len(files), 0, -1):
        fp = open("posts/" + str(i))
        post = fp.read()
        fp.close()

        if post[0:5] == ":skip":
            continue

        url, title, dateStr, post = parse(post, False)

        content += "<div class='post' title='Post #" + str(i) + "'>" + post + "</div>"
    return content

def getPost(name):
    content = ""
    files = os.listdir("posts/")

    for i in range(len(files), 0, -1):
        fp = open("posts/" + str(i))
        post = fp.read()
        fp.close()

        if post[0:5] == ":skip":
            continue

        url, title, dateStr, post = parse(post, True)
        if url == name:
            return title, "<div class='post' title='Post #" + str(i) + "'>" + post + "</div>"
    return "Post not found", "<p class='center'>Post not found.</p>"

def getPostByID(num):
    content = ""

    if not num.isnumeric():
        return "404"

    try:
        fp = open("posts/" + str(num), "r")
    except:
        return "404"
    post = fp.read()
    fp.close()

    if post[0:5] == ":skip":
        return "404"

    url, title, dateStr, post = parse(post, True)
    return url

@route("/")
def main():
    if request.params.get('post') is not None:
        redirect(getPostByID(request.query["post"]))

    return template(
        getIndex(),
        posts=getPosts(),
        title="Daniel's 'Stuff'"
    )

@route("/index.php")
def main():
    if request.params.get('post') is not None:
        redirect(getPostByID(request.query["post"]))
    redirect("/")


@route("/<post>")
def post(post):
    title, content = getPost(post)
    return template(
        getIndex(),
        posts=content,
        title=title
    )

@route("/rss.xml")
def rss():
    domain = "https://petabyt.dev/blog"
    title = "Daniel's Blog"
    desc = "This is the place where I put stuff"

    response.content_type = "text/xml; charset=utf-8"

    content = """<?xml version="1.0" encoding="UTF-8"?>
    <rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">
        <channel>
          <title>""" + title + """</title>
            <link>""" + domain + """</link>
            <description>""" + desc + """</description>
            <generator>Tinyblog</generator>
            <language>en</language>
            <lastBuildDate>""" + date.today().strftime("%Y-%m-%d") + """</lastBuildDate>
    """
    
    files = os.listdir("posts/")

    for i in range(len(files), 0, -1):
        fp = open("posts/" + str(i))
        post = fp.read()
        fp.close()

        if post[0:5] == ":skip":
            continue

        url, title, dateStr, post = parse(post, False)

        content += """
            <item>
            <title>""" + title + """</title>
            <pubDate>""" + dateStr + """</pubDate>
            <link>""" + domain + """/""" + url + """</link>
            </item>"""
    content += """
        </channel>
    </rss>
    """
    return content

@route("/image")
def post(post):
    redirect("")

run(host='localhost', port=7000)
