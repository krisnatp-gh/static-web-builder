# Pattern matching for extracting urls
IMAGE_URL_PATTERN = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

REGULAR_URL_PATTERN = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"


# Pattern matching for removing block markdown markers before conversion to HTMLNodes
HEADER_BLOCK_MARKER = r"#{1,6} "

CODE_BLOCK_MARKER = "```"

QUOTE_BLOCK_MARKER = ">"

UNORDERED_LIST_BLOCK_MARKER = "- "

ORDERED_LIST_BLOCK_MARKER = r"\d. "



