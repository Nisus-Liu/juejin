import os


# 使用示例
# write_to_file('path/to/your/file', b'your data')
def write(file: str, data, mode="wb"):
    # 创建文件的目录
    os.makedirs(os.path.dirname(file), exist_ok=True)

    # 打开文件，如果文件不存在，open()函数会自动创建它
    with open(file, mode) as f:
        f.write(data)
