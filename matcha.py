import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 1. CẤU HÌNH TRANG
st.set_page_config(
    page_title="MÁTCHOA — Dashboard Quản Lý Chiến Lược & Tài Chính",
    page_icon="🍵",
    layout="wide",
)

# 2. CUSTOM CSS (Matcha Green & Soft Pink Palette)
st.markdown(
    """
    <style>
    .stApp { background-color: #FAFAFA; }
    [data-testid="stSidebar"] { background-color: #F3F8F2; border-right: 2px solid #E8F0E6; }
    h1, h2, h3, h4 { color: #1B4D3E !important; font-family: 'Segoe UI', Tahoma, Geneva, sans-serif; }
    
    /* Style cho Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #FFF0F5;
        border: 1px solid #FFC0CB;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.04);
    }
    [data-testid="stMetricValue"] { color: #D81B60 !important; font-weight: bold; }
    
    /* Tabs styling */
    button[data-baseweb="tab"] { color: #1B4D3E !important; font-weight: 600; }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #4A7C59 !important;
        color: #FFFFFF !important;
        border-radius: 8px 8px 0 0;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Màu sắc đồ thị Plotly
COLOR_MATCHA = '#1B4D3E'
COLOR_SAGE = '#4A7C59'
COLOR_PINK = '#FF69B4'
COLOR_LIGHT_PINK = '#FFC0CB'

# HEADER
st.title("🍵 MÁTCHOA — DASHBOARD QUẢN LÝ CHUỖI & TÀI CHÍNH (2026–2030)")
st.caption(
    "Dự án Khởi nghiệp Matcha Online Cloud Kitchen & Hybrid Store | Chuẩn Cấu"
    " Trúc UEH Strategic Management"
)
st.markdown("---")

# 3. SIDEBAR - CẤU HÌNH & KỊCH BẢN
st.sidebar.header("⚙️ Cấu Hình Kịch Bản Vận Hành")

# Quick Scenario Buttons
scenario = st.sidebar.radio(
    "Chọn kịch bản nhanh:",
    ["Tùy chỉnh", "Cơ sở (750 ly)", "Tăng trưởng (1,200 ly)", "Bão giá (+20% COGS)"],
)

if scenario == "Cơ sở (750 ly)":
  def_vol, def_aov, def_cogs, def_app, def_fc = 750, 35000, 10550, 25.0, 1500000
elif scenario == "Tăng trưởng (1,200 ly)":
  def_vol, def_aov, def_cogs, def_app, def_fc = 1200, 38000, 10550, 22.0, 2000000
elif scenario == "Bão giá (+20% COGS)":
  def_vol, def_aov, def_cogs, def_app, def_fc = 750, 35000, 12660, 25.0, 1500000
else:
  def_vol, def_aov, def_cogs, def_app, def_fc = 750, 35000, 10550, 25.0, 1500000

volume_monthly = st.sidebar.slider(
    "Sản lượng bán (ly/tháng)",
    min_value=100,
    max_value=3000,
    value=def_vol,
    step=50,
)
aov = st.sidebar.number_input(
    "Giá bán trung bình (AOV - VNĐ/ly)", value=def_aov, step=1000
)
cogs = st.sidebar.number_input(
    "Giá vốn hàng bán (COGS - VNĐ/ly)", value=def_cogs, step=250
)
app_fee_pct = (
    st.sidebar.slider(
        "Phí sàn giao hàng (%)",
        min_value=0.0,
        max_value=30.0,
        value=def_app,
        step=1.0,
    )
    / 100
)
fixed_cost = st.sidebar.number_input(
    "Định phí vận hành (VNĐ/tháng)", value=def_fc, step=100000
)

# TÍNH TOÁN UNIT ECONOMICS
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

# TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Tài Chính & Unit Economics",
    "⚖️ CAPEX vs OPEX & Mô Hình",
    "🍵 Menu & R&D Trend",
    "🎯 OKRs & BSC KPIs",
    "🗺️ Lộ Trình 12 Tháng",
])

# ==========================================
# TAB 1: TÀI CHÍNH & SENSITIVITY ANALYSIS
# ==========================================
with tab1:
  st.subheader("📌 Chỉ Số Tài Chính Cốt Lõi (Kịch Bản Đang Chọn)")

  col1, col2, col3, col4 = st.columns(4)
  col1.metric("Doanh thu tháng", f"{total_rev:,.0f} VNĐ")
  col2.metric(
      "Lợi nhuận ròng",
      f"{net_profit:,.0f} VNĐ",
      delta=f"{net_margin:.1f}% Margin",
  )
  col3.metric(
      "Lãi đóng góp/ly", f"{cm_per_unit:,.0f} VNĐ", delta=f"{cm_margin:.1f}%"
  )
  col4.metric(
      "Sản lượng hòa vốn",
      f"{be_volume} ly/tháng",
      delta="~3 ly/ngày (An toàn)",
      delta_color="inverse",
  )

  st.markdown("---")

  c1, c2 = st.columns(2)
  with c1:
    st.subheader("📊 Cơ Cấu Chi Phí & Lợi Nhuận Cho 1 Ly")
    df_unit = pd.DataFrame({
        "Hạng mục": [
            "Giá vốn (COGS)",
            "Phí sàn (App Fee)",
            "Lãi đóng góp (CM)",
        ],
        "Số tiền": [cogs_per_unit, app_fee_per_unit, cm_per_unit],
    })
    fig_unit = px.pie(
        df_unit,
        values="Số tiền",
        names="Hạng mục",
        hole=0.4,
        color_discrete_sequence=["#E57373", "#FFB74D", "#81C784"],
    )
    st.plotly_chart(fig_unit, use_container_width=True)

  with c2:
    st.subheader("📈 Dự Phóng Dòng Tiền Tích Lũy (Mục tiêu: 105M)")
    default_monthly_cash = max(0, int(net_profit))
    months_list = [f"Tháng {i}" for i in range(1, 11)]

    init_df = pd.DataFrame({
        "Tháng": months_list,
        "Dòng tiền giữ lại (VNĐ)": [default_monthly_cash] * 10,
    })

    edited_df = st.data_editor(
        init_df,
        column_config={
            "Tháng": st.column_config.TextColumn("Tháng", disabled=True),
            "Dòng tiền giữ lại (VNĐ)": st.column_config.NumberColumn(
                "Tiền giữ lại (VNĐ)",
                min_value=0,
                step=500000,
                format="%d VNĐ",
            ),
        },
        hide_index=True,
        use_container_width=True,
        key="cashflow_editor",
    )

    edited_df["Tích lũy (VNĐ)"] = edited_df["Dòng tiền giữ lại (VNĐ)"].cumsum()

    fig_cash = px.line(
        edited_df,
        x="Tháng",
        y="Tích lũy (VNĐ)",
        markers=True,
        text="Tích lũy (VNĐ)",
    )
    fig_cash.update_traces(
        line_color=COLOR_MATCHA,
        marker=dict(size=8, color=COLOR_PINK),
        textposition="top left",
        texttemplate="%{y:,.0f}",
    )
    fig_cash.add_hline(
        y=105000000,
        line_dash="dash",
        line_color=COLOR_PINK,
        annotation_text="🎯 Mục tiêu 105M mở Hybrid Store",
    )
    st.plotly_chart(fig_cash, use_container_width=True)

# ==========================================
# TAB 2: CAPEX VS OPEX & COMPARISON
# ==========================================
with tab2:
  st.subheader(
      "⚖️ So Sánh Mô Hình: Online Cloud Kitchen vs Cửa Hàng Truyền Thống"
  )

  col_comp1, col_comp2 = st.columns(2)
  with col_comp1:
    st.markdown("### 🛠️ So Sánh Vốn Đầu Tư Ban Đầu (CAPEX)")
    df_capex = pd.DataFrame({
        "Hạng mục đầu tư": [
            "Cọc & Thuê mặt bằng",
            "Decor & Bàn ghế",
            "Thiết bị pha chế",
            "Dụng cụ & Pháp lý",
            "TỔNG CAPEX",
        ],
        "Mátchoa Tại Nhà": [
            "0 VNĐ",
            "3.000.000 VNĐ",
            "4.500.000 VNĐ",
            "2.500.000 VNĐ",
            "10.000.000 VNĐ",
        ],
        "Cửa Hàng Truyền Thống": [
            "34.000.000 VNĐ",
            "25.000.000 VNĐ",
            "22.000.000 VNĐ",
            "9.000.000 VNĐ",
            "90.000.000 VNĐ",
        ],
        "Mức Tiết Kiệm": [
            "Tiết kiệm 100%",
            "Tiết kiệm 88.0%",
            "Tiết kiệm 79.5%",
            "Tiết kiệm 72.2%",
            "TIẾT KIỆM 88.9%",
        ],
    })
    st.table(df_capex)

  with col_comp2:
    st.markdown("### 💸 So Sánh Vận Hành & Điểm Hòa Vốn (OPEX)")
    df_opex_comp = pd.DataFrame({
        "Chỉ tiêu hàng tháng": [
            "Tiền thuê nhà cố định",
            "Điện, Nước, Wifi",
            "Chi phí nhân sự",
            "Tổng Định Phí (Fixed Cost)",
            "Sản Lượng Hòa Vốn",
        ],
        "Cloud Kitchen Tại Nhà": [
            "0 VNĐ",
            "500.000 VNĐ",
            "1.000.000 VNĐ",
            "1.500.000 VNĐ",
            "96 ly/tháng (~3 ly/ngày)",
        ],
        "Cửa Hàng Truyền Thống": [
            "10.000.000 VNĐ",
            "2.500.000 VNĐ",
            "6.000.000 VNĐ",
            "18.500.000 VNĐ",
            "1.178 ly/tháng (~39 ly/ngày)",
        ],
    })
    st.table(df_opex_comp)

  st.info(
      "💡 **Kết luận chiến lược:** Mô hình Cloud Kitchen tại nhà giúp tiết kiệm"
      " 88,9% vốn ban đầu và an toàn hòa vốn gấp 12 lần so với mặt bằng truyền"
      " thống."
  )

# ==========================================
# TAB 3: MENU & R&D TREND ANALYTICS
# ==========================================
with tab3:
  st.subheader("🍵 Quản Lý Menu & Chiến Lược R&D Sản Phẩm Trend")

  st.markdown("""
    Dự án Mátchoa áp dụng **Quy trình R&D 3 Bước**: 
    1. *Thử nghiệm hương vị (Sensory test)* ➡️ 2. *Tính COGS & Biên lợi nhuận* ➡️ 3. *Khảo sát phản hồi khách hàng*.
    """)

  # Menu Data
  menu_data = pd.DataFrame({
      "Tên món": [
          "Matcha Latte",
          "Matcha Dừa (Hot Trend)",
          "Matcha Dâu",
          "Matcha Xoài",
          "Cà Phê Kem Muối",
      ],
      "Phân loại": [
          "Cốt lõi (Core)",
          "Bắt trend (Fusion)",
          "Bắt trend (Fusion)",
          "Bắt trend (Fusion)",
          "Mở rộng (Coffee)",
      ],
      "Giá bán lẻ (VNĐ)": [35000, 39000, 39000, 39000, 29000],
      "Giá vốn COGS (VNĐ)": [10500, 11500, 12000, 11800, 8500],
      "Tỷ lệ COGS (%)": [30.0, 29.5, 30.8, 30.3, 29.3],
      "Trạng thái R&D": [
          "Menu Chính",
          "Menu Chính (Best Seller)",
          "Menu Chính",
          "Menu Chính",
          "Menu Phụ",
      ],
  })

  st.dataframe(menu_data, use_container_width=True)

  # Chart Margin
  fig_menu = px.bar(
      menu_data,
      x="Tên món",
      y=["Giá vốn COGS (VNĐ)", "Giá bán lẻ (VNĐ)"],
      barmode="group",
      title="So Sánh Giá Bán & Giá Vốn Các Món Trong Menu",
      color_discrete_sequence=[COLOR_LIGHT_PINK, COLOR_MATCHA],
  )
  st.plotly_chart(fig_menu, use_container_width=True)

# ==========================================
# TAB 4: OKRs & BSC KPIS
# ==========================================
with tab4:
  st.subheader("🎯 Quản Trị Mục Tiêu OKRs & Bản Đồ KPI (Balanced Scorecard)")

  st.markdown("### 📌 Bộ Mục Tiêu & Kết Quả Cốt Lõi (OKRs)")
  with st.expander(
      "O1: Tối ưu hiệu quả vận hành & Sức khỏe tài chính Cloud Kitchen",
      expanded=True,
  ):
    st.progress(0.85, text="KR1.1: Tích lũy dòng tiền đạt mục tiêu 105M (85%)")
    st.progress(0.95, text="KR1.2: Tỷ suất lợi nhuận ròng >= 37.8% (95%)")
    st.progress(0.90, text="KR1.3: Tỷ lệ hao hụt nguyên liệu < 2.0% (90%)")

  with st.expander("O2: Trải nghiệm khách hàng & Phát triển kênh Zalo DTC"):
    st.progress(1.00, text="KR2.1: Rating ứng dụng đạt 5.0 / 5.0 sao (100%)")
    st.progress(0.60, text="KR2.2: Đơn hàng qua Zalo Mini-App đạt 15% (60%)")

  st.markdown("---")
  st.markdown("### 📊 Bản Đồ Đo Lường BSC KPIs")
  bsc_df = pd.DataFrame([
      {
          "Viễn cảnh": "💰 Tài chính",
          "KPI cốt lõi": "Tích lũy dòng tiền ròng",
          "Mục tiêu": ">= 10tr/tháng",
          "Tần suất": "Hàng tháng",
      },
      {
          "Viễn cảnh": "👥 Khách hàng",
          "KPI cốt lõi": "Rating App giao hàng",
          "Mục tiêu": "5.0 / 5.0 sao",
          "Tần suất": "Hàng tuần",
      },
      {
          "Viễn cảnh": "⚙️ Vận hành",
          "KPI cốt lõi": "Thời gian pha chế/ly",
          "Mục tiêu": "< 90 giây/ly",
          "Tần suất": "Hàng ngày",
      },
      {
          "Viễn cảnh": "🌱 Học hỏi",
          "KPI cốt lõi": "Nhân sự đạt chuẩn SOP",
          "Mục tiêu": "100% nhân sự",
          "Tần suất": "Hàng quý",
      },
  ])
  st.table(bsc_df)

# ==========================================
# TAB 5: LỘ TRÌNH 12 THÁNG
# ==========================================
with tab5:
  st.subheader("🗺️ Lộ Trình Triển Khai Chiến Lược 12 Tháng (2026)")

  timeline_events = [
      {
          "Giai đoạn": "Quý 1 (Tháng 1-3)",
          "Trọng tâm": "Chuẩn hóa & Kênh DTC",
          "Chi tiết hành động": (
              "• Setup gian hàng Grab/ShopeeFood\n• Dán QR Zalo Loyalty trên"
              " 100% ly\n• Chuẩn hóa văn bản SOP pha chế dưới 90s"
          ),
      },
      {
          "Giai đoạn": "Quý 2 (Tháng 4-6)",
          "Trọng tâm": "Tăng trưởng & Tối ưu AOV",
          "Chi tiết hành động": (
              "• Chạy quảng cáo từ khóa 'Matcha chuẩn Nhật'\n• Ra mắt combo Bữa"
              " trưa/Cặp đôi (AOV 55k-70k)\n• Ký bao tiêu bột MK4 6-12 tháng"
          ),
      },
      {
          "Giai đoạn": "Quý 3 (Tháng 7-9)",
          "Trọng tâm": "Tích lũy & Chuẩn bị Offline",
          "Chi tiết hành động": (
              "• Đạt mốc tích lũy 105 triệu VNĐ\n• Khảo sát & chốt báo giá thiết"
              " bị cải tạo tầng trệt tại nhà thành Hybrid Store"
          ),
      },
      {
          "Giai đoạn": "Quý 4 (Tháng 10-12)",
          "Trọng tâm": "Khai trương Hybrid Store",
          "Chi tiết hành động": (
              "• Thi công cải tạo quầy Pickup & Seating Mini\n• Khai trương"
              " cửa hàng Hybrid kết hợp trải nghiệm tại chỗ & Online"
          ),
      },
  ]
  st.table(pd.DataFrame(timeline_events))

