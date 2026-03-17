import os

from config import ASSET_DIR, OUTPUT_DIR, TEMPLATE_PATH, CONTENT_PATH

from copy_static import copy_static
from generate_page import generate_page_recursive

def main():
    # copy static files to output directory
    copy_static(source_dir=ASSET_DIR, dest_dir_path=OUTPUT_DIR)

    # # generate page from markdown
    # markdown_path = os.path.join(CONTENT_PATH, MARKDOWN_FILENAME)
    # output_html_path = os.path.join(OUTPUT_DIR, OUTPUT_HTML_FILENAME)
    
    generate_page_recursive(content_path = CONTENT_PATH,
                  template_path = TEMPLATE_PATH,
                  dest_dir_path = OUTPUT_DIR)
main()