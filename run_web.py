#!/usr/bin/env python3
"""
AI图像真伪检测系统 - Web界面启动脚本
"""

import os
import sys
from app import app

if __name__ == '__main__':
    print("=" * 50)
    print("🔍 AI图像真伪检测系统 - Web界面")
    print("=" * 50)
    print()
    
    # 检查必要的目录和文件
    if not os.path.exists('pretrained_weights/model_v11_ViT_384_base_ckpt.pt'):
        print("❌ 错误：找不到预训练模型文件")
        print("请确保 'pretrained_weights/model_v11_ViT_384_base_ckpt.pt' 文件存在")
        sys.exit(1)
    
    print("✅ 预训练模型文件检查通过")
    print("🚀 正在启动Web服务器...")
    print()
    print("📱 访问地址：http://localhost:5000")
    print("🔄 按 Ctrl+C 停止服务器")
    print()
    
    try:
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败：{e}")
        sys.exit(1) 