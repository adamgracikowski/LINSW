import os

def build_file_tree(current_path, relative_path=""):
    tree = {
        'name': os.path.basename(current_path) if relative_path else 'Root',
        'path': relative_path,
        'is_dir': True,
        'children': []
    }
    try:
        items = sorted(os.listdir(current_path))
    except OSError:
        return tree

    for entry in items:
        entry_rel = os.path.join(relative_path, entry) if relative_path else entry
        entry_path = os.path.join(current_path, entry)
        if os.path.isdir(entry_path):
            subtree = build_file_tree(entry_path, entry_rel)
            tree['children'].append(subtree)
        else:
            tree['children'].append({
                'name': entry,
                'path': entry_rel,
                'is_dir': False,
                'children': []
            })
    return tree