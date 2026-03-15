from extract_urls import extract_markdown_images, extract_markdown_links

from enum import Enum

class TextType(Enum):
# For denoting type of texts. The values correspond to the HTML tags of the markdown delimiters or image/url markers.
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

        case (TextType.CODE, "`"):
            return True
        
        case _:
            return False
    


class TextNode():
    """
    Represent parsed markdown meaning.
    """
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

def text_to_textnodes(text):
    """
    Take a markdown text and split it into a list of TextNodes using split functions below

    Args:
        text (str): markdown text to be split into
    
    Returns:
        list of TextNodes: list of text nodes split by delimiter and images
    """
    node = TextNode(text = text,
                    text_type = TextType.TEXT
                    )
    
    # Split into bold delimiters
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    # Split nto italics delimiters
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    # Split into code delimiters
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    # Extract images
    new_nodes = split_nodes_image(new_nodes)
    # Extract links
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes




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


def split_nodes_image(old_nodes):

    new_nodes = []
    for node in old_nodes:
        if node.text is None:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_images(node.text)

        if len(matches) < 1:
            new_nodes.append(node)
            continue # no image urls --> append node as is and move on to next iteration
        
        # matches now guaranteed to have at least one image_alt, urls
        current_text = node.text
        for image_alt, image_link in matches:
            image_markdown = f"![{image_alt}]({image_link})"
            sections = current_text.split(image_markdown, maxsplit=1) # since the link separator is guaranteed to be there, may have at least two items
            #
            # two items --> case 1 : current_text is a text followed by image url and some other text (may contain another image_url) [<text1>, <text2>]
            #               case 2 : current_text is an image url followed by some other text (may contain another image_url) ['', <text>]
            #               case 3 : current_text is a text followed by an image url [<text>, '']
            #               case 4 : current_text is just an image url ['', '']

            if sections[0] != '':
                # append the text node preceding the image markdown
                pre_node = TextNode(text = sections[0], 
                                    text_type = TextType.TEXT
                                    )

                new_nodes.append(pre_node)


            # append the image node following the text
            image_node = TextNode(text = image_alt, 
                                  text_type = TextType.IMAGE,
                                  url = image_link
                                  )
            new_nodes.append(image_node)
            
            current_text  = sections[1] # move to second element -> in the next loop match second image link
        
        # done looping throughout all matching url -> check if there's remaining current text then append
        if current_text != '':
            after_node = TextNode(text = current_text,
                                  text_type = TextType.TEXT,
                                  )
            new_nodes.append(after_node)

    
    return new_nodes

            

def split_nodes_link(old_nodes):

    new_nodes = []
    for node in old_nodes:
        if node.text is None:
            new_nodes.append(node)
            continue
        
        matches = extract_markdown_links(node.text)

        if len(matches) < 1:
            new_nodes.append(node)
            continue # no link urls --> append node as is and move on to next iteration
        
        # matches now guaranteed to have at least one link_alt, urls
        current_text = node.text

        for link_alt, regular_link in matches:
            link_markdown = f"[{link_alt}]({regular_link})"
            sections = current_text.split(link_markdown, 1) # since the link separator is guaranteed to be there, may have at least two items
            #
            # two items --> case 1 : current_text is a text followed by link url and some other text (may contain another link_url) [<text1>, <text2>]
            #               case 2 : current_text is a link url followed by some other text (may contain another link_url) ['', <text>]
            #               case 3 : current_text is a text followed by an link url [<text>, '']
            #               case 4 : current_text is just an image url ['', '']

            if sections[0] != '':
                # append the text node preceding the link markdown
                pre_node = TextNode(text = sections[0], 
                                    text_type = TextType.TEXT
                                    )

                new_nodes.append(pre_node)


            # append the link node following the text
            link_node = TextNode(text = link_alt, 
                                  text_type = TextType.LINK,
                                  url = regular_link
                                  )
            new_nodes.append(link_node)
            
            current_text  = sections[1] # move to second element -> in the next loop match second link
        
        # done looping throughout all matching url -> check if there's remaining current text then append
        if current_text != '':
            after_node = TextNode(text = current_text,
                                  text_type = TextType.TEXT,
                                  )
            new_nodes.append(after_node)


    
    return new_nodes

                        
        

        

        
