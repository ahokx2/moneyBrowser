from models import tblthuchi, vtonghopgiaodich, vbieudophantramnguontien
from datetime import date
from models import db

def get_giao_dich_hom_nay():
    today = date.today().strftime('%d/%m/%Y')  # format tùy theo bạn lưu
    return tblthuchi.query.filter_by(ngay=today).all()

def get_giao_dich_by_date(date_str):
    """
    Lấy giao dịch theo ngày.
    :param date_str: Ngày theo định dạng 'dd/mm/yyyy'
    :return: Danh sách giao dịch
    """
    return tblthuchi.query.filter_by(ngay=date_str).all()

def get_giao_dich_all():
    return tblthuchi.query.all()

def get_giao_dich_thang_hien_tai():
    today = date.today()
    month = today.strftime('%m/%Y')
    return tblthuchi.query.filter(tblthuchi.ngay.like(f'%/{month}')).order_by(tblthuchi.ngay.desc()).all()

def get_tong_hop_giao_dich_thang_hien_tai():
    today = date.today()
    month = today.strftime('%m/%Y')
    return vtonghopgiaodich.query.filter_by(thang=month).all()

def get_tong_hop_giao_dich_by_month(month):
    return vtonghopgiaodich.query.filter_by(thang=month).all()

def get_bieu_do_phan_tram_nguon_tien(): #bieu_do_phan_tram_nguon_tien dùng để lấy dữ liệu cho biểu đồ
    return vbieudophantramnguontien.query.all()

def get_bieu_do_phan_tram_nguon_tien_by_month(month):   #bieu_do_phan_tram_nguon_tien dùng để lấy dữ liệu cho biểu đồ theo thang
    return vbieudophantramnguontien.query.filter_by(thang=month).all()

def get_tong_hop_giao_dich_all():
    return vtonghopgiaodich.query.all()

def get_5_giao_dich_gan_nhat():
    return tblthuchi.query.order_by(tblthuchi.id.desc()).limit(5).all()

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
        print(data)
        db.session.commit()
        return True
    except Exception as e:
        print("Lỗi khi thêm giao dịch:", e)
        db.session.rollback()
        return False