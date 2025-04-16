import os
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from datetime import date
from db_utils import get_giao_dich_all, get_tong_hop_giao_dich_all, get_tong_hop_giao_dich_by_month, get_tong_hop_giao_dich_thang_hien_tai, add_giao_dich_moi, get_5_giao_dich_gan_nhat, get_giao_dich_by_date, get_giao_dich_thang_hien_tai, get_giao_dich_by_date, get_bieu_do_phan_tram_nguon_tien, get_bieu_do_phan_tram_nguon_tien_by_month
from models import db, tblnguonnoiden, tbldanhmuc, tblthuchi, User, vbieudophantramnguontien, vtonghopgiaodich
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
import unicodedata

app = Flask(__name__)

# ✅ Xác định đường dẫn tuyệt đối đến file DB
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'moneyBrowser.db3')  # nếu db nằm ngoài thư mục chứa routes.py

# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

#cái này là external, dùng để dev tại máy cá nhân
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ahokx2:DE2xekSNBsFUCcechR6u84bnnWvPDYkH@dpg-cvui9ommcj7s73ceqjjg-a.oregon-postgres.render.com/moneybrowser_44q3'

# cái này là internal, dùng trên render
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ahokx2:DE2xekSNBsFUCcechR6u84bnnWvPDYkH@dpg-cvui9ommcj7s73ceqjjg-a/moneybrowser_44q3'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'some_very_secret_key'

login_manager = LoginManager()
login_manager.login_view = 'login'  # tên của route login
login_manager.init_app(app)

db.init_app(app)

def remove_accents(text):
    text = text.replace('đ', 'd').replace('Đ', 'D')  # xử lý riêng
    nfkd_form = unicodedata.normalize('NFKD', text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower().replace(" ", "")

app.jinja_env.filters['slugify'] = remove_accents

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

@app.route('/api/data')
def api_data():
    loai = request.args.get("loai")
    today = date.today().strftime('%Y-%m-%d')

    if loai == 'tblthuchi':
        data = tblthuchi.query.order_by(tblthuchi.ngay.desc()).all()
        result = [{
            "ngay": g.ngay,
            "loai_giao_dich": g.loai_giao_dich,
            "so_tien": g.so_tien,
            "ghi_chu": g.ghi_chu
        } for g in data]

        return jsonify({
            "success": True,
            "tieu_de": "Danh sách giao dịch chi tiết",
            "data": result
        })

    elif loai == 'tonghop':
        data = vtonghopgiaodich.query.order_by(vtonghopgiaodich.thang.desc()).all()
        result = [{
            "thang": i.thang,
            "nguon_tien": i.nguon_tien,
            "ten_nguon": i.ten_nguon,
            "dau_ky": i.dau_ky,
            "thu": i.thu,
            "chi": i.chi,
            "chuyen_doi": i.chuyen_doi,
            "cuoi_ky": i.cuoi_ky
        } for i in data]

        return jsonify({
            "success": True,
            "tieu_de": "Báo cáo tổng hợp theo tháng",
            "data": result
        })

    else:
        return jsonify({
            "success": False,
            "tieu_de": "Lỗi",
            "message": "Không xác định được loại yêu cầu",
            "data": []
    })

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
    loai = request.args.get('loai')
    data = []
    data1 = []
    tieu_de = "Chào mừng!"
    tieu_de_data = ""
    tieu_de_data1 = ""
    kieu = None  # để điều khiển kiểu hiển thị trong template

    if loai == 'tblthuchi':
        data = tblthuchi.query.order_by(tblthuchi.ngay.desc()).all()
        tieu_de = "Danh sách giao dịch chi tiết"
        kieu = 'chi_tiet'

    elif loai == 'tonghop':
        data = vtonghopgiaodich.query.order_by(vtonghopgiaodich.thang.desc()).all()
        tieu_de = "Báo cáo tổng hợp theo tháng"
        kieu = 'tong_hop'

    else :
        data = get_5_giao_dich_gan_nhat()
        data1 = get_bieu_do_phan_tram_nguon_tien_by_month(thang_hien_tai)
        tieu_de = "Tổng quan tài chính"
        tieu_de_data = "Danh sách giao dịch gần nhất"
        tieu_de_data1 = "Phần trăm nguồn tiền"
        kieu = 'tong_quan_tai_chinh'

    return render_template('index.html', tieu_de=tieu_de, data=data, data1=data1, kieu=kieu, tieu_de_data=tieu_de_data, tieu_de_data1=tieu_de_data1)

if __name__ == "__main__":
    app.run(debug=True)
