from leafnode import LeafNode
from parentnode import ParentNode

import unittest

class TestParentNode(unittest.TestCase):

    def test_parent_with_children(self):    
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node= LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_html_with_multiple_children(self):
        node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    ParentNode("span", [LeafNode("b", "aiaiaou"), LeafNode("a", "gugle", {"href": "https://www.google.com", "target": "_blank",})]),
                    LeafNode(None, "Normal text"),
                ],
            )
        

        self.assertEqual(
            node.to_html(),
            '<p><b>Bold text</b>Normal text<span><b>aiaiaou</b><a href="https://www.google.com" target="_blank">gugle</a></span>Normal text</p>'
        )

