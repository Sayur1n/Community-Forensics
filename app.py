import os
import json
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import PIL
import torch
import models
import argparse

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 确保上传和结果目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

# 支持的图片格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_model(ckpt_path='pretrained_weights/model_v11_ViT_384_base_ckpt.pt', input_size=384, device='cuda'):
    """加载模型"""
    device = torch.device(device)
    ckpt = torch.load(ckpt_path, map_location=device)

    args = argparse.Namespace()
    args.model_size = 'small'
    args.patch_size = 16
    args.freeze_backbone = False
    args.input_size = input_size
    model = models.ViTClassifier(args, device=device)
    model.load_state_dict(ckpt['model'])

    return model.to(device)

def get_result_description(prob):
    """根据概率值返回结果描述"""
    if prob > 0.9:
        return "该样本被分类为生成内容，置信度很高。"
    elif prob > 0.7:
        return "该样本被分类为生成内容，置信度中等。"
    elif prob > 0.6:
        return "该样本被分类为生成内容，置信度较低。"
    elif prob > 0.5:
        return "该样本被分类为生成内容，置信度很低。"
    elif prob > 0.4:
        return "该样本被分类为真实内容，置信度很低。"
    elif prob > 0.3:
        return "该样本被分类为真实内容，置信度较低。"
    elif prob > 0.1:
        return "该样本被分类为真实内容，置信度中等。"
    else:
        return "该样本被分类为真实内容，置信度很高。"

def load_daily_results(date_str):
    """加载指定日期的结果文件"""
    result_file = os.path.join(app.config['RESULTS_FOLDER'], f"results_{date_str}.json")
    if os.path.exists(result_file):
        try:
            with open(result_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"date": date_str, "results": []}
    return {"date": date_str, "results": []}

def save_daily_results(date_str, results_data):
    """保存指定日期的结果文件"""
    result_file = os.path.join(app.config['RESULTS_FOLDER'], f"results_{date_str}.json")
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(results_data, f, indent=4, ensure_ascii=False)

# 全局模型变量
model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global model
    
    if 'file' not in request.files:
        return jsonify({'error': '没有选择文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # 保存上传的文件
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename_with_timestamp = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename_with_timestamp)
            file.save(filepath)
            
            # 加载模型（如果还没有加载）
            if model is None:
                model = load_model(device='cuda' if torch.cuda.is_available() else 'cpu')
                model.eval()
            
            # 开始检测
            start_time = time.time()
            
            # 加载图片
            input_image = PIL.Image.open(filepath).convert('RGB')
            
            # 进行推理
            with torch.no_grad():
                fake_prob = model.forward(input_image)
                fake_prob = fake_prob.item()
            
            analysis_time = round(time.time() - start_time, 2)
            
            # 准备结果
            result = {
                'filename': filename,
                'fake_probability': round(fake_prob, 4),
                'real_probability': round(1 - fake_prob, 4),
                'description': get_result_description(fake_prob),
                'analysis_time': analysis_time,
                'device': 'CUDA' if torch.cuda.is_available() else 'CPU',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'upload_time': timestamp
            }
            
            # 保存结果到每日JSON文件
            date_str = datetime.now().strftime('%Y%m%d')
            daily_results = load_daily_results(date_str)
            daily_results['results'].append(result)
            save_daily_results(date_str, daily_results)
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({'error': f'处理文件时出错: {str(e)}'}), 500
    
    return jsonify({'error': '不支持的文件格式'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/results')
def get_results():
    """获取历史检测结果"""
    all_results = []
    results_dir = app.config['RESULTS_FOLDER']
    
    if os.path.exists(results_dir):
        # 获取所有每日结果文件
        daily_files = [f for f in os.listdir(results_dir) if f.startswith('results_') and f.endswith('.json')]
        daily_files.sort(reverse=True)  # 按文件名倒序排列（最新的在前）
        
        for daily_file in daily_files:
            filepath = os.path.join(results_dir, daily_file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    daily_data = json.load(f)
                    if 'results' in daily_data:
                        # 为每个结果添加日期信息
                        for result in daily_data['results']:
                            result['date'] = daily_data.get('date', daily_file.replace('results_', '').replace('.json', ''))
                            all_results.append(result)
            except Exception as e:
                print(f"读取文件 {daily_file} 时出错: {e}")
                continue
    
    # 按时间倒序排列
    all_results.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return jsonify(all_results)

@app.route('/results/<date>')
def get_daily_results(date):
    """获取指定日期的检测结果"""
    daily_results = load_daily_results(date)
    return jsonify(daily_results)

if __name__ == '__main__':
    print("正在加载模型...")
    try:
        model = load_model(device='cuda' if torch.cuda.is_available() else 'cpu')
        model.eval()
        print("模型加载成功！")
    except Exception as e:
        print(f"模型加载失败: {e}")
        model = None
    
    print("启动Web服务器...")
    app.run(debug=True, host='0.0.0.0', port=5000) 