

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return [f' {key}="{value}"' for key, value in self.props.items()]
    
    def __repr__(self):
        return f"HTMLNode: {self.tag}, {self.value}, {self.children}, {self.props}"
    
    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props 
    



class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)
    
    def to_html(self):
        if self.tag != "img" and not self.value:
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return f"{self.value}"
        return f"<{self.tag}{"" if not self.props else "".join(self.props_to_html())}>{self.value}</{self.tag}>"
    




class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have tag")
        if not self.children:
            raise ValueError("ParentNode must have one or more children")
        node_string = f"<{self.tag}{"" if not self.props else "".join(self.props_to_html())}>"

        for node in self.children:
            node_string = node_string + f"{node.to_html()}"
        node_string = node_string + f"</{self.tag}>"
        return node_string
            
        
    
    

    

        
               



        
