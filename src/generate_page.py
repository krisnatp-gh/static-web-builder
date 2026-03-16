import os

from extract_title import extract_title
from markdown_to_html_node import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    """_summary_

    Args:
        from_path (str): path to markdown file (to-be-converted to html)
        template_path (str): path to html template for the page
        dest_path (str): path to copy the converted html to (output html path)
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # read markdown file
    with open(from_path, "r") as f:
        md = f.read()

    # read template file
    with open(template_path, "r") as f:
        template = f.read()
    
    # convert markdown to html
    html_node = markdown_to_html_node(md)
    html_content = html_node.to_html()
    title = extract_title(md)

    # replace {{ Title }} and {{ Content }} placeholders with the ones from markdown
    html_formatted = template.replace("{{ Title }}", title)
    html_formatted = html_formatted.replace("{{ Content }}", html_content)

    # Write the formatted html into dest_path
    if not os.path.exists(dest_path):
        dest_path_dirname = os.path.dirname(dest_path)
        os.makedirs(dest_path_dirname, exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(html_formatted)
    
