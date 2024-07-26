from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# 配置应用密钥
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'

# 创建上传文件夹
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/upload', methods=['GET', 'POST'])
def upload_and_download():
    if request.method == 'POST':
        # 文件上传处理
        if 'photo' not in request.files:
            return "No file part"
        file = request.files['photo']
        if file.filename == '':
            return "No selected file"
        if file:
            # 获取用户输入的新文件名
            new_filename = request.form.get('new_filename', file.filename)
            filename = secure_filename(new_filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f"File {filename} saved."

    # 文件列表和下载处理
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('upload.html', files=files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0')