import os
import shutil

def copy_static(source_dir, dest_dir):
    # delete dest_dir
    shutil.rmtree(dest_dir)

    # Copy each item from source_dir recursively
    copy_static_helper(source_dir, dest_dir)

def copy_static_helper(source_dir, dest_dir):
    # Make destination dir if not exist
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    
    # Base case: copy file if source_dir is file
    if os.path.isfile(source_dir):
        shutil.copy(source_dir, dest_dir)
        return
    
    # Pass: source_dir is a directory
    # Copy each item recursively for nested elements
    for item_dir in os.listdir(source_dir):
        item_source_dir = os.path.join(source_dir, item_dir)
        # set new_dest_dir into subdirectory if item_source_dir is a directory; if file then keep from previous dest_dir
        new_dest_dir = os.path.join(dest_dir, item_dir) if not os.path.isfile(item_source_dir) else dest_dir
        copy_static_helper(item_source_dir, new_dest_dir)