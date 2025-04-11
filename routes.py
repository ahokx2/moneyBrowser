import os
from flask import Flask, render_template, request, redirect
from datetime import date
from db_utils import get_giao_dich_hom_nay, get_giao_dich_all, get_tong_hop_giao_dich_all, get_tong_hop_giao_dich_by_month, get_tong_hop_giao_dich_thang_hien_tai, add_giao_dich_moi, get_5_giao_dich_gan_nhat, get_giao_dich_by_date
from models import db, tblnguonnoiden, tbldanhmuc

app = Flask(__name__)

# ✅ Xác định đường dẫn tuyệt đối đến file DB
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'moneyBrowser.db3')  # nếu db nằm ngoài thư mục chứa routes.py

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

hom_nay = date.today()  # format tùy theo bạn lưu
thang_hien_tai = hom_nay.strftime('%m/%Y')

@app.template_filter('format_tien')
def format_tien(value):
    """
    Định dạng số tiền với dấu phẩy và ký hiệu tiền tệ.
    :param value: Giá trị số tiền
    :return: Chuỗi định dạng tiền tệ
    """
    try:
        value = float(value)
        if value.is_integer():
            return f"{int(value):,}".replace(",", ".") + " đ"  # 75000000 → 75.000.000
        else:
            return f"{value:,.2f}".replace(",", ".").replace(".", ",", 1) + " đ"  # nếu có phần thập phân
    except:
        return value

@app.route("/them_giao_dich", methods=["POST"])
def them_giao_dich():
    data = request.form.to_dict()
    success = add_giao_dich_moi(data)
    if success:
        return redirect("/")  # hoặc redirect(url_for('index'))
    else:
        return "Lỗi khi thêm giao dịch", 500

@app.route("/loc_theo_ngay", methods=["GET"])
def loc_theo_ngay():
    ngay_loc = request.args.get("ngay_loc")  # yyyy-mm-dd
    if ngay_loc:
        # Convert sang dd/mm/yyyy nếu mày lưu vậy trong DB
        parts = ngay_loc.split("-")
        formatted = f"{parts[2]}/{parts[1]}/{parts[0]}"
        giao_dich = get_giao_dich_by_date(formatted)
    else:
        giao_dich = []

    return render_template("by_date.html", giao_dich_theo_ngay=giao_dich,
                           ngay_loc = ngay_loc)
    
@app.route("/")
def index():
    giao_dich_hom_nay = get_giao_dich_hom_nay()
    giao_dich_gan_nhat = get_5_giao_dich_gan_nhat()
    tong_hop_giao_dich = get_tong_hop_giao_dich_all()
    tong_hop_giao_dich_by_month = get_tong_hop_giao_dich_by_month("03/2025")
    tong_hop_giao_dich_thang_hien_tai = get_tong_hop_giao_dich_thang_hien_tai()
    danh_sach_nguon = tblnguonnoiden.query.all()
    danh_sach_danh_muc = tbldanhmuc.query.all()

    return render_template('index.html',
                           today = hom_nay,
                           thang_hien_tai = thang_hien_tai,
                           giao_dich_gan_nhat = giao_dich_gan_nhat,
                           tong_hop_giao_dich = tong_hop_giao_dich,
                           tong_hop_giao_dich_thang_hien_tai = tong_hop_giao_dich_thang_hien_tai,
                           tong_hop_giao_dich_by_month = tong_hop_giao_dich_by_month,
                           giao_dich_hom_nay=giao_dich_hom_nay,
                           danh_sach_nguon=danh_sach_nguon,
                           danh_sach_danh_muc=danh_sach_danh_muc)

if __name__ == "__main__":
    app.run(debug=True)
