import os
from flask import Flask, render_template
from datetime import date
from db_utils import get_giao_dich_hom_nay, get_giao_dich_all, get_tong_hop_giao_dich_all, get_tong_hop_giao_dich_by_month, get_tong_hop_giao_dich_thang_hien_tai
from models import db

app = Flask(__name__)

# ✅ Xác định đường dẫn tuyệt đối đến file DB
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'moneyBrowser.db3')  # nếu db nằm ngoài thư mục chứa routes.py

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
hom_nay = date.today()
thang_hien_tai = hom_nay.strftime('%m/%Y')

@app.route("/")
def index():
    giao_dich_hom_nay = get_giao_dich_hom_nay()
    #giao_dich_all = get_giao_dich_all()
    tong_hop_giao_dich = get_tong_hop_giao_dich_all()
    tong_hop_giao_dich_by_month = get_tong_hop_giao_dich_by_month("03/2025")
    tong_hop_giao_dich_thang_hien_tai = get_tong_hop_giao_dich_thang_hien_tai()


    thong_ke_thang = {
        'thu': 15000000,
        'chi': 5000000
    }
    return render_template('index.html',
                           today = hom_nay,
                           thang_hien_tai = thang_hien_tai,
                           tong_hop_giao_dich = tong_hop_giao_dich,
                           tong_hop_giao_dich_thang_hien_tai = tong_hop_giao_dich_thang_hien_tai,
                           tong_hop_giao_dich_by_month = tong_hop_giao_dich_by_month,
                           giao_dich_hom_nay=giao_dich_hom_nay)

if __name__ == "__main__":
    app.run(debug=True)
