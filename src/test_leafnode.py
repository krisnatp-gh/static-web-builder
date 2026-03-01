from leafnode import LeafNode

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


if __name__ == "__main__":
    test_leafnode.main() # run all test* functions