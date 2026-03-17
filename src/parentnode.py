from htmlnode import HTMLNode
from textnode import TextType 

class ParentNode(HTMLNode):
    def __init__(self,tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Error: Parent Node must have tag attribute.")
        
        if self.children is None:
            raise ValueError("Error: Children Attribute cannot be empty.")
        
        list_tags = []
        for child in self.children:
            list_tags.append(child.to_html())
        
        inner_htmls = "".join(list_tags)
        if self.tag is TextType.IMAGE:
            raise Exception("Error: ParentNode cannot have a TextType.IMAGE tag.")
        return_html = f"<{self.tag}>{inner_htmls}</{self.tag}>"

        return return_html
