import unittest
from extract_urls import extract_markdown_images, extract_markdown_links

class TestExtractUrls(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    
    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )

        self.assertListEqual([('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')], matches)

    def def_test_extract_markdown_images_no_alt(self):
        matches = extract_markdown_images("![](https://rentry.co)")
        self.assertListEqual([('', 'https://rentry.co')], matches)

    def test_extract_markdown_images_special_characters(self):
        matches = extract_markdown_images("![diy link](https://google.com/search?q=how+to+basic)")
        self.assertListEqual([('diy link', 'https://google.com/search?q=how+to+basic')], matches)

    def test_extract_markdown_images_no_exclamation(self):
        matches = extract_markdown_images("[diy link](https://google.com/search?q=how+to+basic)")
        self.assertListEqual([], matches)

    def text_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a url: [diy link](https://google.com/search?q=how+to+basic)"
        )
        
        self.assertListEqual([("diy link", "https://google.com/search?q=how+to+basic")], matches)


    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )

        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)