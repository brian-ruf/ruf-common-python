"""
XML Formatter Module

This module provides XML formatting functionality both as a command-line tool and as 
importable functions for use by other Python modules.

Command Line Interface:
    python xml_formatter.py <xml_file_or_directory> [--line-wrap N] [-r]

Programmatic API Functions:

1. format_xml_string(xml_content, line_wrap_column=None)
   - Format XML content that's already in memory
   - Returns formatted XML as a string
   
2. format_xml_file_to_string(file_path, line_wrap_column=None)  
   - Format an XML file and return the result without modifying the original
   - Returns formatted XML as a string
   
3. format_xml_file_programmatic(file_path, in_place=False, line_wrap_column=None)
   - Format an XML file with option to save in place or return content
   - If in_place=True: modifies the original file and returns True on success
   - If in_place=False: returns formatted XML as a string without modifying file
   
4. format_xml_folder(folder_path, recursive=False, line_wrap_column=None, in_place=True)
   - Format all XML files in a folder
   - If in_place=True: modifies files and returns dict of {file_path: success_bool}
   - If in_place=False: returns dict of {file_path: formatted_content_string}
   - recursive=True searches subdirectories

Usage Examples:
    from common.xml_formatter import format_xml_string, format_xml_file_programmatic
    
    # Format XML content in memory
    formatted = format_xml_string('<root><item>content</item></root>')
    
    # Format file and save in place
    format_xml_file_programmatic('myfile.xml', in_place=True)
    
    # Format file and get content without modifying original
    content = format_xml_file_programmatic('myfile.xml', in_place=False)
"""

import xml.etree.ElementTree as ET
import xml.dom.minidom
import argparse
import sys
from pathlib import Path

# Global configuration
LINE_WRAP_COLUMN = 80


def format_xml_string(xml_content, line_wrap_column=None):
    """
    Format XML content string with proper indentation and line wrapping.
    
    Args:
        xml_content (str): XML content as a string
        line_wrap_column (int, optional): Column width for line wrapping. 
                                        If None, uses global LINE_WRAP_COLUMN
        
    Returns:
        str: Formatted XML string, or None if formatting failed
    """
    global LINE_WRAP_COLUMN
    
    if line_wrap_column is None:
        line_wrap_column = LINE_WRAP_COLUMN
        
    try:
        # Store original global setting
        original_wrap_column = LINE_WRAP_COLUMN
        LINE_WRAP_COLUMN = line_wrap_column
        
        # Validate XML structure with ElementTree
        ET.fromstring(xml_content.strip())
        
        # Use minidom to format while preserving original structure
        dom = xml.dom.minidom.parseString(xml_content.strip())
        
        # Format with pretty printing
        pretty_xml = dom.toprettyxml(indent="  ", encoding=None)
        
        # Clean up the output
        lines = pretty_xml.split('\n')
        
        # Remove empty lines and clean up
        cleaned_lines = []
        for line in lines:
            stripped = line.rstrip()
            if stripped:  # Only keep non-empty lines
                cleaned_lines.append(stripped)
        
        # Apply line wrapping for long lines
        wrapped_lines = []
        for line in cleaned_lines:
            if len(line) <= LINE_WRAP_COLUMN:
                wrapped_lines.append(line)
            else:
                # For very long lines, try to wrap at attribute boundaries
                if '=' in line and '<' in line and not line.strip().startswith('<!--'):
                    # This is likely an element with attributes
                    wrapped = wrap_xml_element(line)
                    wrapped_lines.extend(wrapped)
                else:
                    # For other long lines, just add them as-is to preserve content
                    wrapped_lines.append(line)
        
        # Join lines and ensure proper line endings
        formatted_xml = '\n'.join(wrapped_lines)
        
        # Ensure content ends with newline
        if not formatted_xml.endswith('\n'):
            formatted_xml += '\n'
            
        return formatted_xml
        
    except ET.ParseError as e:
        raise ValueError(f"Error parsing XML content: {e}")
    except Exception as e:
        raise RuntimeError(f"Error formatting XML content: {e}")
    finally:
        # Restore original global setting
        LINE_WRAP_COLUMN = original_wrap_column


def format_xml_file_to_string(file_path, line_wrap_column=None):
    """
    Format an XML file and return the formatted content as a string without modifying the original file.
    
    Args:
        file_path (str): Path to the XML file to format
        line_wrap_column (int, optional): Column width for line wrapping.
                                        If None, uses global LINE_WRAP_COLUMN
        
    Returns:
        str: Formatted XML content as a string
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the XML content is invalid
        RuntimeError: If formatting fails for other reasons
    """
    try:
        # Read the original XML content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Use the string formatter
        return format_xml_string(content, line_wrap_column)
        
    except FileNotFoundError:
        raise FileNotFoundError(f"XML file not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Error reading file {file_path}: {e}")


def format_xml_file_programmatic(file_path, in_place=False, line_wrap_column=None):
    """
    Format an XML file with the option to save in place or return the formatted content.
    
    Args:
        file_path (str): Path to the XML file to format
        in_place (bool): If True, save the formatted XML back to the original file.
                        If False, return the formatted content without modifying the file.
        line_wrap_column (int, optional): Column width for line wrapping.
                                        If None, uses global LINE_WRAP_COLUMN
        
    Returns:
        str or bool: If in_place=False, returns formatted XML content as string.
                    If in_place=True, returns True on success.
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the XML content is invalid
        RuntimeError: If formatting fails for other reasons
    """
    try:
        # Get the formatted content
        formatted_xml = format_xml_file_to_string(file_path, line_wrap_column)
        
        if in_place:
            # Write the formatted XML back to the same file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(formatted_xml)
            return True
        else:
            # Return the formatted content
            return formatted_xml
            
    except Exception as e:
        # Re-raise with more context
        raise type(e)(f"Error formatting file {file_path}: {e}")


def format_xml_folder(folder_path, recursive=False, line_wrap_column=None, in_place=True):
    """
    Format all XML files in a folder.
    
    Args:
        folder_path (str): Path to the folder containing XML files
        recursive (bool): If True, search for XML files recursively in subdirectories
        line_wrap_column (int, optional): Column width for line wrapping.
                                        If None, uses global LINE_WRAP_COLUMN
        in_place (bool): If True, save formatted XML back to original files.
                        If False, return a dictionary of {file_path: formatted_content}
        
    Returns:
        dict or bool: If in_place=False, returns dict mapping file paths to formatted content.
                     If in_place=True, returns dict mapping file paths to success status (bool).
        
    Raises:
        FileNotFoundError: If the folder doesn't exist
        ValueError: If folder_path is not a directory
    """
    folder = Path(folder_path)
    
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    if not folder.is_dir():
        raise ValueError(f"Path is not a directory: {folder_path}")
    
    # Find XML files
    xml_files = find_xml_files(folder_path, recursive)
    
    if not xml_files:
        return {} if not in_place else {}
    
    results = {}
    
    for xml_file in xml_files:
        try:
            if in_place:
                # Format and save in place
                success = format_xml_file_programmatic(xml_file, in_place=True, line_wrap_column=line_wrap_column)
                results[xml_file] = success
            else:
                # Format and return content
                formatted_content = format_xml_file_programmatic(xml_file, in_place=False, line_wrap_column=line_wrap_column)
                results[xml_file] = formatted_content
                
        except Exception as e:
            # Store the error for this file
            results[xml_file] = False if in_place else f"Error: {e}"
    
    return results


def format_xml_file(file_path):
    """
    Format an XML file with proper indentation and line wrapping.
    This function modifies the original file in place and is used by the CLI.
    
    Args:
        file_path (str): Path to the XML file to format
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Use the new programmatic function with in_place=True
        format_xml_file_programmatic(file_path, in_place=True)
        print(f"Successfully formatted XML file: {file_path}")
        return True
        
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error processing file {file_path}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error processing file {file_path}: {e}")
        return False


def format_element(element, indent_level):
    """
    Recursively format an XML element with proper indentation.
    
    Args:
        element: The XML element to format
        indent_level: Current indentation level
        
    Returns:
        str: Formatted XML string for this element
    """
    indent = '  ' * indent_level
    lines = []
    
    # Build the opening tag
    tag_parts = [element.tag]
    
    # Add attributes
    if element.attrib:
        for key, value in element.attrib.items():
            tag_parts.append(f'{key}="{value}"')
    
    # Create the opening tag line
    if len(tag_parts) == 1:
        opening_tag = f'<{tag_parts[0]}>'
    else:
        # Check if we need to wrap attributes
        full_tag = '<' + ' '.join(tag_parts) + '>'
        if len(indent + full_tag) <= LINE_WRAP_COLUMN:
            opening_tag = full_tag
        else:
            # Wrap attributes
            opening_tag = f'<{tag_parts[0]}'
            for attr in tag_parts[1:]:
                if len(indent + opening_tag + ' ' + attr + '>') <= LINE_WRAP_COLUMN:
                    opening_tag += ' ' + attr
                else:
                    lines.append(indent + opening_tag)
                    opening_tag = indent + '    ' + attr
            opening_tag += '>'
    
    # Handle element content
    has_children = len(element) > 0
    has_text = element.text and element.text.strip()
    
    if not has_children and not has_text:
        # Self-closing or empty element
        if opening_tag.endswith('>'):
            opening_tag = opening_tag[:-1] + '/>'
        lines.append(indent + opening_tag)
    elif not has_children and has_text:
        # Element with only text content
        text_content = element.text.strip()
        full_line = indent + opening_tag + text_content + f'</{element.tag}>'
        if len(full_line) <= LINE_WRAP_COLUMN:
            lines.append(full_line)
        else:
            # Split across multiple lines
            lines.append(indent + opening_tag)
            lines.append(indent + '  ' + text_content)
            lines.append(indent + f'</{element.tag}>')
    else:
        # Element with children
        lines.append(indent + opening_tag)
        
        # Add text content if present
        if has_text:
            lines.append(indent + '  ' + element.text.strip())
        
        # Add children
        for child in element:
            child_lines = format_element(child, indent_level + 1)
            lines.append(child_lines)
            
            # Add tail text if present
            if child.tail and child.tail.strip():
                lines.append(indent + '  ' + child.tail.strip())
        
        # Add closing tag
        lines.append(indent + f'</{element.tag}>')
    
    return '\n'.join(lines)


def wrap_xml_element(line):
    """
    Wrap a long XML element line at attribute boundaries.
    
    Args:
        line (str): The XML line to wrap
        
    Returns:
        list: List of wrapped lines
    """
    # Find the opening tag
    tag_start = line.find('<')
    tag_end = line.find('>')
    
    if tag_start == -1 or tag_end == -1:
        return [line]
    
    # Extract indentation
    indent = line[:tag_start]
    
    # Extract tag name
    tag_content = line[tag_start:tag_end + 1]
    remaining = line[tag_end + 1:]
    
    # If the tag itself is not too long, don't wrap
    if len(indent + tag_content) <= LINE_WRAP_COLUMN:
        return [line]
    
    # Try to wrap at attribute boundaries
    if ' ' not in tag_content:
        return [line]  # No attributes to wrap
    
    # Split tag content into parts
    parts = tag_content.split(' ')
    if len(parts) < 2:
        return [line]
    
    wrapped_lines = []
    current_line = indent + parts[0]  # Start with opening tag
    
    for part in parts[1:]:
        # Check if adding this part would exceed the line limit
        if len(current_line + ' ' + part) > LINE_WRAP_COLUMN:
            # Add current line and start a new one
            wrapped_lines.append(current_line)
            current_line = indent + '    ' + part  # Extra indentation for attributes
        else:
            current_line += ' ' + part
    
    # Add the final line with any remaining content
    wrapped_lines.append(current_line + remaining)
    
    return wrapped_lines


def find_xml_files(directory_path, recursive=False):
    """
    Find all XML files in a directory.
    
    Args:
        directory_path (str): Path to the directory to search
        recursive (bool): Whether to search recursively in subdirectories
        
    Returns:
        list: List of XML file paths
    """
    xml_files = []
    directory = Path(directory_path)
    
    if recursive:
        # Use glob to find all XML files recursively
        xml_files = list(directory.rglob('*.xml'))
    else:
        # Find XML files only in the current directory
        xml_files = list(directory.glob('*.xml'))
    
    return [str(xml_file) for xml_file in xml_files]


def main():
    """Main function to handle command line arguments and process the XML file(s)."""
    global LINE_WRAP_COLUMN
    
    parser = argparse.ArgumentParser(
        description='Format XML files with proper indentation and line wrapping'
    )
    parser.add_argument(
        'xml_path',
        help='Path to the XML file or directory containing XML files to format'
    )
    parser.add_argument(
        '--line-wrap',
        type=int,
        default=LINE_WRAP_COLUMN,
        help=f'Column width for line wrapping (default: {LINE_WRAP_COLUMN})'
    )
    parser.add_argument(
        '-r', '--recurse',
        action='store_true',
        help='Recursively format XML files in subdirectories (only applies when path is a directory)'
    )
    
    args = parser.parse_args()
    
    # Update global line wrap setting if provided
    LINE_WRAP_COLUMN = args.line_wrap
    
    # Check if path exists
    xml_path = Path(args.xml_path)
    if not xml_path.exists():
        print(f"Error: Path '{args.xml_path}' does not exist.")
        sys.exit(1)
    
    xml_files_to_process = []
    
    if xml_path.is_file():
        # Single file processing
        if not xml_path.suffix.lower() == '.xml':
            print(f"Error: '{args.xml_path}' is not an XML file.")
            sys.exit(1)
        xml_files_to_process = [str(xml_path)]
    elif xml_path.is_dir():
        # Directory processing
        xml_files_to_process = find_xml_files(args.xml_path, args.recurse)
        if not xml_files_to_process:
            print(f"No XML files found in directory '{args.xml_path}'")
            if not args.recurse:
                print("Use -r/--recurse to search subdirectories")
            sys.exit(0)
        
        print(f"Found {len(xml_files_to_process)} XML file(s) to format")
        if args.recurse:
            print("Searching recursively in subdirectories")
    else:
        print(f"Error: '{args.xml_path}' is neither a file nor a directory.")
        sys.exit(1)
    
    # Process all XML files
    success_count = 0
    total_count = len(xml_files_to_process)
    
    for xml_file in xml_files_to_process:
        success = format_xml_file(xml_file)
        if success:
            success_count += 1
    
    # Print summary
    if total_count > 1:
        print(f"\nSummary: Successfully formatted {success_count} out of {total_count} XML files")
        if success_count < total_count:
            print(f"Failed to format {total_count - success_count} files")
    
    if success_count < total_count:
        sys.exit(1)


if __name__ == '__main__':
    main()
