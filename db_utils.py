from models import tblthuchi
from models import vtonghopgiaodich
from datetime import date
from models import db

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

def get_5_giao_dich_gan_nhat():
    return tblthuchi.query.order_by(tblthuchi.ngay.desc()).limit(5).all()

def add_giao_dich_moi(data):
    """
    Lưu một giao dịch mới vào database.
    :param data: dict gồm các field tương ứng với bảng tblthuchi
    :return: True nếu thành công, False nếu lỗi
    """
    try:
        giao_dich = tblthuchi(
            ngay=data.get('ngay', date.today().strftime('%d/%m/%Y')),
            loai_giao_dich=data.get('loai_giao_dich'),
            nguon_tien=data.get('nguon_tien'),
            noi_den=data.get('noi_den'),
            so_tien=data.get('so_tien'),
            ghi_chu=data.get('ghi_chu'),
            danh_muc=data.get('danh_muc')
        )
        db.session.add(giao_dich)
        db.session.commit()
        return True
    except Exception as e:
        print("Lỗi khi thêm giao dịch:", e)
        db.session.rollback()
        return False