

from typing import override


class HTMLNode:
    def __init__(self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        html_str = ""
        if self.props is None:
            return html_str
        keys = list(self.props.keys())
        values = list(self.props.values())
        for i in range(len(self.props)):
            html_str += f' {keys[i]}="{values[i]}"'
        return html_str


    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag
                and self.value == other.value
                and self.children == other.children
                and self.props == other.props
                )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

#---------------------------------------------------------

class LeafNode(HTMLNode):
    def __init__(self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None
    ):
        super().__init__(tag, value, None, props)

    @override
    def to_html(self) -> str:
        if not isinstance(self.value, str):
            raise ValueError("leaf nodes must have a value")  # noqa: TRY004
        if self.tag is None:
            return self.value
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

    @override
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

#---------------------------------------------------------

class ParentNode(HTMLNode):
    def __init__(self,
        tag: str,
        children: list["HTMLNode"],
        props: dict[str, str] | None = None
    ):
        super().__init__(tag, None, children, props)

    @override
    def to_html(self) -> str:
        if not isinstance(self.tag, str):
            raise ValueError("Parent node must have a tag")
        if self.children is None:
            raise ValueError("Parent node must have a child node")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    @override
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
