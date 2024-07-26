import xml.etree.ElementTree as ET
import sys
import re
import csv

def parse_xml(file_path):
    # Define the namespace dictionary to handle the XML namespaces
    ns = {"mw": "http://www.mediawiki.org/xml/export-0.11/"}

    # Create an iterparse object
    context = ET.iterparse(file_path, events=("start", "end"))
    context = iter(context)
    event, root = next(context)  # Get the root element

    f_pages = open("import/pages.csv", "w", newline='', encoding='utf-8')
    f_links = open("import/links.csv", "w", newline='', encoding='utf-8')

    f_pages.write("page\n")
    f_links.write("from,to\n")

    page_writer = csv.writer(f_pages, quoting=csv.QUOTE_NONE, escapechar='\\')
    link_writer = csv.writer(f_links, quoting=csv.QUOTE_NONE, escapechar='\\')

    for event, elem in context:
        # Check for the end event and <page> tag
        if event == "end" and elem.tag == "{http://www.mediawiki.org/xml/export-0.11/}page":
            # Extract and print the title, namespace, and id
            title = elem.find("mw:title", ns).text
            
            # Extract the text from the latest revision
            revision = elem.find("mw:revision", ns)
            if revision is not None:
                text_elem = revision.find("mw:text", ns)
                text = text_elem.text if text_elem is not None else ""
            else:
                text = ""
            
            # print(f"Title: {title}")

            if text != None:
                try:
                    pattern = r'\[\[([^|\]]+)(?:\|[^\]]*)?\]\]'
                    matches = re.findall(pattern, text)

                    page_writer.writerow([escape_csv_value(title)])

                    for m in matches:
                        link_writer.writerow([escape_csv_value(title), escape_csv_value(m)])
                except:
                    print(f"{title} failed and text is: {text}")

            # sys.exit(0)

            # It's important to clear the processed element to save memory
            root.clear()
    
    f_pages.close()
    f_links.close()

def escape_csv_value(value):
    """
    Escapes a string value to be safely included in a CSV file.
    
    Args:
    value (str): The string value to escape.
    
    Returns:
    str: The escaped string value.
    """
    if '"' in value:
        # Escape double quotes by doubling them
        value = value.replace('"', '""')
    # Enclose the field in double quotes if it contains a comma, newline, or quote
    if any(c in value for c in [',', '\n', '"']):
        value = f'"{value}"'
    return value

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_csv.py <path_to_xml_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    parse_xml(file_path)
