import torch
print("CUDA 可用:", torch.cuda.is_available())
print("PyTorch 使用的 CUDA 版本:", torch.version.cuda)
print("CUDA device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "无")



#python main.py --input_path="images\fake\1.png" --output_path="./results_dir" --device="cuda" --checkpoint_path="pretrained_weights/model_v11_ViT_384_base_ckpt.pt"
#python main.py --input_path="images\fake" --output_path="./results_dir" --device="cuda" --checkpoint_path="pretrained_weights/model_v11_ViT_384_base_ckpt.pt"
#python main.py --input_path="images\real" --output_path="./results_dir" --device="cuda" --checkpoint_path="pretrained_weights/model_v11_ViT_384_base_ckpt.pt"