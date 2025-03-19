import os
import json

def update_module_paths():
    # Get the root directory of the project (where app.py is located)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Dictionary to store module paths
    module_paths = {}
    
    # Walk through the project directory
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py') and file != 'app.py' and file != 'path_manager.py':
                # Get the relative path of the module
                module_name = file.replace('.py', '')
                module_path = os.path.join(root, file)
                module_paths[module_name] = module_path
    
    # Update devcontainer.json with module paths
    devcontainer_path = os.path.join(root_dir, 'devcontainer', 'devcontainer.json')
    if os.path.exists(devcontainer_path):
        with open(devcontainer_path, 'r') as f:
            devcontainer_config = json.load(f)
    else:
        devcontainer_config = {}

    devcontainer_config['module_paths'] = module_paths

    with open(devcontainer_path, 'w') as f:
        json.dump(devcontainer_config, f, indent=4)

if __name__ == "__main__":
    update_module_paths()
