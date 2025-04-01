from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Cấu hình SQLite
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'moneyBrowser.db3')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
COMMAND_HANDLERS = {}

# Định nghĩa model (tương ứng với bảng trong SQLite)
class tblthuchi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ngay = db.Column(db.String(100), nullable=True)
    loai_giao_dich = db.Column(db.String(100), nullable=True)
    nguon_tien = db.Column(db.String(100), nullable=True)
    noi_den = db.Column(db.String(100), nullable=True)
    so_tien = db.Column(db.Float, nullable=True)
    ghi_chu = db.Column(db.String(100), nullable=True)
    danh_muc = db.Column(db.String(100), nullable=True)
    

def register_command(name):
    def decorator(func):
        COMMAND_HANDLERS[name.lower()] = func
        return func
    return decorator

@register_command('doc_du_lieu')
@register_command('xem_tat_ca')
@register_command('list_all')
def doc_du_lieu_thuchi_handler(args):
    """
    Đọc tất cả dữ liệu từ bảng tblthuchi và hiển thị.
    """
    transactions = tblthuchi.query.all()
    if not transactions:
        return "Chưa có dữ liệu thu chi nào."

    output = "\n--- Dữ liệu Thu Chi ---\n"
    output += "{:<4} {:<12} {:<10} {:<20} {:<20} {:<15} {:<30} {:<20}\n".format(
        "ID", "Ngày", "Loại", "Nguồn Tiền", "Nơi Đến", "Số Tiền", "Ghi Chú", "Danh Mục"
    )
    output += "-" * 131 + "\n"

    for giao_dich in transactions:
        output += "{:<4} {:<12} {:<10} {:<20} {:<20} {:<15.2f} {:<30} {:<20}\n".format(
            giao_dich.id,
            giao_dich.ngay if giao_dich.ngay else "",
            giao_dich.loai_giao_dich if giao_dich.loai_giao_dich else "",
            giao_dich.nguon_tien if giao_dich.nguon_tien else "",
            giao_dich.noi_den if giao_dich.noi_den else "",
            giao_dich.so_tien if giao_dich.so_tien is not None else 0.00,
            giao_dich.ghi_chu if giao_dich.ghi_chu else "",
            giao_dich.danh_muc if giao_dich.danh_muc else ""
        )
    output += "-" * 131
    return output

@register_command('clear')
@register_command('cls')
def clear_output_handler(args):
    return {'clear_output': True} # Trả về một flag đặc biệt

@register_command('help')
@register_command('?')
def help_handler(args):
    output = "Các lệnh khả dụng:\n"
    for command in COMMAND_HANDLERS:
        output += f"- {command}\n"
    return output

def execute_command(command_string):
    parts = command_string.lower().split()
    if not parts:
        return ""
    action = parts[0]
    args = parts[1:]

    if action in COMMAND_HANDLERS:
        handler = COMMAND_HANDLERS[action]
        return handler(args)
    else:
        return f"Lệnh '{action}' không được hỗ trợ. Nhập 'help' hoặc '?' để xem danh sách lệnh."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    command = data.get('command', '')
    result = execute_command(command)
    if isinstance(result, dict) and 'clear_output' in result:
        return jsonify(result)
    return jsonify({'result': result})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)