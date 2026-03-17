from leafnode import *

import unittest

class TestLeafNode(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(TypeError) as context:
            node = LeafNode(tag='p', value="Lorem ipsum dolor sit amet, consectetur adipiscing elit", children=[])

        with self.assertRaises(TypeError) as context:
            node = LeafNode(tag='p', value="Lorem ipsum dolor sit amet, consectetur adipiscing elit", children=None)



    def test_repr(self):
        node = LeafNode(tag='b', value="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua")

        str_representation = f"""HTMLNode(
        tag      = b
        value    = 'Lorem ipsum...' (n_chars = 122)
        props    = 
        )
        """
        
        self.assertEqual(str_representation, repr(node))

    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"}) # with tag and props
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')

        node3 = LeafNode(tag='p', value="") # no value
        self.assertEqual(node3.to_html(), '<p></p>')

        node4 = LeafNode(tag=None, value="Hello World!") # no tag
        self.assertEqual(node4.to_html(), "Hello World!")

    
    def test_text_node_to_html_node(self):
        # Text Node
        text_node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "This is a text node")

    
    def test_bold_node_to_html_node(self):
        # Bold Node
        text_node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        self.assertEqual(html_node.to_html(), "<b>This is a bold node</b>")

    def test_italic_node_to_html_node(self):
        # Italic Node
        text_node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
        self.assertEqual(html_node.to_html(), "<i>This is an italic node</i>")

    
    def text_code_node_to_html_node(self):
        # Code Node
        text_node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        self.assertEqual(html_node.to_html(), "<code>This is a code node</code>")
    

    def test_link_node_to_html_node(self):
        # Link Node
        text_node = TextNode(text="bootdev front page",
                              text_type=TextType.LINK,
                              url="https://www.boot.dev/")

        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "bootdev front page")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev/"})
        self.assertEqual(html_node.to_html(), '<a href="https://www.boot.dev/">bootdev front page</a>')
    
    def test_image_node_to_html_node(self):
        # Image Node
        text_node = TextNode(text="dinosaurs comic",
                              text_type=TextType.IMAGE,
                              url="https://xkcd.com/3204/")
        
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://xkcd.com/3204/", "alt":"dinosaurs comic"})
        self.assertEqual(html_node.to_html(), '<img src="https://xkcd.com/3204/" alt="dinosaurs comic" />')

        


