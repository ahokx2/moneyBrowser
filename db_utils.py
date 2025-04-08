from models import tblthuchi
from models import vtonghopgiaodich
from datetime import date

def get_giao_dich_hom_nay():
    today = date.today().strftime('%d/%m/%Y')  # format tùy theo bạn lưu
    return tblthuchi.query.filter_by(ngay=today).all()

def get_giao_dich_all():
    return tblthuchi.query.all()

def get_tong_hop_giao_dich_thang_hien_tai():
    today = date.today()
    month = today.strftime('%m/%Y')
    return vtonghopgiaodich.query.filter_by(thang=month).all()

def get_tong_hop_giao_dich_by_month(month):
    return vtonghopgiaodich.query.filter_by(thang=month).all()

def get_tong_hop_giao_dich_all():
    return vtonghopgiaodich.query.all()