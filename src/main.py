from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    Test2 = HTMLNode("p", "Test Two", None, None)
    Test = HTMLNode("p", "Test Node", [Test2], {"href": "https://www.google.com", "target": "_blank",})
    print(Test)



main()