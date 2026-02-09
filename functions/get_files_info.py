import os

def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))

        # Will be True or False
        valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        is_dir = os.path.isdir(target_dir)
        if is_dir is False:
            return f'Error: "{directory}" is not a directory'
        
        list_dir = os.listdir(target_dir)
        all_items = []
        for item in list_dir:
            
            item_size = os.path.getsize(os.path.join(target_dir, item))
            is_item_dir = os.path.isdir(os.path.join(target_dir, item))
            
            item_info = f"- {item}: file_size={item_size}, is_dir={is_item_dir}"
            all_items.append(item_info)
        format_list_items = "\n".join(all_items)
        return format_list_items
    except FileNotFoundError:
        return f"Error: could not locate file"
    except PermissionError:
        return f"Error: you do not have file access"
    except Exception as e:
        return f"Error: {e}, could not process this request"