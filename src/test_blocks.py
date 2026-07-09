import unittest
from blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node



class TestBlocks(unittest.TestCase):

        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        block = "This is some normal text for a paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.paragraph, block_type)

    def test_block_to_heading_type(self):
        block = "#### This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(BlockType.heading, block_type)

    def test_block_to_bad_heading(self):
        block = "#This is a heading"
        type = block_to_block_type(block)
        self.assertEqual(BlockType.paragraph, type)

    def test_block_to_code_type(self):
        block = """```
        This is a code block```"""
        self.assertEqual(BlockType.code, block_to_block_type(block))

    def test_block_to_bad_code(self):
        block = """```This is a code block```"""
        self.assertEqual(BlockType.paragraph, block_to_block_type(block))

    def test_block_to_quote_type(self):
        block = """>This is a quote block
> It is multiline too"""
        self.assertEqual(BlockType.quote, block_to_block_type(block))

    def test_block_to_bad_quote(self):
        block = """>This is a quote block
It is multiline too"""
        self.assertEqual(BlockType.paragraph, block_to_block_type(block))

    def test_block_to_unordered_type(self):
        block = """- This is an unordered list
- It is multiline as well"""
        self.assertEqual(BlockType.unordered_list, block_to_block_type(block))
    
    def test_block_to_bad_unordered(self):
        block = """- This is an unordered list
-It is multiline too"""
        self.assertEqual(BlockType.paragraph, block_to_block_type(block))

    def test_block_to_ordered_type(self):
        block = """1. This is an ordered list
2. It counts up as it goes on
3. It is also multiline"""
        self.assertEqual(BlockType.ordered_list, block_to_block_type(block))

    def test_block_to_bad_ordered(self):
        block = """1. This is an ordered list
2. It counts up as it goes on
30. It is also multiline"""
        self.assertEqual(BlockType.paragraph, block_to_block_type(block))

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headingblock(self):
        md = """
#### This is text for a heading of four
and it will have inline _italic_ and **bold** words
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h4>This is text for a heading of four and it will have inline <i>italic</i> and <b>bold</b> words</h4></div>"
        )

    def test_quoteblock(self):
        md = """
> This is a **bold quote block**
>It also has inline and `code` too
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <b>bold quote block</b> It also has inline and <code>code</code> too</blockquote></div>"
        )

    def test_unorderedblock(self):
        md = """
- This is an unordered list
- It has `code` and _italic_ in it
- It is very **bold** too
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is an unordered list</li><li>It has <code>code</code> and <i>italic</i> in it</li><li>It is very <b>bold</b> too</li></ul></div>"
        )

    def test_orderedblock(self):
        md = """
1. This is an ordered list
2. It has _italic_ and **bold** in it
3. It has an ![image](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwallpaperaccess.com%2Ffull%2F1101027.jpg&f=1&nofb=1&ipt=91c8fcc8a7ad474746dfcbe33577546e35fd66e70fd63e6ee50b8b004af9fda5) as well
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is an ordered list</li><li>It has <i>italic</i> and <b>bold</b> in it</li><li>It has an <img src=\"https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwallpaperaccess.com%2Ffull%2F1101027.jpg&f=1&nofb=1&ipt=91c8fcc8a7ad474746dfcbe33577546e35fd66e70fd63e6ee50b8b004af9fda5\" alt=\"image\"> as well</li></ol></div>"
        )

    def test_full_markdown_document(self):
        self.maxDiff = None
        md = """
# Heading 1

This paragraph has **bold**, _italic_, `code`, a [link](https://example.com), and an ![image](https://example.com/image.png).

## Heading 2

> This is a quote with **bold** text
> and _italic_ text too

### Heading 3

- First unordered item
- Second unordered item with `code`
- Third unordered item with a [link](https://example.com/list)

#### Heading 4

1. First ordered item
2. Second ordered item with **bold**
3. Third ordered item with an ![image](https://example.com/list-image.png)

##### Heading 5

```
This is text that _should_ remain
the **same** even with inline stuff
```

###### Heading 6
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            '<div>'
            '<h1>Heading 1</h1>'
            '<p>This paragraph has <b>bold</b>, <i>italic</i>, <code>code</code>, a <a href="https://example.com">link</a>, and an <img src="https://example.com/image.png" alt="image">.</p>'
            '<h2>Heading 2</h2>'
            '<blockquote>This is a quote with <b>bold</b> text and <i>italic</i> text too</blockquote>'
            '<h3>Heading 3</h3>'
            '<ul><li>First unordered item</li><li>Second unordered item with <code>code</code></li><li>Third unordered item with a <a href="https://example.com/list">link</a></li></ul>'
            '<h4>Heading 4</h4>'
            '<ol><li>First ordered item</li><li>Second ordered item with <b>bold</b></li><li>Third ordered item with an <img src="https://example.com/list-image.png" alt="image"></li></ol>'
            '<h5>Heading 5</h5>'
            '<pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre>'
            '<h6>Heading 6</h6>'
            '</div>',
        )