import os
import sys

from config import ASSET_DIR, OUTPUT_DIR, TEMPLATE_PATH, CONTENT_DIR

from copy_static import copy_static
from generate_page import generate_page_recursive

def main():
    # Get the basepath from cli argument
    basepath = "/" if len(sys.argv) < 2 else sys.argv[1]
    # copy static files to output directory
    copy_static(source_dir=ASSET_DIR, dest_dir_path=OUTPUT_DIR)
    
    generate_page_recursive(content_path = CONTENT_DIR,
                  template_path = TEMPLATE_PATH,
                  dest_dir_path = OUTPUT_DIR,
                  basepath = basepath)
main()