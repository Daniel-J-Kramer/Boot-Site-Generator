from __future__ import annotations
from enum import Enum
import types
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "Regular Text"
    BOLD = "**Bold text"
    ITALIC = "_Italic text_"
    CODE = "'Code text'"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

class TextNode:
    
    def __init__(self, TEXT: str, TEXT_TYPE: TextType, URL: str | None =None):
        self.text: str = TEXT
        self.text_type = TEXT_TYPE
        self.url: str | None = URL

    def __eq__(self, other: TextNode):

        if self.text == other.text:
            if self.text_type == other.text_type:
                if self.url == other.url:
                    return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node: TextNode) -> LeafNode | None:
    if text_node.text_type not in TextType:
        raise Exception("Must have a valid TextType")
    
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
    
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            node_list = node.text.split(delimiter)
            text_list = []
            if len(node_list) % 2 == 0:
                raise Exception("Missing closing delimiter")
            else:
                for n in range(0, len(node_list)):
                    if n % 2 == 0:
                        text_list.append(TextNode(node_list[n], TextType.TEXT))
                    else:
                        text_list.append(TextNode(node_list[n], text_type))

                if text_list[-1].text == "":
                    text_list.pop(-1)
                
                if text_list[0].text == "":
                    text_list.pop(0)

            new_nodes.extend(text_list)




    return new_nodes