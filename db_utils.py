from models import tblthuchi
from datetime import date

def get_giao_dich_all():
    return tblthuchi.query.all()

def get_giao_dich_hom_nay():
    today = date.today().strftime('%Y-%m-%d')  # format tùy theo bạn lưu
    return tblthuchi.query.filter_by(ngay=today).all()

def get_tong_quan():
    tong_tien = {
        'ngan_hang': 0,
        'tien_mat': 0,
        'gui_tiet_kiem': 0
    }
    records = tblthuchi.query.all()
    for r in records:
        if r.noi_den == 'ngân hàng':
            tong_tien['ngan_hang'] += r.so_tien or 0
        elif r.noi_den == 'tiền mặt':
            tong_tien['tien_mat'] += r.so_tien or 0
        elif r.noi_den == 'gửi tiết kiệm':
            tong_tien['gui_tiet_kiem'] += r.so_tien or 0
    return tong_tien
