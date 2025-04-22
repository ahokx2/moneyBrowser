from models import tblthuchi, vtonghopgiaodich, vbieudophantramnguontien, vtichluy, tbldanhmuc, tblnguonnoiden, tblsodudauky, variable
from datetime import date, datetime
from models import db
from sqlalchemy import text

# def get_giao_dich_hom_nay():
#     today = date.today().strftime('%d/%m/%Y')  # format tùy theo bạn lưu
#     return tblthuchi.query.filter_by(ngay=today).all()

# def get_giao_dich_by_date(date_str):
#     """
#     Lấy giao dịch theo ngày.
#     :param date_str: Ngày theo định dạng 'dd/mm/yyyy'
#     :return: Danh sách giao dịch
#     """
#     return tblthuchi.query.filter_by(ngay=date_str).all()

def get_giao_dich_theo_thang(month):
    # today = date.today()
    # month = today.strftime('%m/%Y')
    return tblthuchi.query.filter(tblthuchi.ngay.like(f'%/{month}')).order_by(tblthuchi.ngay.desc()).all()

# def get_tong_hop_giao_dich_thang_hien_tai():
#     today = date.today()
#     month = today.strftime('%m/%Y')
#     return vtonghopgiaodich.query.filter_by(thang=month).all()

def get_danh_muc():
    return tbldanhmuc.query.all()

def get_so_du_dau_ky_theo_thang(month):
    return tblsodudauky.query.filter_by(thang=month).all()

def get_nguon_noi_den():
    return tblnguonnoiden.query.all()

def get_tich_luy_theo_thang(month):
    return vtichluy.query.filter_by(thang=month).all()

def get_tong_hop_giao_dich_theo_thang(month):
    return vtonghopgiaodich.query.filter_by(thang=month).all()

def get_bieu_do_phan_tram_nguon_tien(): #bieu_do_phan_tram_nguon_tien dùng để lấy dữ liệu cho biểu đồ
    return vbieudophantramnguontien.query.all()

def get_bieu_do_phan_tram_nguon_tien_theo_thang(month):   #bieu_do_phan_tram_nguon_tien dùng để lấy dữ liệu cho biểu đồ theo thang
    return vbieudophantramnguontien.query.filter_by(thang=month).all()

def get_tong_hop_giao_dich_all():
    return vtonghopgiaodich.query.all()

def get_5_giao_dich_gan_nhat():
    return tblthuchi.query.order_by(tblthuchi.id.desc()).limit(5).all()

def get_variable(ten_bien):
    """
    Lấy giá trị của biến từ bảng variable.
    :param ten_bien: Tên biến cần lấy giá trị
    :return: Giá trị của biến hoặc None nếu không tìm thấy
    """
    bien = variable.query.filter_by(ten_bien=ten_bien).first()
    return bien.gia_tri if bien else None

def tinh_cuoi_ky(thang):
    """
    Cập nhật số dư cuối kỳ cho tháng `thang` và tạo số dư đầu kỳ cho tháng tiếp theo nếu chưa có.
    """
    # Bước 1: Update cuoi_ky từ vtonghopgiaodich
    update_sql = text("""
        UPDATE tblsodudauky
        SET cuoi_ky = (
            SELECT cuoi_ky
            FROM vtonghopgiaodich AS v
            WHERE v.thang = tblsodudauky.thang AND v.nguon_tien = tblsodudauky.ma_nguon
        )
        WHERE thang = :thang
    """)
    db.session.execute(update_sql, {"thang": thang})

    # Bước 2: Tính tháng kế tiếp
    thang_date = datetime.strptime(thang, "%m/%Y")
    if thang_date.month == 12:
        next_month = datetime(thang_date.year + 1, 1, 1)
    else:
        next_month = datetime(thang_date.year, thang_date.month + 1, 1)
    thang_tiep_theo = next_month.strftime("%m/%Y")

    # Bước 3: Tạo dòng mới cho tháng sau nếu chưa có
    insert_sql = text("""
        INSERT INTO tblsodudauky (thang, ma_nguon, so_tien)
        SELECT :next_month, ma_nguon, cuoi_ky
        FROM tblsodudauky
        WHERE thang = :current_month
        ON CONFLICT (thang, ma_nguon) DO UPDATE
        SET so_tien = EXCLUDED.so_tien
    """)
    db.session.execute(insert_sql, {
        "current_month": thang,
        "next_month": thang_tiep_theo
    })

    db.session.commit()
    update_variable("tinh_so_du", 1)

def update_variable(ten_bien, gia_tri):
    """
    Cập nhật giá trị của biến trong bảng variable.
    :param ten_bien: Tên biến cần cập nhật
    :param gia_tri: Giá trị mới
    :return: True nếu thành công, False nếu lỗi
    """
    try:
        bien = variable.query.filter_by(ten_bien=ten_bien).first()
        if bien:
            bien.gia_tri = gia_tri
            db.session.commit()
            return True
        else:
            print(f"Biến {ten_bien} không tồn tại.")
            return False
    except Exception as e:
        print("Lỗi khi cập nhật biến:", e)
        db.session.rollback()
        return False

def add_giao_dich_moi(data):
    """
    Lưu một giao dịch mới vào database.
    :param data: dict gồm các field tương ứng với bảng tblthuchi
    :return: True nếu thành công, False nếu lỗi
    """

    ngay_str = data.get('ngay')  # ví dụ: '2025-04-20' từ form <input type="date">
    try:
        # Parse kiểu trình duyệt gửi (yyyy-mm-dd)
        ngay_obj = datetime.strptime(ngay_str, "%Y-%m-%d")
        # Convert sang chuỗi dd/mm/yyyy
        ngay_str = ngay_obj.strftime("%d/%m/%Y")
    except Exception as e:
        print("Lỗi định dạng ngày:", e)
        return False

    try:
        giao_dich = tblthuchi(
            # ngay=data.get('ngay', date.today().strftime('%d/%m/%Y')),
            ngay = ngay_str,
            loai_giao_dich=data.get('loai_giao_dich'),
            nguon_tien=data.get('nguon_tien'),
            noi_den=data.get('noi_den'),
            so_tien=float(data.get('so_tien')),
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