import re
from config import HEADER_BLOCK_MARKER, CODE_BLOCK_MARKER, QUOTE_BLOCK_MARKER, UNORDERED_LIST_BLOCK_MARKER, ORDERED_LIST_BLOCK_MARKER

from blocktype import BlockType
from parentnode import ParentNode
from leafnode import LeafNode, text_node_to_html_node
from textnode import TextNode, text_to_textnodes




def text_to_code_node(text):
    """
    Accept a markdown block containing a code block, convert it into code html node.

    Args:
        text (str): markdown block

    Returns:
        ParentNode_: code block with a single children with pre tag. The children is the content of the code block (not separated into appropriate leaf node html tags)
    """

    cleaned_text = text.strip() # Remove possible leading newlines/spaces before the triple backticks
    cleaned_text = cleaned_text.strip(CODE_BLOCK_MARKER) # remove leading and trailing triple backgticks from the ends
    cleaned_text = cleaned_text.lstrip() # Remove possible leading spaces/newlines/tabs within the code block
    
    pre_node = LeafNode(tag = BlockType.CODE.value,          # Code html node need to have one child node with a pre tag.
                        value = cleaned_text) # Note: content of code block is represented as it is with no inline markdown parsing
    
    code_node = ParentNode(tag = "pre",             # For Code blocks (not inline blocks), it is enclosed by pre tag outside the code tag
                           children = [pre_node])

    return code_node


def text_to_header_node(text, header_block_type):
    """
    Accept a markdown block containing a header block, convert it into quote html node.

    Args:
        text (str): markdown block
        header_block_type (str): type of the header block (h1 up to h6)

    Returns:
        ParentNode: header node with its children separated into the appropriate leaf node html tags (bold, italics, etc.)
    """

    cleaned_text = re.sub(HEADER_BLOCK_MARKER, "", text, count=1) # Remove the leading hashtags from the text
    child_nodes = text_to_children(cleaned_text)
    header_node = ParentNode(tag = header_block_type.value,
                             children = child_nodes)
    
    return header_node


def text_to_paragraph_node(text):
    """
    Accept a markdown block containing a paragraph block, convert it into quote html node.
    Note: Newlines are ignored and become spaces during conversion.

    Args:
        text (str): markdown block

    Returns:
        ParentNode: paragraph node with its children separated into the appropriate leaf node html tags (bold, italics, etc.)
    """
    
    lines = text.split("\n")
    paragraph_item_nodes = []
    for line in lines:
        cleaned_line = line.strip()
        if line != lines[-1]:
            cleaned_line += " " # Add final space at the end to replace the deleted newline in between lines
        
        child_nodes = text_to_children(cleaned_line)
        paragraph_item_nodes.extend(child_nodes)
    
    paragraph_node = ParentNode(tag = BlockType.PARAGRAPH.value,
                                children = paragraph_item_nodes)
    return paragraph_node

def text_to_quote_node(text):
    """
    Accept a markdown block containing a quote markdown block (each line starts with a '>'), convert it into quote html node
    Note: Newlines are ignored and become spaces during conversion.

    Args:
        text (str): markdown block

    Returns:
        ParentNode: quote node with its children separated into the appropriate leaf node html tags (bold, italics, etc.)
    """

    lines = text.split("\n")
    quote_item_nodes = []
    for line in lines:
        cleaned_line = re.sub(QUOTE_BLOCK_MARKER, "", line, count=1) # Remove the leading quote marker from the text
        cleaned_line = cleaned_line.strip()
        if line != lines[-1]:
            cleaned_line += " "  # Add final space at the end to replace the deleted newline in between lines
        

        child_nodes = text_to_children(cleaned_line)
        quote_item_nodes.extend(child_nodes)
    
    quote_node = ParentNode(tag = BlockType.QUOTE.value, 
                            children = quote_item_nodes)
    
    return quote_node
        


def text_to_list_node(text, list_block_type):
    """
    Accept a markdown block containing list (ordered or unordered), convert it into a list html node.

    Args:
        text (str): markdown block containing list items
        list_block_type (str): list type of the block (ordered or unordered list)

    Returns:
        ParentNode: list node with its list items as its children
    """

    match list_block_type:
        # match the markers to remove later from each item using regex
        case BlockType.UNORD_LIST:
            item_marker = UNORDERED_LIST_BLOCK_MARKER
        case BlockType.ORD_LIST:
            item_marker = ORDERED_LIST_BLOCK_MARKER
        
        case _:
            raise Exception("Error: list_block_type must be 'ul' for unordered list or 'ol' for ordered list.")
    
    lines = text.split("\n")
    item_nodes = []
    for line in lines:
        cleaned_line = re.sub(item_marker, "", line, count=1) # Remove the leading list item marker from the text
        cleaned_line = cleaned_line.strip() # Remove trailing white spaces from the text

        child_nodes = text_to_children(cleaned_line)
        
        item_node = ParentNode(tag = "li",
                                    children = child_nodes)
        
        item_nodes.append(item_node)
    
    list_node = ParentNode(tag = list_block_type.value,
                           children = item_nodes)
    
    return list_node


    

def text_to_children(text):
    """
    Convert a markdown text -> split into list of TextNodes based on delimiters -> LeafNodes.
    
    Assumption: input text already has block markdown markers removed

    Args:
        text (str): markdown text to be converted

    Returns:
        list of LeafNodes: converted from markdown text
    """
    text_nodes = text_to_textnodes(text)
    child_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return child_nodes
    