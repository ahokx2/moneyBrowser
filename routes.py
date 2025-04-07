import os
from flask import Flask, render_template
from datetime import date
from db_utils import get_giao_dich_hom_nay, get_tong_quan, get_giao_dich_all
from models import db

app = Flask(__name__)

# ✅ Xác định đường dẫn tuyệt đối đến file DB
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'moneyBrowser.db3')  # nếu db nằm ngoài thư mục chứa routes.py

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route("/")
def index():
    # # dữ liệu demo, bạn có thể thay bằng truy vấn từ DB sau
    # today = date.today().strftime('%d/%m/%Y')
    # tong_quan = {
    #     'ngan_hang': 10000000,
    #     'tien_mat': 1200000,
    #     'gui_tiet_kiem': 5000000
    # }
    # giao_dich_hom_nay = [
    #     {'loai': 'Chuyển đổi', 'mo_ta': 'Tiền mặt ➝ Ngân hàng', 'so_tien': 500000},
    #     {'loai': 'Chi', 'mo_ta': 'Ăn trưa', 'so_tien': 50000},
    #     {'loai': 'Chi', 'mo_ta': 'Xăng xe', 'so_tien': 30000}
    # ]

    tong_quan = get_tong_quan()
    giao_dich_hom_nay = get_giao_dich_hom_nay()
    giao_dich_all = get_giao_dich_all()


    thong_ke_thang = {
        'thu': 15000000,
        'chi': 5000000
    }
    return render_template('index.html',
                           tong_quan=tong_quan,
                           giao_dich_hom_nay=giao_dich_hom_nay,
                           thong_ke_thang=thong_ke_thang,
                           giao_dich_all = giao_dich_all)

if __name__ == "__main__":
    app.run(debug=True)
