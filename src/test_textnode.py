import unittest

from textnode import TextNode, TextType

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


if __name__ == "__main__":
    unittest.main() # run all test* functions