# import os
# import shutil
#
#
# def main():
#     copy_file("4.json")
#
# def copy_file(src_filename):
#     src_path = f'captors/{src_filename}'
#     dst_dir = 'captors_data'
#     dst_path = f'{dst_dir}/{src_filename}'
#
#     # first empty the dst_dir to address volume persisting data in container
#     for file in os.listdir(dst_dir):
#         file_path = os.path.join(dst_dir, file) # concatenation: f'{dst_dir}/{file}'
#         try:
#             if os.path.isfile(file_path):
#                 os.remove(file_path)    # empty the dir by removing the files
#             else:
#                 pass
#         except Exception as e:
#             print(f'Error removing {file_path}: {e}')
#     try:
#         shutil.copyfile(src_path, dst_path)
#     except Exception as e:
#         print(f'Error copying {src_path} to {dst_path}: {e}')
#
#
# if __name__ == '__main__':
#     main()