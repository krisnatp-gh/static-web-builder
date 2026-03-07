import unittest

from textnode import TextNode, TextType, split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a link node", TextType.IMAGE, "https://www.boot.dev")

        self.assertNotEqual(node, node2)


    def test_neq2(self):
        node = TextNode("This is a text code", TextType.CODE)
        node2 = TextNode("This is a text code", TextType.CODE, "https://www.boot.dev")

        self.assertNotEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")

        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            f"TextNode(This is a text node, {TextType.TEXT.value}, https://www.boot.dev)", repr(node)
        )
    
    def test_delim_bold(self):
        node = TextNode("**ay**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD) # empty string shouldnt be there
        self.assertListEqual(
            [TextNode("ay", TextType.BOLD)],
            new_nodes
        )

        node_2 = TextNode("****", TextType.TEXT)
        new_nodes_2 = split_nodes_delimiter([node_2], "**", TextType.BOLD)
        self.assertListEqual(
            [],
            new_nodes_2
        )


    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)

        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_two_bold(self):
        node = TextNode("**bold1** and **bold2**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual(
            [
                TextNode("bold1" , TextType.BOLD, None), 
                TextNode(" and ", TextType.TEXT, None), 
                TextNode("bold2", TextType.BOLD, None) 
            ],
            new_nodes
        )

    
    def test_delim_nested_bold(self):
        node = TextNode("**The words: not all who **wander** are **lost****", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertListEqual(
            [
                TextNode("The words: not all who " , TextType.BOLD, None), 
                TextNode("wander", TextType.TEXT, None), 
                TextNode(" are ", TextType.BOLD, None), 
                TextNode("lost", TextType.TEXT, None)
            ],
            new_nodes
        )

    

        node_2 = TextNode("**bold1 **and** bold2** word", TextType.TEXT) # **and** should be bold (?) but I guess I can ignore nested inlines for now

        new_nodes_2 = split_nodes_delimiter([node_2], "**", TextType.BOLD)
        
        self.assertListEqual(
            [
                TextNode("bold1 ", TextType.BOLD, None), 
                TextNode("and", TextType.TEXT, None), 
                TextNode(" bold2", TextType.BOLD, None), 
                TextNode(" word", TextType.TEXT, None)
            ],
            new_nodes_2
        )






if __name__ == "__main__":
    unittest.main() # run all test* functions