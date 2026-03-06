# html_to_markdown

Functions for converting HTML content to Markdown formatting.

## Quick Reference

### Functions
- [`html_to_markdown`](#html_to_markdownhtml_content) - Convert HTML string to Markdown
- [`html_to_markdown_file`](#html_to_markdown_fileinput_file-output_file) - Convert HTML file to Markdown file

### Examples
- [HTML to Markdown Conversion](#usage-example)

---

## Functions

### `html_to_markdown(html_content)`

Convert HTML formatting to Markdown formatting.

**Parameters:**
- `html_content` (str): HTML content to convert

**Returns:** `str` - Converted Markdown content

**Supported HTML Elements:**
- Headers: `<h1>` through `<h6>` → `#` through `######`
- Bold: `<strong>`, `<b>` → `**text**`
- Italic: `<em>`, `<i>` → `*text*`
- Links: `<a href="url">text</a>` → `[text](url)`
- Inline code: `<code>` → `` `code` ``
- Code blocks: `<pre>` → ``` ```code``` ```
- Horizontal rules: `<hr>` → `---`
- Line breaks: `<br>` → newline
- Unordered lists: `<ul><li>` → `- item`
- Ordered lists: `<ol><li>` → `1. item`
- Paragraphs: `<p>` → double newline
- Blockquotes: `<blockquote>` → `> text`
- Images: `<img src="url" alt="text">` → `![text](url)`
- Tables: Basic table conversion

---

### `html_to_markdown_file(input_file, output_file)`

Convert an HTML file to a Markdown file.

**Parameters:**
- `input_file` (str): Path to input HTML file
- `output_file` (str): Path to output Markdown file

## Usage Example

```python
from ruf_common import html_to_markdown

# Convert HTML string to Markdown
html = """
<h1>Main Title</h1>
<p>This is a <strong>bold</strong> paragraph with <em>italic</em> text.</p>
<ul>
    <li>First item</li>
    <li>Second item</li>
</ul>
<p>Visit <a href="https://example.com">our site</a> for more info.</p>
"""

markdown = html_to_markdown.html_to_markdown(html)
print(markdown)

# Output:
# # Main Title
#
# This is a **bold** paragraph with *italic* text.
#
# - First item
# - Second item
#
# Visit [our site](https://example.com) for more info.

# Convert a file
html_to_markdown.html_to_markdown_file("input.html", "output.md")
```

## Notes

- HTML entities are automatically unescaped
- Nested HTML within list items and blockquotes is recursively converted
- Empty or whitespace-only content returns `"_Empty_"`
- Remaining HTML tags not explicitly handled are stripped
