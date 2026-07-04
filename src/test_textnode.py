import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_links, text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is an italic text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This has a url", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This has a url", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_nourl(self):
        node = TextNode("This has a url", TextType.LINK)
        node2 = TextNode("This has a url", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a BOLD node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a BOLD node")

    def test_italic(self):
        node = TextNode("This is an Italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an Italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev", "alt": "This is an image node"})

    def test_bold_delimiter(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        text_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(text_nodes, [TextNode("This is text with a ", TextType.TEXT),
                                      TextNode("bolded phrase", TextType.BOLD),
                                      TextNode(" in the middle", TextType.TEXT)])

    def test_italic_delimiter(self):
        node = TextNode("This is text with an _italic phrase_ in the middle", TextType.TEXT)
        text_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(text_nodes, [TextNode("This is text with an ", TextType.TEXT),
                                      TextNode("italic phrase", TextType.ITALIC),
                                      TextNode(" in the middle", TextType.TEXT)])

    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` in the middle", TextType.TEXT)
        text_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(text_nodes, [TextNode("This is text with a ", TextType.TEXT),
                                      TextNode("code block", TextType.CODE),
                                      TextNode(" in the middle", TextType.TEXT)])

    def test_delimiter_at_end(self):
        node = TextNode("This is text with a phrase at the end **that is bolded**", TextType.TEXT)
        text_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(text_nodes, [TextNode("This is text with a phrase at the end ", TextType.TEXT),
                                      TextNode("that is bolded", TextType.BOLD)])

    def test_delimiter_at_start(self):
        node = TextNode("**Bolded phrase** at the beginning is strong", TextType.TEXT)
        text_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(text_nodes, [TextNode("Bolded phrase", TextType.BOLD),
                                      TextNode(" at the beginning is strong", TextType.TEXT)])

    def test_bad_delimiter_count(self):
        node = TextNode("This is text with a **bolded phrase in the middle", TextType.TEXT)
        with self.assertRaises(Exception):
            text_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_odd_delimiters(self):
        node = TextNode("This is text with **one bolded phrase** and **two bolded phrases", TextType.TEXT)
        with self.assertRaises(Exception):
            text_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_multiple_delimiters(self):
        node = TextNode("This is text with **one bolded phrase** and **two bolded phrases**", TextType.TEXT)
        text_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(text_nodes, [TextNode("This is text with ", TextType.TEXT),
                                      TextNode("one bolded phrase", TextType.BOLD),
                                      TextNode(" and ", TextType.TEXT),
                                      TextNode("two bolded phrases", TextType.BOLD)])

    def test_multiple_nodes(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        node_2 = TextNode("This is also text with a **bolded phrase** in the middle", TextType.TEXT)
        node_3 = TextNode("This text has no bolded phrase", TextType.TEXT)
        node_4 = TextNode("This text is all bold", TextType.BOLD)
        text_nodes = split_nodes_delimiter([node, node_2, node_3, node_4], "**", TextType.BOLD)
        self.assertEqual(text_nodes, [TextNode("This is text with a ", TextType.TEXT),
                                      TextNode("bolded phrase", TextType.BOLD),
                                      TextNode(" in the middle", TextType.TEXT),
                                      TextNode("This is also text with a ", TextType.TEXT),
                                      TextNode("bolded phrase", TextType.BOLD),
                                      TextNode(" in the middle", TextType.TEXT),
                                      TextNode("This text has no bolded phrase", TextType.TEXT),
                                      TextNode("This text is all bold", TextType.BOLD)])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_images_as_link(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_link_as_image(self):
        matches = extract_markdown_images(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
, matches)
        
    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://google.com) and another [second link](https://www.boot.dev) at the end",
            TextType.TEXT
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" at the end", TextType.TEXT)
            ],
            new_nodes
        )
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        textnodes = text_to_textnodes(text)
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),                            
                            ],
            textnodes
            )









if __name__ == "__main__":
    unittest.main()