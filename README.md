🍵 MÁTCHOA — Strategic Management & Financial Dashboard
📌 Giới Thiệu Dự Án
MÁTCHOA Dashboard là ứng dụng tương tác phân tích dữ liệu và giả lập tài chính dành cho mô hình kinh doanh Matcha Online Cloud Kitchen & Hybrid Store.
Dự án thuộc nghiên cứu chiến lược và tài chính của PK-Team Analytic — UEH Strategic Management, hỗ trợ cấp quản lý mô phỏng kịch bản kinh doanh theo thời gian thực (Real-time Scenario Planning), đánh giá các chỉ số Unit Economics, tối ưu hóa chi phí CAPEX/OPEX, theo dõi lộ trình OKRs/BSC và lập kế hoạch tích lũy dòng tiền tái đầu tư.
🌟 Tính Năng Nổi Bật
⚙️ 1. Bộ Mô Phỏng Kịch Bản Tài Chính (Sidebar Scenario Planner)
•	Kịch bản thiết lập sẵn:
o	🟢 Cơ sở: Sản lượng 750 ly/tháng.
o	🚀 Tăng trưởng: Sản lượng 1,000 ly/tháng.
o	🔻 Thấp: Sản lượng 350 ly/tháng.
o	⚡ Bão giá: COGS tăng +20%.
o	🛠️ Tùy chỉnh: Cho phép thay đổi linh hoạt mọi biến số.
•	Tham số đầu vào tùy biến:
o	Biến phí per unit: Sản lượng (Volume), Giá bán trung bình ($AOV$), Giá vốn nguyên liệu ($COGS$), Phí chiết khấu sàn (% App Fee).
o	Định phí hàng tháng: Điện/nước/wifi tăng thêm, chi phí công chủ/nhân sự linh hoạt.
📊 2. Phân Hệ Quản Lý Chiến Lược (6 Tabs Chức Năng)
Tab	Tên phân hệ	Mô tả chi tiết
Tab 1	📈 Tài Chính & Unit Economics	Theo dõi Doanh thu, Net Profit, $CM$/ly, Sản lượng hòa vốn. Tích hợp cảnh báo sức khỏe tài chính dynamic và biểu đồ dự phóng dòng tiền tích lũy 105M VNĐ.
Tab 2	⚖️ CAPEX vs OPEX	Bảng so sánh trực quan vốn đầu tư ban đầu (tiết kiệm 88.9% CAPEX) và áp lực chi phí cố định giữa Cloud Kitchen vs Store truyền thống.
Tab 3	🍵 Menu & Quy Trình R&D	Quản lý danh mục món (Menu lõi, Best-seller, Combo kèm) cùng tỷ lệ $COGS$ định mức và trạng thái SOP / Recipe Sheet.
Tab 4	🎯 OKRs & BSC KPIs	Đánh giá tiến độ OKRs 4 giai đoạn và bản đồ Balanced Scorecard theo 4 viễn cảnh (Tài chính, Khách hàng, Vận hành, Học hỏi).
Tab 5	🗺️ Lộ Trình Thực Thi	Kế hoạch hành động chi tiết 4 giai đoạn từ hoàn thiện SOP $\rightarrow$ Kênh Zalo DTC $\rightarrow$ Tích lũy vốn $\rightarrow$ Mở Hybrid Store.
Tab 6	💡 Khuyến Nghị CEO	Tổng hợp 3 ưu tiên chiến lược hàng đầu và nguyên tắc kỷ luật tài chính 100% vốn tự có (không nợ vay).
📂 Cấu Trúc Thư Mục Dự Án
matchoa-dashboard/
│
├── .streamlit/
│   └── config.toml          # Cấu hình giao diện Streamlit (Matcha Palette)
├── app.py                   # Mã nguồn chính của ứng dụng Streamlit
├── requirements.txt         # Các thư viện Python phụ thuộc
└── README.md                # Tài liệu hướng dẫn dự án

🚀 Hướng Dẫn Cài Đặt Và Khởi Chạy
1. Yêu cầu hệ thống
•	Python 3.9 hoặc phiên bản cao hơn.
•	Trình quản lý gói pip.
2. Clone Repository
git clone https://github.com/your-username/matchoa-dashboard.git
cd matchoa-dashboard

3. Cài đặt các thư viện phụ thuộc
pip install -r requirements.txt

4. Khởi chạy ứng dụng Streamlit
streamlit run app.py

🌐 Ứng dụng sẽ tự động mở tại địa chỉ: http://localhost:8501
📋 Tóm Tắt Chỉ Số Mô Hình Cơ Sở (Base Scenario)
Mô hình: Online Cloud Kitchen Tại Nhà (750 ly/tháng)
-----------------------------------------------------------------
• Giá bán trung bình (AOV)     : 35.000 VNĐ / ly
• Giá vốn nguyên liệu (COGS)   : 10.550 VNĐ / ly (30.1%)
• Phí sàn chiết khấu (App Fee) : 25.0% (8.750 VNĐ / ly)
• Lãi đóng góp (CM / ly)       : 15.700 VNĐ / ly (44.9%)
• Định phí cố định hàng tháng  : 1.500.000 VNĐ / tháng
• Điểm hòa vốn (Break-even)    : ~96 ly / tháng (~4 ly / ngày)
• Tiết kiệm vốn đầu tư CAPEX   : 10.000.000 VNĐ (Tiết kiệm 88.9%)
-----------------------------------------------------------------

🎨 Bảng Màu Giao Diện (Brand Theme Palette)
•	Matcha Green: #1B4D3E (Màu chủ đạo / Header)
•	Sage Green: #4A7C59 (Accent color / Tab highlight)
•	Soft Pink: #FFC0CB & #FFF0F5 (Card background & Container)
•	Hot Pink: #D81B60 (Metric values & Highlights)
👥 Thống Kê Dự Án & Đội Ngũ
•	Đơn vị phát triển: PK-Team Analytic
•	Môn học: UEH Strategic Management
•	Đóng góp: Mọi đóng góp (Pull Request / Issue) cho dự án đều được hoan nghênh.

