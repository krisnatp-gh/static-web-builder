from enum import Enum
import re

class BlockType(Enum):
# For denoting type of markdown blocks. The values correspond to the HTML tags of the markdown block.
    PARAGRAPH  = "p"
    HEADING_1  = "h1"
    HEADING_2  = "h2"
    HEADING_3  = "h3"
    HEADING_4  = "h4"
    HEADING_5  = "h5"
    HEADING_6  = "h6"
    CODE       = "code"
    QUOTE      = "blockquote"
    UNORD_LIST = "ul"
    ORD_LIST   = "ol"


HEADER_HASHTAG_COUNT_DICT = {
    1: BlockType.HEADING_1,
    2: BlockType.HEADING_2,
    3: BlockType.HEADING_3,
    4: BlockType.HEADING_4,
    5: BlockType.HEADING_5,
    6: BlockType.HEADING_6
}



def block_to_blocktype(markdown):
    """
    Infer BlockType based on the provided markdown block.

    Args:
        markdown (str): markdown block for which the type is to be inferred

    Returns:
        BlockType: type of the markdown block.
    """

    if re.match(r"#{1,6} .+", markdown):
        hashtag_count = markdown.count("#", 0, 6)
        header = HEADER_HASHTAG_COUNT_DICT[hashtag_count]
        return header
        
    if markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE
    
    # The rest of the checks below might have multiple lines
    md_lines = markdown.split("\n")
    

    if markdown.startswith(">"):
        for md in md_lines:
            if not md.startswith(">"):
                return BlockType.PARAGRAPH
        # pass: all lines starts with ">"
        return BlockType.QUOTE
    

    if markdown.startswith("- "):
        for md in md_lines:
            if not md.startswith("- "):
                return BlockType.PARAGRAPH
        # pass: all lines starts with "- "
        return BlockType.UNORD_LIST
        
    if markdown.startswith("1. "):
        n_lines = len(md_lines)
        if n_lines == 1:
            return BlockType.ORD_LIST

        for i in range(1, n_lines):
            if not md_lines[i].startswith(f"{i+1}. "):
                return BlockType.PARAGRAPH
        # pass: all lines start  with sequential numbers
        return BlockType.ORD_LIST

    # pass all: is paragraph block
            
    return BlockType.PARAGRAPH
    


def markdown_to_blocks(markdown):
    """
    Split a markdown block (string) into a list of inline markdowns.
    Markdown blocks are separated by two newlines.

    Args:
        markdown (str): markdown block

    Returns:
        cleaned_blocks (list of str): list of inline markdowns
    """
    pre_blocks = markdown.split("\n\n")
    cleaned_blocks = []


    for block in pre_blocks:
        clean_block = block.strip()
        if len(clean_block) > 1:
            cleaned_blocks.append(clean_block)
    
    return cleaned_blocks