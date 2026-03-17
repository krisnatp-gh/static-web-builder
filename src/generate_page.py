import os

from extract_title import extract_title
from markdown_to_html_node import markdown_to_html_node

def generate_page_recursive(content_path, template_path, dest_dir_path):
    """
    Recursive. Crawl every entry in the content directory. For each markdown file found, generate a new .html file using the same template.html. The generated pages should be written to the public directory in the same directory structure.

    Assume content_path contains only markdown file if it is a file path.

    Args:
        content_path (str): (file or directory) path .
        template_path (str): file path to html template for the page
        dest_dir_path (str): directory path to copy the converted html to (output html path)
    """

    # Base case: file
    if os.path.isfile(content_path):
        generate_page(content_path, template_path, dest_dir_path)
        return
    
    # Pass: content_path is directory
    for item_path in os.listdir(content_path):
        item_path_relative = os.path.join(content_path, item_path) # item path relative to content path

        # set new_dest_dir_path into subdirectory if item_path_relative is a directory, else set it into new html file
        if not os.path.isfile(item_path_relative):
            new_dest_dir_path = os.path.join(dest_dir_path, item_path)
        else:
            # output file is converted to html
            output_file_path = item_path.rsplit(".", maxsplit=1)[0] + ".html"
            new_dest_dir_path = os.path.join(dest_dir_path, output_file_path)
        
        # Recursive call
        generate_page_recursive(item_path_relative, template_path, new_dest_dir_path)





def generate_page(from_path, template_path, dest_path):
    """
    Read a markdown file -> Convert it into HTML -> Include the converted HTML into body of template -> Save output destination path.

    Args:
        from_path (str): file path to markdown (to-be-converted to html)
        template_path (str): file path to html template for the page
        dest_path (str): file path to copy the converted html to (output html path)
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
    
