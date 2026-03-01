from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    # LeafNode has no children
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Node has no value.")

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
