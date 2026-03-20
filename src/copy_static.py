import os
import shutil

def copy_static(source_dir, dest_dir_path):
    # delete dest_dir_path
    if os.path.exists(dest_dir_path):
        shutil.rmtree(dest_dir_path)

    # Copy each item from source_dir recursively
    copy_static_helper(source_dir, dest_dir_path)

def copy_static_helper(source_dir, dest_dir_path):
    # Make destination dir if not exist
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    
    # Base case: copy file if source_dir is file
    if os.path.isfile(source_dir):
        shutil.copy(source_dir, dest_dir_path)
        return
    
    # Pass: source_dir is a directory
    # Copy each item recursively for nested elements
    for item_path in os.listdir(source_dir):
        item_path_relative = os.path.join(source_dir, item_path)
        # set new_dest_dir_path into subdirectory if item_path_relative is a directory; if file then keep from previous dest_dir_path
        new_dest_dir_path = os.path.join(dest_dir_path, item_path) if not os.path.isfile(item_path_relative) else dest_dir_path
        copy_static_helper(item_path_relative, new_dest_dir_path)