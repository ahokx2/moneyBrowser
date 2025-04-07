from flask import Flask, render_template
from datetime import date

app = Flask(__name__)

@app.route("/")
def index():
    # dữ liệu demo, bạn có thể thay bằng truy vấn từ DB sau
    today = date.today().strftime('%d/%m/%Y')
    tong_quan = {
        'ngan_hang': 10000000,
        'tien_mat': 1200000,
        'gui_tiet_kiem': 5000000
    }
    giao_dich_hom_nay = [
        {'loai': 'Chuyển đổi', 'mo_ta': 'Tiền mặt ➝ Ngân hàng', 'so_tien': 500000},
        {'loai': 'Chi', 'mo_ta': 'Ăn trưa', 'so_tien': 50000},
        {'loai': 'Chi', 'mo_ta': 'Xăng xe', 'so_tien': 30000}
    ]
    thong_ke_thang = {
        'thu': 15000000,
        'chi': 5000000
    }
    return render_template('index.html',
                           today=today,
                           tong_quan=tong_quan,
                           giao_dich_hom_nay=giao_dich_hom_nay,
                           thong_ke_thang=thong_ke_thang)

if __name__ == "__main__":
    app.run(debug=True)
