import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = HTMLNode("p")
        node2 = HTMLNode("p")
        self.assertEqual(node, node2)

    def test_eq3(self):
        node = HTMLNode("p", "test", None, {"href": "https://www.google.com",
                                            "target": "_blank",})
        node2 = HTMLNode("p", "test", None, {"href": "https://www.google.com",
                                            "target": "_blank",})

        self.assertEqual(node, node2)

    def test_eq4(self):
        node = HTMLNode("p", "test", None, {"href": "https://www.google.com",
                                            "target": "_blank",})
        node2 = HTMLNode("p", "test", None, {"href": "https://www.google.com",
                                            "target": "_blank",})
        text = node.props_to_html()
        text2 = node2.props_to_html()
        self.assertEqual(text, text2)

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )


class TestParentMode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren2(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("p", "grandchild2")
        child_node = ParentNode("span", [grandchild_node, grandchild_node2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><p>grandchild2</p></span></div>",
        )

    def test_to_html_many_children(self):
            node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
            )
            self.assertEqual(
                node.to_html(),
                "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
            )


if __name__ == "__main__":
    unittest.main()
