from blocktype import markdown_to_blocks, block_to_blocktype, BlockType

def extract_title(markdown):
    block_list = markdown_to_blocks(markdown)
    for block in block_list:
        if block_to_blocktype(block) is BlockType.HEADING_1:
            # strip hashtag and leading/trailing whitespace
            title = block.lstrip("#").strip()
            return title
    
    # Pass: no h1 found
    raise Exception("Error: no h1 header found.")