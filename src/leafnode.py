from htmlnode import HTMLNode

from textnode import TextNode, TextType


class LeafNode(HTMLNode):
    # LeafNode has no children
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Error: Node has no value.")

        if self.tag is None:
            return str(self.value)
        else:
            return f"<{self.tag}{self.props_to_html()}>{str(self.value)}</{self.tag}>"

    # For display
    def __repr__(self):
        str_representation = f"""HTMLNode(
        tag      = {self._clip_tag()}
        value    = {self._clip_str(self.value)}
        props    = {self._clip_props()}
        )
        """

        return str_representation



def text_node_to_html_node(text_node):
    """
    Convert a Text Node into corresponding Leaf Node

    Args:
        text_node (TextNode): to-be-converted
    
    Output:
        leaf_node (LeafNode): corresponding html node of the input
    """

    if text_node is None:
        raise Exception("Error: input must be a TextNode data type.")
    
    match text_node.text_type:

        case TextType.TEXT:

            return LeafNode(tag=None, 
                            value=text_node.text, 
                            props=None)
        
        case TextType.BOLD | TextType.ITALIC | TextType.CODE:

            return LeafNode(tag=text_node.text_type.value,
                            value=text_node.text,
                            props=None)

        case TextType.LINK:
            text_node_url = text_node.url if text_node.url is not None else ""

            return LeafNode(tag=text_node.text_type.value,
                            value=text_node.text,
                            props={"href": text_node_url})
        
        case TextType.IMAGE:
            text_node_url = text_node.url if text_node.url is not None else ""
            alt_text = text_node.text
    
            return LeafNode(tag=text_node.text_type.value,
                            value="",
                            props={"href": text_node_url, "alt": alt_text})
