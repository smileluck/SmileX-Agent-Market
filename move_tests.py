import os
import shutil

# 获取当前目录
dir_path = os.path.dirname(os.path.abspath(__file__))

# 目标目录
target_dir = os.path.join(dir_path, 'script', 'test')

# 确保目标目录存在
os.makedirs(target_dir, exist_ok=True)

# 列出所有需要移动的测试文件
test_files = [
    'simple_log_test.py',
    'simple_test.py',
    'test_db_save.py',
    'test_log_chinese.py',
    'test_log_encoding.py',
    'test_logger.py',
    'test_module.py',
    'test_search.py'
]

# 移动文件（先复制再删除）
for file in test_files:
    src = os.path.join(dir_path, file)
    dst = os.path.join(target_dir, file)
    if os.path.exists(src):
        print(f"复制文件: {src} -> {dst}")
        shutil.copy2(src, dst)
        print(f"删除原始文件: {src}")
        os.remove(src)
    else:
        print(f"文件不存在: {src}")

print("所有测试文件已移动完成!")

# 验证移动结果
print("\n目标目录内容:")
for file in os.listdir(target_dir):
    print(f"  {file}")

print("\n当前目录剩余文件:")
for file in os.listdir(dir_path):
    if file.startswith('test_') or file.startswith('simple_'):
        print(f"  {file}")