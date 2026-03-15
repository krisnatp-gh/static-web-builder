from blocktype import markdown_to_blocks, block_to_blocktype, BlockType

import unittest


class TestSplitBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    
    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph but with following excessive new lines


- This is a list
- with items


    """

        blocks = markdown_to_blocks(md)        
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph but with following excessive new lines",
                "- This is a list\n- with items",
            ],
        )
    
    
    def test_block_to_blocktype_header(self):
        md = "# Title 1"
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.HEADING_1)

        md = "## Title 2"
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.HEADING_2)

        md = "###### Title 3"
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.HEADING_6)

        
        md = "####### Title 4" # 7 hashtags -> should be treated as paragraph
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    
    def test_block_to_blocktype_paragraph(self):
        md = "This is another paragraph with _italic_ text and `code` here.\nThis is the same paragraph on a new line"
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_block_to_blocktype_list(self):
        md = "- Item A\n- Item B\n- Item C"
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.UNORD_LIST)

    def test_block_to_blocktype_ordered_list(self):
        md = "1. aaa\n2. bbb\n3. ccc"
        block_type = block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.ORD_LIST)


    def test_block_to_blocktype_combined(self):
        md = """

# Title 1

This is **bolded** paragraph

## Subtitle

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

# Title 2

and a code block:

```
for i in range(5):
    print("Hello!")
```

and an ordered list:

1. aaa
2. bbb
3. ccc

And a quote:

> ...
> ...
> ...
        """

        blocks = markdown_to_blocks(md)
        # print("\n")
        block_types = []
        for block in blocks:
            block_type = block_to_blocktype(block)
            block_types.append(block_type)
            # print(f"{block_type}\n {block}\n")
        self.assertListEqual(
            [
                BlockType.HEADING_1,
                BlockType.PARAGRAPH,
                BlockType.HEADING_2,
                BlockType.PARAGRAPH,
                BlockType.UNORD_LIST,
                BlockType.HEADING_1,
                BlockType.PARAGRAPH,
                BlockType.CODE,
                BlockType.PARAGRAPH,
                BlockType.ORD_LIST,
                BlockType.PARAGRAPH,
                BlockType.QUOTE
            ],
            block_types
        )


