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
    
    def test_split_nodes_delimiter(self):
        node = TextNode("**bold1 **and** bold2** word", TextType.TEXT) # **and** should be bold (?) but I guess I can ignore nested inlines for now
        output = split_nodes_delimiter([node], "**", TextType.BOLD)
        print(output)

        node = TextNode("**bold1** and **bold2**", TextType.TEXT) # 'and' shouldnt be bold here
        output = split_nodes_delimiter([node], "**", TextType.BOLD)
        print(output)


        node = TextNode("**ay**", TextType.TEXT)
        output = split_nodes_delimiter([node], "**", TextType.BOLD) # empty string shouldnt be there
        print(output)

        # node = TextNode("****", TextType.TEXT)
        # output = split_nodes_delimiter([node], "**", TextType.BOLD)
        # print(output)

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

        print(new_nodes)


if __name__ == "__main__":
    unittest.main() # run all test* functions