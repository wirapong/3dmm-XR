import os
import shutil
import random

# 设置随机种子，确保结果可复现
random.seed(42)

# 原始数据目录
data_dir = "data"
# 训练集目录
train_dir = os.path.join(data_dir, "train")
# 测试集目录
test_dir = os.path.join(data_dir, "test")

# 创建训练集和测试集目录（如果不存在）
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# 获取所有图片和对应的mat文件路径
image_paths = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".jpg")]
mat_paths = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.endswith(".mat")]

# 按文件名关联图片和mat文件，构建配对列表（假设文件名除后缀外一致）
pairs = []
image_name_set = {os.path.splitext(os.path.basename(p))[0] for p in image_paths}
mat_name_set = {os.path.splitext(os.path.basename(p))[0] for p in mat_paths}
common_names = image_name_set & mat_name_set

for name in common_names:
    img_path = os.path.join(data_dir, f"{name}.jpg")
    mat_path = os.path.join(data_dir, f"{name}.mat")
    pairs.append((img_path, mat_path))

# 计算划分比例（80%训练，20%测试）
total = len(pairs)
test_size = int(total * 0.2)
train_size = total - test_size

print(f"总样本数: {total}, 训练集: {train_size}, 测试集: {test_size}")

# 随机划分训练集和测试集
test_pairs = random.sample(pairs, test_size)
train_pairs = [p for p in pairs if p not in test_pairs]

# 将训练集文件移动到train目录并改名
for idx, (img_path, mat_path) in enumerate(train_pairs, start=1):
    new_img_name = f"train_{idx}.jpg"
    new_mat_name = f"train_{idx}.mat"
    shutil.move(img_path, os.path.join(train_dir, new_img_name))
    shutil.move(mat_path, os.path.join(train_dir, new_mat_name))

# 将测试集文件移动到test目录并改名
for idx, (img_path, mat_path) in enumerate(test_pairs, start=1):
    new_img_name = f"test_{idx}.jpg"
    new_mat_name = f"test_{idx}.mat"
    shutil.move(img_path, os.path.join(test_dir, new_img_name))
    shutil.move(mat_path, os.path.join(test_dir, new_mat_name))

print(f"已完成划分，训练集目录: {train_dir}，测试集目录: {test_dir}")
