from enum import Enum
from htmlnode import ParentNode, LeafNode, HTMLNode
from textnode import text_to_textnodes, text_node_to_html_node, TextNode, TextType


class BlockType(Enum):
    paragraph = ""
    heading = "###### "
    code = "```"
    quote = ">"
    unordered_list = "- "
    ordered_list = "1. "

def block_to_block_type(block: str) -> BlockType:

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
            return BlockType.heading
        
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.code
    
    block_split = block.split("\n")
    
    quote = False
    for line in block_split:
        if line.startswith(">"):
            quote = True
        else:
            quote = False
            break
    if quote:
        return BlockType.quote
    
    unordered_list = False
    for line in block_split:
        if line.startswith("- "):
            unordered_list = True
        else:
            unordered_list = False
            break
    if unordered_list:
        return BlockType.unordered_list
    
    ordered_list = False
    num = 1
    for line in block_split:
        if line.startswith(f"{num}. "):
            
            ordered_list = True
            num += 1
        else:
            
            ordered_list = False
            break
    if ordered_list:
        return BlockType.ordered_list

    return BlockType.paragraph



def markdown_to_blocks(markdown) -> list[str]:
    block_strings: list = []
    split_markdown = markdown.split("\n\n")
    for b in split_markdown:
        if b.strip() == "":
            continue

        block_strings.append(b.strip())


    return block_strings



def markdown_to_html_node(markdown) -> HTMLNode:
    Main_Node: ParentNode = ParentNode("div", [], {})
    
    blocks_list = markdown_to_blocks(markdown)

    for block in blocks_list:
        type = block_to_block_type(block)
        if type == BlockType.paragraph:
            paragraph_node = ParentNode("p", [])
            paragraph_node.children.extend(text_to_children(block, type))
            Main_Node.children.append(paragraph_node)
        if type == BlockType.heading:
            tag_count = 0
            for c in range(0, 6):
                if block[c] == "#":
                    tag_count += 1
                else:
                    break
            heading_node = ParentNode(f"h{tag_count}", [])
            heading_node.children.extend(text_to_header(block, type))
            Main_Node.children.append(heading_node)
        if type == BlockType.code:
            join_string = block.rstrip("`").lstrip("`").lstrip("\n")
            code_node = ParentNode("pre", [text_node_to_html_node(TextNode(join_string,TextType.CODE))])
            Main_Node.children.append(code_node)
        if type == BlockType.quote:
            quote_node = ParentNode("blockquote", [])
            quote_node.children.extend(text_to_children(block, type))
            Main_Node.children.append(quote_node)
        if type == BlockType.unordered_list:
            unordered_node = ParentNode("ul", [])
            unordered_node.children.extend(text_to_lists(block, type))
            Main_Node.children.append(unordered_node)
        if type == BlockType.ordered_list:
            ordered_node = ParentNode("ol", [])
            ordered_node.children.extend(text_to_lists(block, type))
            Main_Node.children.append(ordered_node)

    
    return Main_Node


def text_to_children(text, type) -> list[HTMLNode]:
    children = []
    split_list = text.split("\n")
    join_string = ""
    if type == BlockType.quote:
        new_list = []
        for l in split_list:
            new_list.append(l.lstrip(">").lstrip())
        join_string = " ".join(new_list)
    else:
        join_string = " ".join(split_list)

    textnodes = text_to_textnodes(join_string)

    for node in textnodes:
        children.append(text_node_to_html_node(node))

    return children

def text_to_lists(text, type):
    children = []
    split_list = text.split("\n")

    for item in split_list:
        if type == BlockType.unordered_list:
            item = item[2:]
        else:
            item = item[3:]
        item_node = ParentNode("li", [])
        item_contents = text_to_textnodes(item)
        for content in item_contents:
            new = text_node_to_html_node(content)
            item_node.children.append(new)
        
        children.append(item_node)

    return children

def text_to_header(text, type):
    children = []
    new = ""
    if text.startswith("# "):
        new = text[2:]
    elif text.startswith("## "):
        new = text[3:]
    elif text.startswith("### "):
        new = text[4:]
    elif text.startswith("#### "):
        new = text[5:]
    elif text.startswith("##### "):
        new = text[6:]
    elif text.startswith("###### "):
        new = text[7:]

    split_list = new.split("\n")
    join_string = " ".join(split_list)

    textnodes = text_to_textnodes(join_string)

    for node in textnodes:
        children.append(text_node_to_html_node(node))
    

    return children