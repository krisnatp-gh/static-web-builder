from markdown_to_html_node import *

import unittest

class TestMarkdownToHTMLNode(unittest.TestCase):

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

    
    def test_listblock(self):
        md = """
- item A - 1
- item B - 1
- item C - 1

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item A - 1</li><li>item B - 1</li><li>item C - 1</li></ul></div>"
        )

        md = """
1. item 1.1. 
2. item 2.1. 
3. item 3.1. 

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>item 1.1.</li><li>item 2.1.</li><li>item 3.1.</li></ol></div>"
        )
    
    def test_quoteblock(self):
        md = """
> quote1
> quote2
> quote3
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><blockquote>quote1 quote2 quote3</blockquote></div>"
        )

    
    def test_headingblock(self):
        md = """
# Title 1

Lorem ipsum dolor sit amet.

## Subtitle 2

        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title 1</h1><p>Lorem ipsum dolor sit amet.</p><h2>Subtitle 2</h2></div>"
        )