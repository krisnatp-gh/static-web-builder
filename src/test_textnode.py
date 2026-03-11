import unittest

from textnode import TextNode, TextType, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

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

    

        node_2 = TextNode("**bold1 **and** bold2** word", TextType.TEXT)

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

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            new_nodes
        )


    def test_split_two_images(self):
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


    
    def test_split_two_links(self):
        node = TextNode(
            "This is text with a [link](https://google.com/search?q=how+to+basic) and another [second link](https://www.google.com)",
            text_type = TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("link", TextType.LINK, "https://google.com/search?q=how+to+basic"),
                TextNode(" and another " ,TextType.TEXT, None),
                TextNode("second link", TextType.LINK, "https://www.google.com")
            ],
            new_nodes
        )


    def test_split_images_and_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node]) # split by link
        new_nodes = split_nodes_image(new_nodes) # split by images
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT, None), 
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), 
                TextNode(" and a ", TextType.TEXT, None), 
                TextNode("link", TextType.LINK, "https://www.google.com")
            ],
            new_nodes
        )

    
    def test_text_totextnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
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
            new_nodes
        )

if __name__ == "__main__":
    unittest.main() # run all test* functions