from flask import Flask, jsonify, render_template, request, redirect, url_for, send_file, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret_key"
BASE_DIR = "/Users/apple/Desktop/Python/2nd_Grade/Competition/TEAM-CLICK"
UPLOAD_DIR = os.path.join(BASE_DIR, "asset/images/input")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        student_id = request.form['studentId']
        student_name = request.form['studentName']
        file_path = os.path.join(UPLOAD_DIR, f"{student_id}.png")
        
        if os.path.exists(file_path):
            flash("중복된 입력입니다. 학번을 다시 입력해주세요.")
            return redirect(url_for('index'))

        return redirect(url_for('upload_image', student_id=student_id))
    return render_template('index.html')

@app.route('/upload/<student_id>', methods=['GET', 'POST'])
def upload_image(student_id):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('파일이 업로드되지 않았습니다.')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('선택된 파일이 없습니다.')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{student_id}.png")
            file.save(os.path.join(UPLOAD_DIR, filename))
            flash('파일이 성공적으로 업로드되었습니다.')
            return render_template('upload.html', student_id=student_id, upload_success=True)
        
        flash('허용되지 않는 파일 형식입니다. PNG 또는 JPG 파일만 가능합니다.')
        return redirect(request.url)
    
    return render_template('upload.html', student_id=student_id, upload_success=False)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(UPLOAD_DIR, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
