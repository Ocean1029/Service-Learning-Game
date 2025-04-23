import os
import nbformat
from nbformat.v4 import new_notebook, new_code_cell
import re

# 設定你的資料夾路徑
folder_path = '/Users/albert/Desktop/大二下/Service Learning/Service-Learning-Game/monkey_shoot_balloon'

# 遞迴取得所有 .py 檔案
def get_py_files(directory):
    py_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                # 取得相對路徑
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, directory)
                py_files.append(relative_path)
    return sorted(py_files)

def convert_relative_imports(code, file_path):
    # Get the module path relative to the root folder
    rel_dir = os.path.dirname(file_path)
    if rel_dir == '':
        return code
        
    # Convert relative imports to absolute
    lines = code.split('\n')
    modified_lines = []
    
    for line in lines:
        # Match relative imports
        if re.match(r'^from\s+\.', line) or re.match(r'^import\s+\.', line):
            # Extract the dots part
            if 'from' in line:
                parts = line.split('from ')[1].split(' import')
                module_path = parts[0].strip()
                rest = ' import' + parts[1] if len(parts) > 1 else ''
            else:
                parts = line.split('import ')[1].split(' as')
                module_path = parts[0].strip()
                rest = ' as' + parts[1] if len(parts) > 1 else ''
                
            # Count the dots
            dots_count = 0
            while module_path.startswith('.'):
                dots_count += 1
                module_path = module_path[1:]
                
            # Calculate the absolute import path
            parts = rel_dir.split(os.sep)
            if dots_count > len(parts):
                # If trying to import from above root, keep original line
                modified_lines.append(line)
                continue
                
            # Get the absolute import path
            absolute_path = '.'.join(parts[:-dots_count] if dots_count > 0 else parts)
            
            if absolute_path and module_path:
                new_path = f"{absolute_path}.{module_path}"
            elif absolute_path:
                new_path = absolute_path
            else:
                new_path = module_path
                
            if 'from' in line:
                modified_lines.append(f'from {new_path}{rest}')
            else:
                modified_lines.append(f'import {new_path}{rest}')
        else:
            modified_lines.append(line)
    
    return '\n'.join(modified_lines)

# 取得所有 .py 檔案
py_files = get_py_files(folder_path)

# 建立一個新的 notebook
nb = new_notebook()
print("Found the following Python files:")
for file in py_files:
    print(f"- {file}")

# Add an initial cell with path setup
setup_code = f"""import sys
import os
# Add project root to Python path
if not "{folder_path}" in sys.path:
    sys.path.append("{folder_path}")
"""
nb.cells.append(new_code_cell(setup_code))

# 將每個 py 檔案的內容加入 notebook 作為一個 cell
for filename in py_files:
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    # Convert relative imports to absolute
    modified_code = convert_relative_imports(code, filename)
    # 在cell開頭加入檔案路徑作為註解
    nb.cells.append(new_code_cell(f'# File: {filename}\n' + modified_code))

# 儲存為 .ipynb 檔案
output_path = os.path.join(folder_path, 'merged_notebook.ipynb')
with open(output_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print(f'✅ Notebook 已成功儲存為 {output_path}')