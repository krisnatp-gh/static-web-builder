from enum import Enum

class TextType(Enum):
    TEXT = ""
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    LINK = "a"
    IMAGE = "img"


def is_valid_delimiter(text_type, delimiter):
    # Check whether text_type, delimiter combination is valid
    match (text_type, delimiter):

        case (TextType.BOLD, "**"):
            return True

        case (TextType.ITALIC, "_"):
            return True

        case (TextType.CODE, "`") | (TextType.CODE, "```"):
            return True
        
        case _:
            return False
    


class TextNode():
    
    def __init__(self, text, text_type, url=None):
        self.text= text
        self.text_type = text_type
        self.url = url

    
    def __eq__(self, other):
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url
                )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Recursive. 
    Create a list of TextNode(s) inside their innermost delimiter. 
    Each TextNode has the proper TextType and no nested delimtier.

    Args:
        old_nodes (list of TextNodes): list of TextNodes
        delimiter (string): delimiter to exctract
        text_type (TextType): text type of the delimiter to extract

    Returns:
        list of TextNodes: list of text nodes inside the delimiter
    """
    if not is_valid_delimiter(text_type, delimiter):
        raise ValueError(f"Error: {text_type} does not match delimiter {delimiter}")

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # you only want to split nodes when the text is nonempty
        if len(node.text) < 1:
            continue

        # If a node is a nonempty text node, then split recursively to find delimiters
        splitted_by_delimiter_list = node.text.split(delimiter, maxsplit=2)

        # base case
        if len(splitted_by_delimiter_list) == 1: # only one item: no delimiter, is text type
            new_nodes.append(node)
            continue

        if len(splitted_by_delimiter_list) == 2: # no closing delimiter detected
            raise SyntaxError("Error: Invalid markdown syntax")

        # pass above: have three items separated by delimiter
        first, target, nested = splitted_by_delimiter_list

        # if text starts with delimiter, then first item is a bold node
        # append the nonempty text as delimiter type node
        if node.text.startswith(delimiter) and len(first) > 0:              
            new_nodes.append(TextNode(first, text_type))
        
        # if text is nonempty but does not start with delimiter, then first item is a text node
        # append the nonempty text as text node
        elif not node.text.startswith(delimiter) and len(first) > 0:       
            new_nodes.append(TextNode(first, TextType.TEXT))
        
        target_node = TextNode(target, text_type)      # second item, is guaranteed to be text_type
        
        nested_node = TextNode(nested, TextType.TEXT)  # third item, may contain nested delimiters
        
        temp_nodes = split_nodes_delimiter([nested_node], delimiter, text_type) # recursively get delimiter nested nodes

        if len(target) > 0:
            new_nodes.append(target_node)

        new_nodes.extend(temp_nodes)

                


    return new_nodes




