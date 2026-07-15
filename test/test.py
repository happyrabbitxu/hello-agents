import torch

# 检查 PyTorch 版本
print("PyTorch 版本:", torch.__version__)

# 检查 CUDA 是否可用
print("CUDA 是否可用:", torch.cuda.is_available())

# 如果 CUDA 可用，打印 GPU 数量和设备名称
if torch.cuda.is_available():
    print("可用的 GPU 数量:", torch.cuda.device_count())
    print("GPU 名称:", torch.cuda.get_device_name(0))

# 创建一个随机张量并执行简单运算
tensor = torch.rand(3, 3)
print("随机张量:\n", tensor)
result = tensor + tensor
print("张量加法结果:\n", result)

# 如果支持 CUDA，将张量移动到 GPU 并打印
if torch.cuda.is_available():
    tensor_cuda = tensor.to("cuda")
    print("移动到 CUDA 的张量:\n", tensor_cuda)