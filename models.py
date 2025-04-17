from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


db = SQLAlchemy()

class tblthuchi(db.Model):
    __tablename__ = 'tblthuchi'
    id = db.Column(db.Integer, primary_key=True)
    ngay = db.Column(db.String(100), nullable=True)
    loai_giao_dich = db.Column(db.String(100), nullable=True)
    nguon_tien = db.Column(db.String(100), db.ForeignKey('tblnguonnoiden.ma_nguon'), nullable=True)
    noi_den = db.Column(db.String(100), db.ForeignKey('tblnguonnoiden.ma_nguon'), nullable=True)
    so_tien = db.Column(db.Float, nullable=True)
    ghi_chu = db.Column(db.String(100), nullable=True)
    danh_muc = db.Column(db.String(100), db.ForeignKey('tbldanhmuc.ma_danh_muc'),
                          nullable=True)
    
    danh_muc_obj = db.relationship('tbldanhmuc', backref='danh_muc', lazy=True)

    # liên kết với bảng tblnguontiennoiden, chỉ rõ foreign_keys
    nguon_tien_obj = db.relationship('tblnguonnoiden', backref='nguon_tien', lazy=True, foreign_keys=[nguon_tien])
    noi_den_obj = db.relationship('tblnguonnoiden', backref='noi_den', lazy=True, foreign_keys=[noi_den])



class tbldanhmuc(db.Model):
    __tablename__ = 'tbldanhmuc'
    ma_danh_muc = db.Column(db.String(100), nullable=True, primary_key=True)
    ten_danh_muc = db.Column(db.String(100), nullable=True)  # 'thu' hoặc 'chi'

class tblnguonnoiden(db.Model):
    __tablename__ = 'tblnguonnoiden'
    ma_nguon = db.Column(db.String(100), nullable=True, primary_key=True)
    ten_nguon = db.Column(db.String(100), nullable=True)
    loai_tai_san = db.Column(db.String(100), nullable=True)
    ghi_chu = db.Column(db.String(100), nullable=True)

class vtonghopgiaodich(db.Model):
    __tablename__ = 'vtonghopgiaodich'    
    thang = db.Column(db.String(100), primary_key=True)
    nguon_tien = db.Column(db.String(100), primary_key=True)
    ten_nguon = db.Column(db.String(100))
    dau_ky = db.Column(db.Float)
    thu = db.Column(db.Float)
    chi = db.Column(db.Float)
    chuyen_doi = db.Column(db.Float)
    cuoi_ky = db.Column(db.Float)

class vbieudophantramnguontien(db.Model):
    __tablename__ = 'vbieudophantramnguontien' 
    thang = db.Column(db.String(100), primary_key=True)
    nguon_tien = db.Column(db.String(100), primary_key=True)
    ten_nguon = db.Column(db.String(100))
    phan_tram = db.Column(db.Float)
    tong_so_tien = db.Column(db.Float)

class vtichluy(db.Model):
    __tablename__ = 'vtichluy' 
    thang = db.Column(db.String(100), primary_key=True)
    thu = db.Column(db.Float, primary_key=True)
    chi = db.Column(db.Float, primary_key=True)
    tich_luy = db.Column(db.Float, primary_key=True)
    phan_tram_tich_luy = db.Column(db.Float, primary_key=True)

class User(UserMixin, db.Model):  # ✅ kế thừa UserMixin
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)