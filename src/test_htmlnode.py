from htmlnode import HTMLNode

import unittest

class TestHTMLNode(unittest.TestCase):
    
    def test_repr(self):
        node = HTMLNode(value="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua")

        str_representation = f"""HTMLNode(
        tag      = 
        value    = 'Lorem ipsum...' (n_chars = 122)
        children = 
        props    = 
        )
        """
        
        self.assertEqual(str_representation, repr(node))


    def test_to_html(self):
        node = HTMLNode(tag="a", props={"href": "https://www.google.com", "target": "_blank"})
        with self.assertRaises(NotImplementedError) as context:
            node.to_html()

    
    def test_props_to_html(self):
        node = HTMLNode(tag="a", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())


    

if __name__ == "__main__":
    test_htmlnode.main() # run all test* functions