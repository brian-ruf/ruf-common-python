"""
HTML to Markdown Converter

A Python function to convert HTML formatting to markdown formatting.
Handles common HTML tags and converts them to their markdown equivalents.
"""

import re
import html


def html_to_markdown(html_content):
    """
    Convert HTML formatting to markdown formatting.
    
    Args:
        html_content (str): HTML content to convert
        
    Returns:
        str: Converted markdown content
    """
    if not html_content:
        return ""
    
    # Unescape HTML entities first
    content = html.unescape(html_content)
    
    # Headers (h1-h6)
    for i in range(6, 0, -1):  # Start from h6 to h1 to avoid conflicts
        content = re.sub(f'<h{i}[^>]*>(.*?)</h{i}>', f'{"#" * i} \\1\n', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Bold text - <strong> and <b>
    content = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>', r'**\2**', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Italic text - <em> and <i>
    content = re.sub(r'<(em|i)[^>]*>(.*?)</\1>', r'*\2*', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Links - <a href="url">text</a>
    content = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Inline code - <code>
    content = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Code blocks - <pre>
    content = re.sub(r'<pre[^>]*>(.*?)</pre>', r'```\n\1\n```', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Horizontal rule - <hr>
    content = re.sub(r'<hr[^>]*/?>', '\n---\n', content, flags=re.IGNORECASE)
    
    # Line breaks - <br>
    content = re.sub(r'<br[^>]*/?>', '\n', content, flags=re.IGNORECASE)
    
    # Handle lists - Unordered lists <ul><li>
    def convert_ul_list(match):
        list_content = match.group(1)
        # Extract list items
        items = re.findall(r'<li[^>]*>(.*?)</li>', list_content, flags=re.IGNORECASE | re.DOTALL)
        markdown_items = []
        for item in items:
            # Recursively convert any nested HTML in list items
            converted_item = html_to_markdown(item.strip())
            markdown_items.append(f'- {converted_item}')
        return '\n' + '\n'.join(markdown_items) + '\n'
    
    content = re.sub(r'<ul[^>]*>(.*?)</ul>', convert_ul_list, content, flags=re.IGNORECASE | re.DOTALL)
    
    # Handle lists - Ordered lists <ol><li>
    def convert_ol_list(match):
        list_content = match.group(1)
        # Extract list items
        items = re.findall(r'<li[^>]*>(.*?)</li>', list_content, flags=re.IGNORECASE | re.DOTALL)
        markdown_items = []
        for i, item in enumerate(items, 1):
            # Recursively convert any nested HTML in list items
            converted_item = html_to_markdown(item.strip())
            markdown_items.append(f'{i}. {converted_item}')
        return '\n' + '\n'.join(markdown_items) + '\n'
    
    content = re.sub(r'<ol[^>]*>(.*?)</ol>', convert_ol_list, content, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove remaining list item tags (in case they weren't in ul/ol)
    content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Paragraphs - <p>
    content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Blockquotes - <blockquote>
    def convert_blockquote(match):
        quote_content = match.group(1).strip()
        # Convert nested HTML first
        converted_content = html_to_markdown(quote_content)
        # Add > to each line
        lines = converted_content.split('\n')
        quoted_lines = ['> ' + line for line in lines]
        return '\n' + '\n'.join(quoted_lines) + '\n'
    
    content = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', convert_blockquote, content, flags=re.IGNORECASE | re.DOTALL)
    
    # Images - <img src="url" alt="text">
    content = re.sub(r'<img[^>]*src=["\']([^"\']*)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*/?>', r'![\2](\1)', content, flags=re.IGNORECASE)
    content = re.sub(r'<img[^>]*alt=["\']([^"\']*)["\'][^>]*src=["\']([^"\']*)["\'][^>]*/?>', r'![\1](\2)', content, flags=re.IGNORECASE)
    # Images without alt text
    content = re.sub(r'<img[^>]*src=["\']([^"\']*)["\'][^>]*/?>', r'![](\1)', content, flags=re.IGNORECASE)
    
    # Tables - Basic table conversion
    def convert_table(match):
        table_content = match.group(1)
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_content, flags=re.IGNORECASE | re.DOTALL)
        markdown_rows = []
        
        for i, row in enumerate(rows):
            # Extract cells (th or td)
            cells = re.findall(r'<(th|td)[^>]*>(.*?)</\1>', row, flags=re.IGNORECASE | re.DOTALL)
            cell_contents = [html_to_markdown(cell[1].strip()) for cell in cells]
            markdown_row = '| ' + ' | '.join(cell_contents) + ' |'
            markdown_rows.append(markdown_row)
            
            # Add header separator after first row if it contains th tags
            if i == 0 and any('th' in cell[0].lower() for cell in cells):
                separator = '| ' + ' | '.join(['---'] * len(cells)) + ' |'
                markdown_rows.append(separator)
        
        return '\n' + '\n'.join(markdown_rows) + '\n'
    
    content = re.sub(r'<table[^>]*>(.*?)</table>', convert_table, content, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove any remaining HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    
    # Clean up extra whitespace
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)  # Multiple empty lines to double
    content = re.sub(r'^\s+|\s+$', '', content)  # Trim leading/trailing whitespace

    if content.replace("\n", "").strip() == "":
        content = "_Empty_"
    
    return content


def html_to_markdown_file(input_file, output_file):
    """
    Convert HTML file to markdown file.
    
    Args:
        input_file (str): Path to input HTML file
        output_file (str): Path to output markdown file
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        markdown_content = html_to_markdown(html_content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Successfully converted {input_file} to {output_file}")
    
    except FileNotFoundError:
        print(f"Error: File {input_file} not found")
    except Exception as e:
        print(f"Error converting file: {e}")


# Example usage and test cases
if __name__ == "__main__":
    # Test cases
    test_html = """
    <h1>Main Title</h1>
    <h2>Subtitle</h2>
    <p>This is a <strong>bold</strong> paragraph with <em>italic</em> text and a <a href="https://example.com">link</a>.</p>
    
    <h3>Lists</h3>
    <ul>
        <li>First item</li>
        <li>Second item with <code>inline code</code></li>
        <li>Third item</li>
    </ul>
    
    <ol>
        <li>Numbered item 1</li>
        <li>Numbered item 2</li>
    </ol>
    
    <h3>Code Block</h3>
    <pre>
    def hello_world():
        print("Hello, World!")
    </pre>
    
    <blockquote>
        This is a blockquote with <strong>bold text</strong>.
    </blockquote>
    
    <hr>
    
    <p>Line break example:<br>This is on a new line.</p>
    
    <table>
        <tr>
            <th>Header 1</th>
            <th>Header 2</th>
        </tr>
        <tr>
            <td>Cell 1</td>
            <td>Cell 2</td>
        </tr>
    </table>
    """
    
    print("Original HTML:")
    print(test_html)
    print("\n" + "="*50 + "\n")
    print("Converted Markdown:")
    print(html_to_markdown(test_html))
