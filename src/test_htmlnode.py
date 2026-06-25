import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_propeq(self):
        node = HTMLNode("p", "This is a test node", None, {"href": "https://boot.dev", "target": "_blank"})
        node2 = " href=\"https://boot.dev\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), node2)

    def test_propnoteq(self):
        node = HTMLNode("p", "This is a text node", None, None)
        node2 = " href=\"https://boot.dev\""
        self.assertNotEqual(node.props_to_html(), node2)

    def test_nodeeq(self):
        node = HTMLNode("a", "This is a matching node", None, {"href": "https://google.com", "target": "_blank"})
        node2 = HTMLNode("a", "This is a matching node", None, {"href": "https://google.com", "target": "_blank"})
        self.assertEqual(node, node2)

    def test_nodenoteq(self):
        node = HTMLNode("a", "This is a matching node", None, {"href": "https://google.com", "target": "_blank"})
        node2 = HTMLNode("a", "This is a matching node", None, {"href": "https://google.com"})
        self.assertNotEqual(node, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_with_props(self):
        node = LeafNode("a", "Search Here!", {"href": "www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), "<a href=\"www.google.com\" target=\"_blank\">Search Here!</a>")

    def test_leaf_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError)

    def test_leaf_no_tag(self):
        node = LeafNode(None, "This is some text")
        self.assertEqual(node.to_html(), "This is some text")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_no_child(self):
        node = ParentNode("p", {})
        self.assertRaises(ValueError)

    def test_parent_many_children(self):
        child1 = LeafNode("b", "First Child")
        child2 = LeafNode("i", "Second Child")
        child3 = LeafNode("a", "Third Child", {"href": "https://www.google.com", "target": "_blank"})
        parent_node = ParentNode("p", [child1, child2, child3])
        self.assertEqual(parent_node.to_html(), "<p><b>First Child</b><i>Second Child</i><a href=\"https://www.google.com\" target=\"_blank\">Third Child</a></p>")