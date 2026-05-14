"""Tests for the html_to_markdown module."""

import pytest

from ruf_common.html_to_markdown import html_to_markdown


class TestHtmlToMarkdownBasic:
    def test_empty_string_returns_empty(self):
        assert html_to_markdown("") == ""

    def test_plain_text_passthrough(self):
        result = html_to_markdown("Hello world")
        assert "Hello world" in result

    def test_whitespace_only_returns_empty_marker(self):
        result = html_to_markdown("   <p>  </p>  ")
        assert result == "_Empty_" or result.strip() == ""


class TestHeaders:
    def test_h1(self):
        result = html_to_markdown("<h1>Title</h1>")
        assert result.startswith("# Title")

    def test_h2(self):
        result = html_to_markdown("<h2>Sub</h2>")
        assert result.startswith("## Sub")

    def test_h6(self):
        result = html_to_markdown("<h6>Tiny</h6>")
        assert result.startswith("###### Tiny")


class TestInlineFormatting:
    def test_bold_strong(self):
        result = html_to_markdown("<strong>bold</strong>")
        assert "**bold**" in result

    def test_bold_b_tag(self):
        result = html_to_markdown("<b>bold</b>")
        assert "**bold**" in result

    def test_italic_em(self):
        result = html_to_markdown("<em>italic</em>")
        assert "*italic*" in result

    def test_italic_i_tag(self):
        result = html_to_markdown("<i>italic</i>")
        assert "*italic*" in result

    def test_inline_code(self):
        result = html_to_markdown("<code>x = 1</code>")
        assert "`x = 1`" in result

    def test_link(self):
        result = html_to_markdown('<a href="https://example.com">click</a>')
        assert "[click](https://example.com)" in result


class TestLineBreakAndHr:
    def test_br_becomes_newline(self):
        result = html_to_markdown("line1<br>line2")
        assert "line1" in result
        assert "line2" in result

    def test_hr_becomes_dashes(self):
        result = html_to_markdown("<hr>")
        assert "---" in result


class TestLists:
    def test_unordered_list(self):
        html = "<ul><li>one</li><li>two</li></ul>"
        result = html_to_markdown(html)
        assert "- one" in result
        assert "- two" in result

    def test_ordered_list(self):
        html = "<ol><li>first</li><li>second</li></ol>"
        result = html_to_markdown(html)
        assert "1. first" in result
        assert "2. second" in result


class TestParagraph:
    def test_paragraph_content_preserved(self):
        result = html_to_markdown("<p>Hello paragraph</p>")
        assert "Hello paragraph" in result


class TestCodeBlock:
    def test_pre_becomes_fenced(self):
        result = html_to_markdown("<pre>code here</pre>")
        assert "```" in result
        assert "code here" in result


class TestBlockquote:
    def test_blockquote_prefix(self):
        result = html_to_markdown("<blockquote>quoted text</blockquote>")
        assert "> " in result
        assert "quoted text" in result


class TestImage:
    def test_image_with_alt(self):
        result = html_to_markdown('<img src="img.png" alt="desc"/>')
        assert "![desc](img.png)" in result

    def test_image_without_alt(self):
        result = html_to_markdown('<img src="img.png"/>')
        assert "img.png" in result


class TestTable:
    def test_table_with_headers(self):
        html = (
            "<table>"
            "<tr><th>A</th><th>B</th></tr>"
            "<tr><td>1</td><td>2</td></tr>"
            "</table>"
        )
        result = html_to_markdown(html)
        assert "| A |" in result or "| A" in result
        assert "---" in result

    def test_table_rows(self):
        html = (
            "<table>"
            "<tr><th>H</th></tr>"
            "<tr><td>val</td></tr>"
            "</table>"
        )
        result = html_to_markdown(html)
        assert "val" in result


class TestHtmlEntities:
    def test_ampersand_entity(self):
        result = html_to_markdown("<p>a &amp; b</p>")
        assert "a & b" in result

    def test_nbsp_entity(self):
        result = html_to_markdown("<p>hello&nbsp;world</p>")
        assert "hello" in result and "world" in result


class TestStripRemainingTags:
    def test_unknown_tags_removed(self):
        result = html_to_markdown("<div><span>text</span></div>")
        assert "<div>" not in result
        assert "<span>" not in result
        assert "text" in result
