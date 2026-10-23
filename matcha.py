import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Cấu hình trang Dashboard
st.set_page_config(
    page_title="MÁTCHOA - Dashboard Quản Lý Chiến Lược & Tài Chính",
    page_icon="🍵",
    layout="wide"
)

# Custom CSS cho phông màu Xanh Matcha & Hồng Nữ Tính
st.markdown("""
    <style>
    /* Bảng màu chính: Matcha Green (#6B8E23 / #8FBC8F) & Pink (#FFB6C1 / #FF69B4) */
    
    /* Nền chính & Sidebar */
    .stApp {
        background-color: #FAFAFA;
    }
    [data-testid="stSidebar"] {
        background-color: #F3F8F2;
        border-right: 2px solid #E8F0E6;
    }
    
    /* Header & Tiêu đề */
    h1, h2, h3, h4 {
        color: #4A6B32 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Thẻ Chỉ số Metric Box (Tone Hồng & Matcha) */
    [data-testid="stMetricValue"] {
        color: #D81B60 !important;
        font-weight: bold;
    }
    div[data-testid="metric-container"] {
        background-color: #FFF0F5;
        border: 1px solid #FFC0CB;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.03);
    }
    
    /* Tab bar */
    button[data-baseweb="tab"] {
        color: #556B2F !important;
        font-weight: 600;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #FFB6C1 !important;
        color: #FFFFFF !important;
        border-radius: 8px 8px 0 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header chính
st.title("🍵 MÁTCHOA — DASHBOARD QUẢN LÝ CHUỖI & TÀI CHÍNH (2026–2030)")
st.caption("Dự án Khởi nghiệp Matcha Cloud Kitchen & Hybrid Store | UEH Strategic Management")
st.markdown("---")

# Palette màu Plotly chuẩn Matcha Green & Pink
COLOR_MATCHA = '#6B8E23'
COLOR_PINK = '#FF69B4'
COLOR_LIGHT_PINK = '#FFC0CB'
COLOR_DARK_GREEN = '#3B5323'
COLOR_MINT = '#98FB98'

# Sidebar cấu hình
st.sidebar.header("⚙️ Cấu Hình Kịch Bản Vận Hành")
volume_monthly = st.sidebar.slider("Sản lượng bán (ly/tháng)", min_value=100, max_value=3000, value=750, step=50)
aov = st.sidebar.number_input("Giá bán trung bình (AOV - VNĐ/ly)", value=35000, step=1000)
cogs = st.sidebar.number_input("Giá vốn hàng bán (COGS - VNĐ/ly)", value=10550, step=250)
app_fee_pct = st.sidebar.slider("Phí sàn giao hàng (%)", min_value=0.0, max_value=30.0, value=25.0, step=1.0) / 100
fixed_cost = st.sidebar.number_input("Định phí vận hành (VNĐ/tháng)", value=1500000, step=100000)

# Tính toán các chỉ số Unit Economics
rev_per_unit = aov
cogs_per_unit = cogs
app_fee_per_unit = aov * app_fee_pct
cm_per_unit = rev_per_unit - cogs_per_unit - app_fee_per_unit
cm_margin = (cm_per_unit / rev_per_unit) * 100 if rev_per_unit > 0 else 0

total_rev = volume_monthly * rev_per_unit
total_cm = volume_monthly * cm_per_unit
net_profit = total_cm - fixed_cost
net_margin = (net_profit / total_rev) * 100 if total_rev > 0 else 0
be_volume = int(fixed_cost / cm_per_unit) if cm_per_unit > 0 else 0
# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Tài Chính & Unit Economics", "⚖️ CAPEX vs OPEX", "🎯 BSC & KPIs", "🗺️ Lộ Trình 12 Tháng"])
# TAB 1: TÀI CHÍNH & UNIT ECONOMICS
# ---------------------------------------------------------
with tab1:
    st.subheader("📌 Chỉ Số Tài Chính Cốt Lõi (Theo Kịch Bản Cấu Hình)")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Doanh thu tháng", f"{total_rev:,.0f} VNĐ")
    col2.metric("Lợi nhuận ròng", f"{net_profit:,.0f} VNĐ", delta=f"{net_margin:.1f}% Margin")
    col3.metric("Lãi đóng góp/ly", f"{cm_per_unit:,.0f} VNĐ", delta=f"{cm_margin:.1f}%")
    col4.metric("Sản lượng hòa vốn", f"{be_volume} ly/tháng", delta="~3 ly/ngày", delta_color="inverse")

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📊 Cơ Cấu Chi Phí & Lợi Nhuận Cho 1 Ly (AOV = 35k)")
        df_unit = pd.DataFrame({
            'Hạng mục': ['Giá vốn (COGS)', 'Phí sàn (App Fee)', 'Lãi đóng góp (CM)'],
            'Số tiền': [cogs_per_unit, app_fee_per_unit, cm_per_unit]
        })
        fig_unit = px.pie(df_unit, values='Số tiền', names='Hạng mục', hole=0.4,
                          color_discrete_sequence=['#ef553b', '#ffa15a', '#00cc96'])
        st.plotly_chart(fig_unit, use_container_width=True)

    with c2:
        st.subheader("📈 Dự Phóng Dòng Tiền Tích Lũy (Mục tiêu 105Tr)")
        months = [f"Tháng {i}" for i in range(1, 11)]
        cumulative_cash = [net_profit * i for i in range(1, 11)]
        df_cash = pd.DataFrame({'Tháng': months, 'Tích lũy (VNĐ)': cumulative_cash})

        fig_cash = px.line(df_cash, x='Tháng', y='Tích lũy (VNĐ)', markers=True,
                           title="Dòng tiền giữ lại để mở rộng Hybrid Store (Mục tiêu 105 triệu VNĐ)")
        fig_cash.add_hline(y=105000000, line_dash="dash", line_color="red", annotation_text="Mục tiêu 105M")
        st.plotly_chart(fig_cash, use_container_width=True)
# TAB 2: CAPEX VS OPEX
# ---------------------------------------------------------
with tab2:
    st.subheader("⚖️ Cân Đối Chi Phí Đầu Tư (CAPEX) & Vận Hành (OPEX)")

    col_cap1, col_cap2 = st.columns(2)

    with col_cap1:
        st.write("### 🛠️ Chi Phí Đầu Tư Ban Đầu (CAPEX) - Ước Tính")
        capex_data = pd.DataFrame({
            'Hạng mục đầu tư': ['Trang thiết bị máy móc', 'Thiết kế & Decor tối giản', 'Ký quỹ mặt bằng (nếu có)', 'Giấy phép & Setup ban đầu'],
            'Chi phí (VNĐ)': [45000000, 20000000, 15000000, 5000000]
        })
        st.table(capex_data)
        total_capex = capex_data['Chi phí (VNĐ)'].sum()
        st.metric("Tổng CAPEX dự kiến", f"{total_capex:,.0f} VNĐ")

    with col_cap2:
        st.write("### 💸 Chi Phí Vận Hành Hàng Tháng (OPEX) - Kịch Bản")
        # Phí biến đổi dựa trên sản lượng vận hành hiện tại
        total_cogs_monthly = volume_monthly * cogs_per_unit
        total_app_fees_monthly = volume_monthly * app_fee_per_unit

        opex_data = pd.DataFrame({
            'Chi phí vận hành': ['Giá vốn hàng bán (COGS)', 'Phí sàn giao hàng', 'Định phí (Marketing, Mặt bằng, Điện nước...)'],
            'Chi phí/Tháng (VNĐ)': [total_cogs_monthly, total_app_fees_monthly, fixed_cost]
        })

        fig_opex = px.bar(opex_data, x='Chi phí vận hành', y='Chi phí/Tháng (VNĐ)',
                          title="Cơ cấu chi phí vận hành hàng tháng (OPEX)",
                          color='Chi phí vận hành', color_discrete_sequence=['#1f77b4', '#aec7e8', '#ff7f0e'])
        st.plotly_chart(fig_opex, use_container_width=True)
      # TAB 3: BSC & KPIS
# ---------------------------------------------------------
with tab3:
    st.subheader("🎯 Bản Đồ Đo Lường Hiệu Quả (Balanced Scorecard - BSC)")

    bsc_data = [
        {"Viễn cảnh": "💰 Tài chính", "KPI": "Lợi nhuận tích lũy giữ lại", "Mục tiêu": ">= 10.000.000 VNĐ/tháng", "Tần suất": "Hàng tháng"},
        {"Viễn cảnh": "💰 Tài chính", "KPI": "Tỷ suất lợi nhuận ròng", "Mục tiêu": ">= 37,8%", "Tần suất": "Hàng tháng"},
        {"Viễn cảnh": "👥 Khách hàng", "KPI": "Đánh giá Rating App (Grab/Shopee)", "Mục tiêu": "5.0 / 5.0 sao", "Tần suất": "Hàng tuần"},
        {"Viễn cảnh": "👥 Khách hàng", "KPI": "Tỷ lệ đơn DTC qua Zalo Mini-App", "Mục tiêu": ">= 15% tổng đơn", "Tần suất": "Hàng tuần"},
        {"Viễn cảnh": "⚙️ Vận hành", "KPI": "Thời gian pha chế hoàn tất/ly", "Mục tiêu": "< 90 giây / ly", "Tần suất": "Hàng ngày"},
        {"Viễn cảnh": "⚙️ Vận hành", "KPI": "Tỷ lệ hao hụt nguyên liệu", "Mục tiêu": "< 2.0% / tháng", "Tần suất": "Hàng ngày"},
        {"Viễn cảnh": "🌱 Học hỏi & Phát triển", "KPI": "Tỷ lệ nhân sự thuộc chuẩn SOP", "Mục tiêu": "100% nhân sự", "Tần suất": "Hàng quý"},
    ]
    st.table(pd.DataFrame(bsc_data))
  # TAB 4: LỘ TRÌNH 12 THÁNG
# ---------------------------------------------------------
with tab4:
    st.subheader("🗺️ Lộ Trình Triển Khai Chiến Lược & Mở Rộng 12 Tháng")
    
    st.markdown("""
    ### 📅 Các Cột Mốc Quan Trọng Năm 1 (2026)
    Hành trình phát triển từ mô hình tinh gọn **Cloud Kitchen** đạt hiệu quả tối ưu (DTC) và tích luỹ ngân sách để chuyển đổi sang mô hình **Hybrid Store**.
    """)
    
    timeline_events = [
        {"Giai đoạn": "Tháng 1 - 3", "Tập trung chính": "Thử nghiệm & Tinh chỉnh", "Chi tiết hành động": "Setup gian hàng Cloud Kitchen trên Grab/Shopee Food; Triển khai Zalo Mini-App; Định vị chuẩn vị sản phẩm Matcha UEH.", "Trạng thái": "Chuẩn bị"},
        {"Giai đoạn": "Tháng 4 - 6", "Tập trung chính": "Tối ưu hóa Chi Phí & Doanh Thu", "Chi tiết hành động": "Chạy chiến dịch giảm phụ thuộc app sàn thông qua ưu đãi đặt trực tiếp (DTC); Đưa biên lợi nhuận ròng đạt mục tiêu >30%.", "Trạng thái": "Chuẩn bị"},
        {"Giai đoạn": "Tháng 7 - 9", "Tập trung chính": "Tích lũy & Chuẩn bị Mặt bằng", "Chi tiết hành động": "Tích lũy đủ hạn mức tài chính tối thiểu (~105 triệu VNĐ) từ dòng tiền giữ lại; Khảo sát tìm mặt bằng phù hợp cho Hybrid Store tại Quận 3/Quận 10.", "Trạng thái": "Chuẩn bị"},
        {"Giai đoạn": "Tháng 10 - 12", "Tập trung chính": "Khai trương Hybrid Store", "Chi tiết hành động": "Chuyển đổi sang mô hình Hybrid Store (kết hợp trải nghiệm tại chỗ và Cloud Kitchen giao hàng tận nơi); Đẩy mạnh trải nghiệm khách hàng.", "Trạng thái": "Chuẩn bị"}
    ]
    
    df_timeline = pd.DataFrame(timeline_events)
    
    # Hiển thị timeline bằng bảng
    st.table(df_timeline)
    
    # Thêm sơ đồ minh họa lộ trình tích lũy tài chính nhanh gọn
    st.info("💡 **Thông điệp cốt lõi:** Lợi nhuận tích lũy từ mô hình Cloud Kitchen tinh gọn chính là nguồn vốn an toàn nhất để tự tái đầu tư mở rộng cửa hàng Hybrid mà không cần huy động nợ vay quá sớm ở giai đoạn đầu.")
