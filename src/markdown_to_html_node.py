from functools import partial

from blocktype import BlockType, block_to_blocktype, markdown_to_blocks
from block_to_html_node import *

from parentnode import ParentNode

BLOCKTYPE_TO_HTML_NODE_FUNCTION_MAP = {
    # Maps heading block types to function that convert the text into header node
    BlockType.HEADING_1: partial(text_to_header_node, header_block_type = BlockType.HEADING_1),
    BlockType.HEADING_2: partial(text_to_header_node, header_block_type = BlockType.HEADING_2),
    BlockType.HEADING_3: partial(text_to_header_node, header_block_type = BlockType.HEADING_3),
    BlockType.HEADING_4: partial(text_to_header_node, header_block_type = BlockType.HEADING_4),
    BlockType.HEADING_5: partial(text_to_header_node, header_block_type = BlockType.HEADING_5),
    BlockType.HEADING_6: partial(text_to_header_node, header_block_type = BlockType.HEADING_6),

    # Maps paragraph block type to function that convert the text into paragraph node
    BlockType.PARAGRAPH: text_to_paragraph_node,

    # Maps code block type to function that convert the text into code node
    BlockType.CODE: text_to_code_node,

    # Maps quote block type to function that convert the text into quote node
    BlockType.QUOTE: text_to_quote_node,

    # Maps list block types to function that convert the text into list node
    BlockType.UNORD_LIST: partial(text_to_list_node, list_block_type = BlockType.UNORD_LIST),
    BlockType.ORD_LIST: partial(text_to_list_node, list_block_type = BlockType.ORD_LIST)

}

def markdown_to_html_node(markdown):
    """
    Split a markdown text into blocks -> Convert each block into appropriate HTML nodes -> Return a ParentNode containing HTMLNode converted from each blocks as its children

    Args:
        markdown (str): markdown text 

    Returns:
        ParentNode: div HTML node containing HTMLNodes converted from each blocks as its content
    """

    blocks_list = markdown_to_blocks(markdown)
    
    div_content_children = []
    for block in blocks_list:
        block_type = block_to_blocktype(block)

        conversion_func = BLOCKTYPE_TO_HTML_NODE_FUNCTION_MAP[block_type]

        block_content_node = conversion_func(block)
        
        div_content_children.append(block_content_node)
    
    div_content_parent = ParentNode(tag = "div",
                                    children = div_content_children)
    
    return div_content_parent



