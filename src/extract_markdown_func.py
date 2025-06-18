import re



def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    



# the first bracket filters out ! preceding [, to avoid extracting images by mistake.
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_title(markdown):
    title = re.findall(r"^#\s+(.+)", markdown, re.MULTILINE)
    if not title:
        raise ValueError("title not found")
    return title[0]



