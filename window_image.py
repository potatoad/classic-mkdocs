from pathlib import Path
import urllib.parse
import xml.etree.ElementTree as etree
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension


class WindowImageProcessor(Treeprocessor):
    def run(self, root):
        # 1. Collect all images first to avoid infinite loops during iteration
        targets = []
        for parent in root.iter():
            for child in parent:
                if child.tag == "img":
                    targets.append((parent, child))

        # 2. Modify the tree using our collected list
        for parent, child in targets:
            # Find exactly where the image is inside its parent
            index = list(parent).index(child)
            filename = child.attrib.get("src", "image")
            
            # Create the outer "window" div
            window_div = etree.Element(
                "div",
                {
                    "class": "window active image-window",
                    "style": "max-width: fit-content; max-height: fit-content;",
                },
            )

            # Create the title bar structure
            title_bar = etree.SubElement(window_div, "div", {"class": "title-bar"})
            title_bar_text = etree.SubElement(
                title_bar, "div", {"class": "title-bar-text"}
            )
            title_bar_text.text = urllib.parse.unquote(Path(filename).name)

            # Create the window body
            window_body = etree.SubElement(window_div, "div", {"class": "window-body window-image"})

            # Move the original <img> element inside the window-body div
            window_body.append(child)

            # Replace the original <img> in the document tree with our new structure
            parent[index] = window_div


class WindowImageExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(WindowImageProcessor(md), "window_image", 15)


def makeExtension(**kwargs):
    return WindowImageExtension(**kwargs)
