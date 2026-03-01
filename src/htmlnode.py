class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        """ Data type to represent a "node" in an HTML document tree

        Args:
            tag (string): A string representing the HTML tag name ("p", "a", "h1", etc.)
            value (string): A string representing the value of the HTML tag (e.g. the text inside a paragraph)
            children (list): A list of HTMLNode objects representing the children of this node
            props (dict): A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        # to-be-overriden by child class
        raise NotImplementedError("Error. to_html has not yet been overriden.")
    
    def props_to_html(self):
        if self.props is None or len(self.props) < 1:
            return ""
        
        formatted_props = " ".join([f'{item}="{value}"' for item, value in self.props.items()])
        
        # add leading space
        formatted_props = " " + formatted_props
        
        return formatted_props

    


    
    # For display

    def _clip_str(self, input_str, clip_len=11):
        # display only first 11 characters of a string if len > 11
        if input_str is None:
            return ""
        
        str_len = len(input_str)
        if str_len <= clip_len:
            value_to_print = input_str
        else:
            # greater than clip_len characters
            value_to_print = f'\'{input_str[:clip_len]}...\' (n_chars = {str_len})'
        
        return value_to_print
    
    def _clip_children(self):
        # string representation of children attribute
        # list gets clipped off if len > 5
        # return string representation of the list
        if self.children is None:
            return ""
        
        children_len = len(self.children)
        if children_len <= 5:
            return str(self.children)
        else:
            return str(self.children[:2]) + ",...," + f"(n_children = {children_len})"

    
    def _clip_props(self):
        # string representation of props attribute
        if self.props is None:
            return ""
        
        props_str = self.props_to_html()
        return self._clip_str(props_str)
        
    def _clip_tag(self):
        if self.tag is None:
            return ""
        else:
            return f'{self.tag}'
    
    def __repr__(self):
        str_representation = f"""HTMLNode(
        tag      = {self._clip_tag()}
        value    = {self._clip_str(self.value)}
        children = {self._clip_children()}
        props    = {self._clip_props()}
        )
        """

        return str_representation
    
