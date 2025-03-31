from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Cấu hình SQLite
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'moneyBrowser.db3')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

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
    

@app.route("/")
def index():
    # Lấy tất cả dữ liệu từ bảng
    data = tblthuchi.query.all()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
