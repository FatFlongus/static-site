from ast import List
import unittest

from inline_markdown import (
    split_nodes_delimiter, extract_markdown_images, extract_markdown_links,
    split_nodes_image, split_nodes_link, text_to_textnodes
)
from textnode import TextNode, TextType


class TestSplitNodeDelimiter(unittest.TestCase):

    def test_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        test_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, test_nodes)

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
            )

class TestExtractMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.youtube.com)"
        )
        self.assertListEqual([("link", "https://www.youtube.com")], matches)

    def test_extract_markdown_images2(self):
        matches = extract_markdown_images(
            "This is text with ![two](https://i.imgur.com/zjjcJKZ.png) ![images](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("two", "https://i.imgur.com/zjjcJKZ.png"),
            ("images", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links2(self):
        matches = extract_markdown_links(
            "This is text with [two](https://www.youtube.com) [links](https://www.boot.dev)"
        )
        self.assertListEqual([("two", "https://www.youtube.com"),
            ("links", "https://www.boot.dev")], matches)

class TestSplitNodesImage(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_images2(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

class TestSplitNodesLink(unittest.TestCase):

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.youtube.com) and another [second link](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.youtube.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )
    def test_split_links2(self):
        node = TextNode(
            "This is text with a [link](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.youtube.com"),
            ],
            new_nodes,
        )

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnode(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )
    def test_text_to_textnode2(self):
        nodes = text_to_textnodes("This is _text_ with a **bold** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.ITALIC),
                TextNode(" with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )
    def test_text_to_textnode_no_links(self):
        nodes = text_to_textnodes("This is _text_ with a **bold** word and a `code block`")
        self.assertListEqual(nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.ITALIC),
                TextNode(" with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
            ]
        )
    def test_text_to_textnode_links(self):
        nodes = text_to_textnodes("This is [text](https://boot.dev) and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual(nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.LINK, "https://boot.dev"),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ]
        )


if __name__ == "__main__":
    unittest.main()
