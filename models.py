from flask_sqlalchemy import SQLAlchemy

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