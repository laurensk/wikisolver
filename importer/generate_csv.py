import xml.etree.ElementTree as ET
import sys
import re
import csv
import os
import time

def parse_xml(file_path):
    node_count = 0
    relationship_count = 0

    start = time.time()

    # Define the namespace dictionary to handle the XML namespaces
    ns = {"mw": "http://www.mediawiki.org/xml/export-0.11/"}

    # Create an iterparse object
    context = ET.iterparse(file_path, events=("start", "end"))
    context = iter(context)
    event, root = next(context)  # Get the root element

    if not os.path.exists("import"):
        os.mkdir("import")

    if os.path.exists("import/relationships.csv"):
        os.remove("import/relationships.csv")

    f_nodes = open("import/nodes.csv", "w", newline='', encoding='utf-8')
    f_relationships = open("import/relationships.csv", "w", newline='', encoding='utf-8')

    f_nodes.write("id:ID\n")
    f_relationships.write(":START_ID,:END_ID,:TYPE\n")

    node_writer = csv.writer(f_nodes, quoting=csv.QUOTE_ALL, escapechar='\\')
    relationship_writer = csv.writer(f_relationships, quoting=csv.QUOTE_ALL, escapechar='\\')

    print("Generating, please wait...")

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

                    node_writer.writerow([title])
                    node_count += 1

                    for m in matches:
                        relationship_writer.writerow([title, m, "HAS_LINK_TO"])
                        relationship_count += 1
                except:
                    print(f"{title} failed and text is: {text}")

            # It's important to clear the processed element to save memory
            root.clear()
    
    f_nodes.close()
    f_relationships.close()

    end = time.time()

    print(f"Successfully generated {node_count} nodes and {relationship_count} relationships in {end-start} seconds!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_csv.py <path_to_xml_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    parse_xml(file_path)
