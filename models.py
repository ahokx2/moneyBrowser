from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class tblthuchi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ngay = db.Column(db.String(100), nullable=True)
    loai_giao_dich = db.Column(db.String(100), nullable=True)
    nguon_tien = db.Column(db.String(100), nullable=True)
    noi_den = db.Column(db.String(100), nullable=True)
    so_tien = db.Column(db.Float, nullable=True)
    ghi_chu = db.Column(db.String(100), nullable=True)
    danh_muc = db.Column(db.String(100), nullable=True)
