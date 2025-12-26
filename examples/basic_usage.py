from dircraft import DirectoryCreator

folder_paths = [
    'project_root/src',
    'project_root/tests',
    'project_root/docs',
    'project_root/assets/images',
    'project_root/assets/styles'
]

creator = DirectoryCreator()
creator.create(folder_paths)

print("✅ Folder structure created successfully")