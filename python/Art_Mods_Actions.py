import os
import json
import zipfile
import shutil

def zip_files_and_folders(file_paths, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in file_paths:
            if os.path.isdir(file_path):
                for root, dirs, files in os.walk(file_path):
                    for file in files:
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.dirname(file_path)))
            else:
                zipf.write(file_path, os.path.basename(file_path))

def list_files_and_subdirectories(directory, output_dict):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), directory)
            if not file_path.endswith('png') and not file_path.endswith('gif'):
                output_dict["additionFile"].append('img/' + file_path.replace("\\", "/"))
            else:
                output_dict["imgFileList"].append('img/' + file_path.replace("\\", "/"))

# 创建 img 目录并将指定文件夹的内容复制进去
def prepare_img_folder(base_dir, folders_to_copy):
    img_dir = os.path.join(base_dir, 'img')
    os.makedirs(img_dir, exist_ok=True)
    
    for folder in folders_to_copy:
        folder_path = os.path.join(base_dir, folder)
        if os.path.exists(folder_path):
            for item in os.listdir(folder_path):
                source = os.path.join(folder_path, item)
                destination = os.path.join(img_dir, item)
                if os.path.isdir(source):
                    shutil.copytree(source, destination, dirs_exist_ok=True)
                else:
                    shutil.copy2(source, destination)

# 定义要处理的文件夹
folders_to_process = ['b3s', 'b3s_hikfem', 'b3s_hikfemsubs', 'kaervek']

# 假设当前路径为 imagepacks 目录
base_directory = os.getcwd()  # 或者使用特定路径 os.path.join(os.getcwd(), "imagepacks")

prepare_img_folder(base_directory, folders_to_process)

# 生成 boot.json
output_dict = {}
output_dict['name'] = os.getenv('MOD_NAME', 'DefaultModName')  # 从环境变量中获取模组名称
output_dict['version'] = os.getenv('MOD_VERSION', '1.0.0')  # 从环境变量中获取版本号
print(f'模组生成中请稍等...')
output_dict['styleFileList'] = []
output_dict['scriptFileList'] = []
output_dict['tweeFileList'] = []
output_dict['additionFile'] = []
output_dict['imgFileList'] = []
list_files_and_subdirectories(os.path.join(base_directory, 'img'), output_dict)
output_dict['addonPlugin'] = [
    {
      "modName": "ModLoader DoL ImageLoaderHook",
      "addonName": "ImageLoaderAddon",
      "modVersion": "^2.3.0",
      "params": [
      ]
    }
  ]
output_dict['dependenceInfo'] = [
    {
      "modName": "ModLoader DoL ImageLoaderHook",
      "version": "^2.3.0"
    }
  ]

# 将 boot.json 保存到 img 同级目录
with open(os.path.join(base_directory, 'boot.json'), 'w', encoding='utf-8') as file:
    json.dump(output_dict, file, indent=2, ensure_ascii=False)

# 要压缩的文件和文件夹路径列表
file_paths = [os.path.join(base_directory, 'img'), os.path.join(base_directory, 'boot.json')]  
# 压缩后的文件名
zip_name = output_dict['name'] + '.zip'

# 打包 img 文件夹和 boot.json
zip_files_and_folders(file_paths, zip_name)

# 删除 boot.json
os.remove(os.path.join(base_directory, 'boot.json'))

print(f'模组生成完成: {zip_name}')
