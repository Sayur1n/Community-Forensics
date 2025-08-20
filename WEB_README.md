# AI图像真伪检测系统 - Web界面

这是一个基于深度学习的图像真伪检测系统的Web界面，提供了友好的用户界面来上传图片并查看检测结果。

## 功能特点

- 🖼️ **图片上传**：支持拖拽上传和点击选择
- 🔍 **实时检测**：使用预训练的ViT模型进行图像真伪检测
- 📊 **结果展示**：直观的概率条和详细的结果说明
- 📈 **历史记录**：查看所有历史检测结果，支持按日期筛选
- 📊 **统计摘要**：显示检测统计信息（总数、真实/生成数量、平均耗时）
- 📱 **响应式设计**：支持桌面和移动设备
- ⚡ **快速检测**：优化的模型推理速度
- 📁 **高效存储**：按日期组织结果文件，减少文件数量

## 安装依赖

确保你已经激活了conda环境，然后安装Web界面所需的依赖：

```bash
pip install flask werkzeug
```

或者直接安装所有依赖：

```bash
pip install -r requirements.txt
```

## 启动Web服务器

### 方法1：使用启动脚本（推荐）

```bash
python run_web.py
```

### 方法2：直接运行Flask应用

```bash
python app.py
```

## 访问Web界面

启动服务器后，在浏览器中访问：

```
http://localhost:5000
```

## 命令行评估（来自 README 摘要）

如果你只需要通过命令行对图片/文件夹进行真伪评估，可按以下步骤：

1. 下载模型权重文件：
   - [Dropbox 链接](https://www.dropbox.com/scl/fi/e8titz35ci9a2ij1oq5mu/model_weights.tar?rlkey=tmyz3tjqf7b4dg071kypsgoal&st=09ud9hdj&dl=0)
   - 解压后放置到 `pretrained_weights/` 目录，确保存在 `model_v11_ViT_384_base_ckpt.pt`
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行评估（单张图片）：
   ```bash
   python main.py --input_path="test_image.jpeg" --output_path="./results_dir" --device="cuda" --checkpoint_path="pretrained_weights/model_v11_ViT_384_base_ckpt.pt"
   ```
4. 运行评估（文件夹）：
   ```bash
   python main.py --input_path="./path_to_test_images" --output_path="./results_dir" --device="cuda" --checkpoint_path="pretrained_weights/model_v11_ViT_384_base_ckpt.pt"
   ```
5. 查看结果：
   - 在 `--output_path` 指定的目录（如 `./results_dir`）下查看生成的 `.json` 结果文件。

## 使用说明

### 1. 上传图片
- 点击上传区域选择图片文件
- 或者直接将图片拖拽到上传区域
- 支持的格式：PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP

### 2. 开始检测
- 选择图片后，点击"开始检测"按钮
- 系统会自动加载模型并进行分析
- 检测过程中会显示加载动画

### 3. 查看结果
- **真实概率**：图片为真实内容的概率
- **生成概率**：图片为AI生成内容的概率
- **检测设备**：使用的计算设备（CUDA/CPU）
- **分析时间**：检测所需的时间
- **结果说明**：详细的检测结果描述

### 4. 历史记录
- 页面底部显示所有历史检测记录
- **按日期筛选**：使用日期选择器查看特定日期的结果
- **统计摘要**：显示总检测数、真实/生成图片数量、平均耗时
- 点击"刷新"按钮更新历史记录

## 文件结构

```
Community-Forensics/
├── app.py                 # Flask应用主文件
├── run_web.py            # Web界面启动脚本
├── migrate_results.py    # 结果文件迁移工具
├── templates/
│   └── index.html        # 前端界面模板
├── uploads/              # 上传文件存储目录
├── results/              # 检测结果存储目录
│   ├── results_20250630.json  # 每日结果文件（格式：results_YYYYMMDD.json）
│   └── results_20250629.json
├── pretrained_weights/   # 预训练模型文件
├── models.py             # 模型定义
├── main.py               # 命令行版本
└── requirements.txt      # 依赖列表
```

## 结果文件格式

### 每日结果文件（results_YYYYMMDD.json）
```json
{
    "date": "20250630",
    "results": [
        {
            "filename": "test_image.jpg",
            "fake_probability": 0.7009,
            "real_probability": 0.2991,
            "description": "该样本被分类为生成内容，置信度中等。",
            "analysis_time": 0.12,
            "device": "CUDA",
            "timestamp": "2025-06-30 17:27:19",
            "upload_time": "20250630_172719"
        }
    ]
}
```

## 数据迁移

如果你有旧版本的单独结果文件，可以使用迁移工具将其合并为每日文件：

```bash
python migrate_results.py
```

迁移工具会：
1. 读取所有 `result_*.json` 文件
2. 按日期分组结果
3. 创建新的 `results_YYYYMMDD.json` 文件
4. 可选择删除原始文件

## 技术栈

- **后端**：Flask (Python)
- **前端**：HTML5, CSS3, JavaScript
- **AI模型**：Vision Transformer (ViT)
- **深度学习框架**：PyTorch

## 注意事项

1. **模型文件**：确保 `pretrained_weights/model_v11_ViT_384_base_ckpt.pt` 文件存在
2. **GPU支持**：如果有CUDA GPU，系统会自动使用GPU加速
3. **文件大小**：上传文件大小限制为16MB
4. **并发处理**：当前版本为单线程处理，不支持并发请求
5. **存储优化**：结果按日期存储，减少文件数量，提高管理效率

## 故障排除

### 1. 模型加载失败
- 检查预训练模型文件是否存在
- 确保PyTorch版本兼容

### 2. 上传失败
- 检查文件格式是否支持
- 确认文件大小不超过16MB

### 3. 检测失败
- 检查图片文件是否损坏
- 查看控制台错误信息

### 4. 历史记录显示异常
- 检查结果文件格式是否正确
- 运行迁移工具整理旧文件

## 开发说明

### 添加新功能
1. 修改 `app.py` 添加新的路由
2. 更新 `templates/index.html` 添加前端界面
3. 测试功能并更新文档

### 自定义样式
- 修改 `templates/index.html` 中的CSS样式
- 支持响应式设计和主题定制

### 数据管理
- 结果文件按日期自动组织
- 支持数据迁移和清理
- 可扩展为数据库存储

## 许可证

本项目遵循原项目的许可证条款。 