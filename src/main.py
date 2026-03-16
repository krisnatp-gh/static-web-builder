import os

from config import ASSET_DIR, OUTPUT_DIR, TEMPLATE_PATH, CONTENT_PATH, MARKDOWN_FILENAME, OUTPUT_HTML_FILENAME

from copy_static import copy_static
from generate_page import generate_page

def main():
    # copy static files to output directory
    copy_static(source_dir=ASSET_DIR, dest_dir=OUTPUT_DIR)

    # generate page from markdown
    markdown_path = os.path.join(CONTENT_PATH, MARKDOWN_FILENAME)
    output_html_path = os.path.join(OUTPUT_DIR, OUTPUT_HTML_FILENAME)
    
    generate_page(from_path = markdown_path,
                  template_path = TEMPLATE_PATH,
                  dest_path = output_html_path)
main()