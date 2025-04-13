import os
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from datetime import date
from db_utils import get_giao_dich_all, get_tong_hop_giao_dich_all, get_tong_hop_giao_dich_by_month, get_tong_hop_giao_dich_thang_hien_tai, add_giao_dich_moi, get_5_giao_dich_gan_nhat, get_giao_dich_by_date, get_giao_dich_thang_hien_tai, get_giao_dich_by_date, get_bieu_do_phan_tram_nguon_tien, get_bieu_do_phan_tram_nguon_tien_by_month
from models import db, tblnguonnoiden, tbldanhmuc, tblthuchi, User, vbieudophantramnguontien
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin

app = Flask(__name__)

# ✅ Xác định đường dẫn tuyệt đối đến file DB
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'moneyBrowser.db3')  # nếu db nằm ngoài thư mục chứa routes.py

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'some_very_secret_key'

login_manager = LoginManager()
login_manager.login_view = 'login'  # tên của route login
login_manager.init_app(app)

db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Sai tài khoản hoặc mật khẩu", "danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/api/phantram-nguontien')
def get_bieu_do_nguon_tien():
    thang = request.args.get('thang')
    # data = vbieudophantramnguontien.query.filter_by(thang=thang).all()
    # data = get_bieu_do_phan_tram_nguon_tien_by_month(thang)
    data = get_tong_hop_giao_dich_by_month(thang)
    result = [
        {
            "nguon_tien": item.nguon_tien,
            "ten_nguon": item.ten_nguon,
            "phan_tram_cuoi_ky": item.cuoi_ky
        }
        for item in data
    ]
    return jsonify(result)

@app.route("/them_giao_dich", methods=["POST"])
def them_giao_dich():
    data = request.form.to_dict()
    success = add_giao_dich_moi(data)
    if success:
        return redirect("/")  # hoặc redirect(url_for('index'))
    else:
        return "Lỗi khi thêm giao dịch", 500

@app.route("/xoa_giao_dich/<int:id>")
def xoa_giao_dich(id):
    gd = tblthuchi.query.get_or_404(id)
    db.session.delete(gd)
    db.session.commit()
    return redirect(request.referrer or "/")

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
    
@app.route("/", methods = ["GET"])
@login_required
def index():
    # giao_dich_hom_nay = get_giao_dich_hom_nay()
    # giao_dich_gan_nhat = get_5_giao_dich_gan_nhat()
    # tong_hop_giao_dich = get_tong_hop_giao_dich_all()
    # tong_hop_giao_dich_by_month = get_tong_hop_giao_dich_by_month("03/2025")
    # tong_hop_giao_dich_thang_hien_tai = get_tong_hop_giao_dich_thang_hien_tai()
    danh_sach_nguon = tblnguonnoiden.query.all()
    danh_sach_danh_muc = tbldanhmuc.query.all()

    ngay_loc = request.args.get("ngay_loc")  # xem giao dịch theo ngày
    xem_thang = request.args.get("xem_thang") # xem giao dịch tháng hiện tại

    if ngay_loc:
        # Convert sang dd/mm/yyyy nếu mày lưu vậy trong DB
        parts = ngay_loc.split("-")
        formatted = f"{parts[2]}/{parts[1]}/{parts[0]}"
        giao_dich = get_giao_dich_by_date(formatted) # lấy giao dịch theo ngày
        title = f"Giao dịch ngày {formatted}"
    elif xem_thang:
        giao_dich = get_giao_dich_thang_hien_tai() # lấy giao dịch tháng hiện tại
        title = "Giao dịch tháng hiện tại : " + thang_hien_tai
    else:
        giao_dich = get_5_giao_dich_gan_nhat() # lấy 5 giao dịch gần nhất
        title = "5 giao dịch gần nhất"
        bieu_do_thang_hien_tai = get_bieu_do_phan_tram_nguon_tien_by_month(thang_hien_tai) # lấy biểu đồ theo tháng hiện tại

    return render_template('index.html',
                           today = hom_nay,
                           thang_hien_tai = thang_hien_tai,
                           title = title,
                           giao_dich = giao_dich,
                           bieu_do_thang_hien_tai = bieu_do_thang_hien_tai,
                           danh_sach_nguon = danh_sach_nguon,
                           danh_sach_danh_muc = danh_sach_danh_muc)

if __name__ == "__main__":
    app.run(debug=True)
