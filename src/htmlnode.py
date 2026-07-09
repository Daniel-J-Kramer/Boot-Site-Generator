from __future__ import annotations

class HTMLNode:

    def __init__(self, tag: str | None = None, value: str | None = None, children: list[HTMLNode] | None = None, props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Sorry, not yet implemented")
    
    def props_to_html(self):
        final = ""
        if self.props != None:
            for p in self.props:
                final += f" {p}=\"{self.props[p]}\""
        return final
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
    
    def __eq__(self, other: HTMLNode):
        if self.tag == other.tag:
            if self.value == other.value:
                if self.children == other.children:
                    if self.props == other.props:
                        return True
                    
        return False
    
class LeafNode(HTMLNode):

    def __init__(self, tag: str | None, value: str | None, props: dict | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag == "img":
            return f'<{self.tag}{self.props_to_html()}>'

        if self.value == None:
            raise ValueError("Must have a value")
        
        if self.tag == None:
            return self.value
        
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props_to_html()})'
    
class ParentNode(HTMLNode):

    def __init__(self, tag: str, children: list[HTMLNode], props: dict | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Must have a tag")
        
        if self.children == {} or self.children == None:
            raise ValueError("Must have children")
        else:
            children_string = ""
            for c in self.children:
                children_string += c.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_string}</{self.tag}>"