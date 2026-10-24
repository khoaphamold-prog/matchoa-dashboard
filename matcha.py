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
    
    div[data-testid="metric-container"] {
        background-color: #FFF0F5;
        border: 1px solid #FFC0CB;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.04);
    }
    [data-testid="stMetricValue"] { color: #D81B60 !important; font-weight: bold; }
    
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

# COLOR PALETTE
COLOR_MATCHA = '#1B4D3E'
COLOR_SAGE = '#4A7C59'
COLOR_PINK = '#FF69B4'
COLOR_LIGHT_PINK = '#FFC0CB'

# HEADER
st.title("🍵 MÁTCHOA — DASHBOARD QUẢN LÝ CHUỖI & TÀI CHÍNH")
st.caption(
    "Dự án Khởi nghiệp Matcha Online Cloud Kitchen & Hybrid Store | PK- Team"
    " Analytic - UEH Strategic Management"
)
st.markdown("---")

# 3. SIDEBAR - CẤU HÌNH CÓ TÙY CHỈNH FLEXIBLE
st.sidebar.header("⚙️ Cấu Hình Chi Phí & Doanh Thu")

# Thêm lại 'Tùy chỉnh' ở đầu danh sách chọn
scenario = st.sidebar.radio(
    "Chọn kịch bản kịch bản mẫu:",
    [
        "Tùy chỉnh",
        "Cơ sở (750 ly)",
        "Tăng trưởng (1,000 ly)",
        "Thấp (350 ly)",
        "Bão giá (+20% COGS)",
    ],
)

if scenario == "Cơ sở (750 ly)":
  def_vol, def_aov, def_cogs, def_app = 750, 35000, 10550, 25.0
  def_util, def_lab = 500000, 1000000
elif scenario == "Tăng trưởng (1,000 ly)":
  def_vol, def_aov, def_cogs, def_app = 1000, 35000, 10550, 25.0
  def_util, def_lab = 700000, 1200000
elif scenario == "Thấp (350 ly)":
  def_vol, def_aov, def_cogs, def_app = 350, 35000, 10550, 25.0
  def_util, def_lab = 300000, 500000
elif scenario == "Bão giá (+20% COGS)":
  def_vol, def_aov, def_cogs, def_app = 750, 34000, 12660, 25.0
  def_util, def_lab = 500000, 1000000
else:
  # Giá trị mặc định khi chọn "Tùy chỉnh"
  def_vol, def_aov, def_cogs, def_app = 750, 35000, 10550, 25.0
  def_util, def_lab = 500000, 1000000

st.sidebar.subheader("📌 1. Doanh thu & Chi phí biến đổi (Per Unit)")
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
    "Giá vốn nguyên liệu (COGS - VNĐ/ly)", value=def_cogs, step=250
)
app_fee_pct = (
    st.sidebar.slider(
        "Phí chiết khấu sàn (%/đơn)",
        min_value=0.0,
        max_value=30.0,
        value=def_app,
        step=1.0,
    )
    / 100
)

st.sidebar.subheader("📌 2. Định phí hàng tháng (Fixed Costs tại nhà)")
cost_util = st.sidebar.number_input(
    "Điện, nước, wifi tăng thêm (VNĐ)", value=def_util, step=50000
)
cost_lab = st.sidebar.number_input(
    "Tiền công linh hoạt (VNĐ)", value=def_lab, step=100000
)

# TỔNG ĐỊNH PHÍ
fixed_cost = cost_util + cost_lab

# TÍNH TOÁN UNIT ECONOMICS THEO BÁO CÁO (MỤC 3.7.1)
rev_per_unit = aov
cogs_per_unit = cogs
app_fee_per_unit = aov * app_fee_pct
cm_per_unit = rev_per_unit - cogs_per_unit - app_fee_per_unit
cm_margin = (cm_per_unit / rev_per_unit) * 100 if rev_per_unit > 0 else 0

total_rev = volume_monthly * rev_per_unit
total_cogs = volume_monthly * cogs_per_unit
total_app_fee = volume_monthly * app_fee_per_unit
total_cm = volume_monthly * cm_per_unit

net_profit = total_cm - fixed_cost
net_margin = (net_profit / total_rev) * 100 if total_rev > 0 else 0
be_volume = int(fixed_cost / cm_per_unit) if cm_per_unit > 0 else 0

# TABS
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Tài Chính & Unit Economics",
    "⚖️ CAPEX vs OPEX & Mô Hình",
    "🍵 Menu & R&D Trend",
    "🎯 OKRs & BSC KPIs",
    "🗺️ Lộ Trình Thực Thi",
    "💡 Tổng Kết & Khuyến Nghị CEO",
])

# ==========================================
# TAB 1: TÀI CHÍNH & DÒNG TIỀN
# ==========================================
with tab1:
  st.subheader("📌 Chỉ Số Tài Chính Cốt Lõi (Kịch Bản Đang Chọn)")

  col1, col2, col3, col4 = st.columns(4)
  col1.metric("Doanh thu tháng", f"{total_rev:,.0f} VNĐ")
  col2.metric(
      "Lợi nhuận ròng tháng",
      f"{net_profit:,.0f} VNĐ",
      delta=f"{net_margin:.1f}% Margin",
  )
  col3.metric(
      "Lãi đóng góp/ly", f"{cm_per_unit:,.0f} VNĐ", delta=f"{cm_margin:.1f}%"
  )
  col4.metric(
      "Sản lượng hòa vốn",
      f"{be_volume} ly/tháng",
      delta=f"~{int(be_volume/30)} ly/ngày",
      delta_color="inverse",
  )

  st.markdown("---")

  # THÔNG BÁO DỰA TRÊN SỨC KHỎE TÀI CHÍNH DYNAMIIC
  if net_profit >= 10000000:
    st.success(
        f"✅ **SỨC KHỎE TÀI CHÍNH RẤT TỐT!**\n\nMô hình đạt lợi nhuận ròng"
        f" **{net_profit:,.0f} VNĐ/tháng** (Margin **{net_margin:.1f}%**). Dự"
        f" án sẽ hoàn thành tích lũy 105 triệu VNĐ trong khoảng"
        f" **{105000000/net_profit:.1f} tháng** để giải ngân mở Hybrid Store."
    )
  elif net_profit > 0:
    st.warning(
        f"⚠️ **SỨC KHỎE TÀI CHÍNH TRUNG BÌNH!**\n\nLợi nhuận ròng đạt"
        f" **{net_profit:,.0f} VNĐ/tháng**. Thời gian tích lũy đủ 105 triệu VNĐ"
        f" kéo dài lên **{105000000/net_profit:.1f} tháng**. Cần đẩy mạnh kênh"
        " Zalo DTC để cắt chiết khấu sàn 25%."
    )
  else:
    st.error(
        "🚨 **CẢNH BÁO: KỊCH BẢN ĐANG LỖ!** Cần điều chỉnh lại giá bán hoặc"
        " khóa giá trần bột MK4."
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
    st.subheader("📈 Dự Phóng Tích Lũy Dòng Tiền (Mục tiêu 105 Triệu VNĐ)")
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
        annotation_text="🎯 Mục tiêu 105M (Mục 3.7.4)",
    )
    st.plotly_chart(fig_cash, use_container_width=True)

# ==========================================
# TAB 2: CAPEX VS OPEX
# ==========================================
with tab2:
  st.subheader(
      "⚖️ So Sánh Mô Hình: Online Cloud Kitchen vs Cửa Hàng Truyền Thống"
  )

  col_comp1, col_comp2 = st.columns(2)
  with col_comp1:
    st.markdown("### 🛠️ Vốn Đầu Tư Ban Đầu (CAPEX - Mục 3.7.2)")
    df_capex = pd.DataFrame({
        "Hạng mục đầu tư": [
            "Cọc & Thuê mặt bằng",
            "Decor thương hiệu & Bàn ghế",
            "Thiết bị pha chế & bảo quản",
            "Dụng cụ, bao bì, pháp lý",
            "TỔNG CAPEX BAN ĐẦU",
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
    st.markdown("### 💸 Định Phí & Điểm Hòa Vốn (OPEX - Mục 3.7.3)")
    df_opex_comp = pd.DataFrame({
        "Chỉ tiêu hàng tháng": [
            "Tiền thuê mặt bằng cố định",
            "Điện, Nước, Wifi (tăng thêm)",
            "Nhân sự / Công chủ quán",
            "Tổng Định Phí (Fixed Cost)",
            "Lãi đóng góp / ly (CM)",
            "Sản Lượng Hòa Vốn (Ly/tháng)",
        ],
        "Cloud Kitchen Tại Nhà": [
            "0 VNĐ",
            "500.000 VNĐ",
            "1.000.000 VNĐ",
            "1.500.000 VNĐ",
            f"{cm_per_unit:,.0f} VNĐ",
            f"{be_volume} ly/tháng",
        ],
        "Cửa Hàng Truyền Thống": [
            "10.000.000 VNĐ",
            "2.500.000 VNĐ",
            "6.000.000 VNĐ",
            "18.500.000 VNĐ",
            "24.450 VNĐ (không phí sàn)",
            "757 ly/tháng (~25 ly/ngày)",
        ],
    })
    st.table(df_opex_comp)

  st.info(
      "💡 **Kết luận từ Báo cáo:** Tận dụng nhà ở giúp tiết kiệm 88,9% CAPEX"
      " và có sản lượng hòa vốn an toàn hơn gấp nhiều lần so với việc thuê cửa"
      " hàng truyền thống ngay từ đầu."
  )

# ==========================================
# TAB 3, 4, 5, 6 GIỮ NGUYÊN
# ==========================================
with tab3:
  st.subheader("🍵 Quản Lý Menu & Quy Trình R&D 3 Bước")
  menu_data = pd.DataFrame({
      "Tên món": [
          "Matcha Latte (Lõi)",
          "Matcha Dừa (Best Seller)",
          "Matcha Dâu (Fusion)",
          "Matcha Xoài (Fusion)",
          "Pudding Chuối (Món kèm)",
      ],
      "Phân loại": [
          "Menu Lõi",
          "Món theo mùa / Trend",
          "Món theo mùa / Trend",
          "Món theo mùa / Trend",
          "Món ăn kèm Combo",
      ],
      "Giá bán lẻ (VNĐ)": [35000, 39000, 39000, 39000, 20000],
      "Giá vốn COGS (VNĐ)": [10500, 11500, 12000, 11800, 5500],
      "Tỷ lệ COGS (%)": [30.0, 29.5, 30.8, 30.3, 27.5],
      "Trạng thái SOP": [
          "Đã có Recipe Sheet",
          "Đã có Recipe Sheet",
          "Đã có Recipe Sheet",
          "Đã có Recipe Sheet",
          "Đã có Recipe Sheet",
      ],
  })
  st.dataframe(menu_data, use_container_width=True)
  fig_menu = px.bar(
      menu_data,
      x="Tên món",
      y=["Giá vốn COGS (VNĐ)", "Giá bán lẻ (VNĐ)"],
      barmode="group",
      title="So Sánh Giá Bán & COGS Định Mức Cho Từng Món",
      color_discrete_sequence=[COLOR_LIGHT_PINK, COLOR_MATCHA],
  )
  st.plotly_chart(fig_menu, use_container_width=True)

with tab4:
  st.subheader("🎯 Hệ Thống OKRs & Bản Đồ KPI Balanced Scorecard")
  with st.expander(
      "O1 (Ngắn hạn 0–3 tháng): Hoàn thiện menu chuẩn hóa & Khóa chi phí đầu"
      " vào",
      expanded=True,
  ):
    st.progress(
        1.00, text="KR1: Chốt menu chính thức lõi/mùa/kèm & loại món lỗi (100%)"
    )
    st.progress(
        0.90, text="KR2: 100% món có Recipe Sheet (gram/ml) & COGS <30% (90%)"
    )
    st.progress(
        0.80, text="KR3: Ký hợp đồng bao tiêu MK4 giá trần 6-12 tháng (80%)"
    )
    st.progress(
        1.00, text="KR4: 100% ly giao đi có dán mã QR Zalo Mini-App (100%)"
    )

  with st.expander(
      "O2 (Trung hạn 3–12 tháng): Chuẩn hóa thương hiệu & Phát triển kênh riêng"
      " Zalo DTC"
  ):
    st.progress(
        0.60, text="KR2: Đạt 15% tổng lượng đơn hàng qua kênh riêng Zalo (60%)"
    )
    st.progress(0.95, text="KR3: Duy trì Rating app >= 4.8 sao (95%)")
    st.progress(
        0.70, text="KR4: Nâng AOV từ 35k lên 55k nhờ combo Bữa trưa/Đôi (70%)"
    )

  st.markdown("---")
  bsc_df = pd.DataFrame([
      {
          "Viễn cảnh": "💰 Tài chính",
          "KPI cốt lõi": "Lợi nhuận giữ lại / tháng",
          "Mục tiêu": "~10.000.000 VNĐ",
          "Tần suất": "Hàng tháng",
          "Phụ trách": "Tài chính",
      },
      {
          "Viễn cảnh": "👥 Khách hàng",
          "KPI cốt lõi": "Rating trung bình sàn",
          "Mục tiêu": "5.0 (Tối thiểu 4.8)",
          "Tần suất": "Hàng tuần",
          "Phụ trách": "Marketing",
      },
      {
          "Viễn cảnh": "👥 Khách hàng",
          "KPI cốt lõi": "Tỷ lệ đơn qua kênh Zalo DTC",
          "Mục tiêu": "15% tổng lượng đơn",
          "Tần suất": "Hàng tháng",
          "Phụ trách": "Marketing",
      },
      {
          "Viễn cảnh": "⚙️ Vận hành",
          "KPI cốt lõi": "Thời gian pha chế chuẩn",
          "Mục tiêu": "< 90 giây / ly",
          "Tần suất": "Hàng tuần",
          "Phụ trách": "Vận hành",
      },
      {
          "Viễn cảnh": "🌱 Học hỏi",
          "KPI cốt lõi": "Nhân sự nắm vững SOP",
          "Mục tiêu": "100% nhân sự",
          "Tần suất": "Hàng quý",
          "Phụ trách": "Vận hành",
      },
  ])
  st.table(bsc_df)

with tab5:
  st.subheader("🗺️ Lộ Trình Thực Thi Working Plan Theo Báo Cáo")
  timeline_events = [
      {
          "Giai đoạn": "1. Hoàn thiện Menu & SOP",
          "Thời gian": "Tháng 1–3",
          "Công việc chính": (
              "Chốt menu; viết Recipe Sheet (gram/ml) & tính COGS; ký hợp đồng"
              " MK4 giá trần; dán mã QR Zalo 100% ly; cơ giới hóa máy đánh"
              " trà tự động."
          ),
          "Sản phẩm đầu ra": "Menu chính thức, Bộ văn bản SOP, Hợp đồng MK4",
      },
      {
          "Giai đoạn": "2. Thương hiệu & Kênh riêng",
          "Thời gian": "Tháng 4–9",
          "Công việc chính": (
              "Hoàn thiện bộ nhận diện; chạy quảng cáo từ khóa; vận hành Zalo"
              " Mini-App đạt 15% đơn; ra mắt combo Bữa trưa/Đôi nâng AOV lên"
              " 55k."
          ),
          "Sản phẩm đầu ra": (
              "Bộ hướng dẫn thương hiệu, 15% đơn qua Zalo, Tích lũy 10M/tháng"
          ),
      },
      {
          "Giai đoạn": "3. Tích lũy & Chuẩn bị cửa hàng",
          "Thời gian": "Tháng 10–12",
          "Công việc chính": (
              "Đánh giá rà soát 7 nhóm điều kiện mục 3.2.1; xác nhận thủ tục"
              " pháp lý địa điểm; chạy thử điểm Pickup; lấy báo giá cải tạo."
          ),
          "Sản phẩm đầu ra": "Hồ sơ quyết định giải ngân 105 triệu VNĐ",
      },
      {
          "Giai đoạn": "4. Mở cửa hàng Hybrid",
          "Thời gian": "Tháng 12–36",
          "Công việc chính": (
              "Giải ngân 105M tự có; thi công cải tạo tầng trệt tại nhà;"
              " lắp thiết bị công nghiệp; khai trương cửa hàng Hybrid đầu"
              " tiên."
          ),
          "Sản phẩm đầu ra": "Cửa hàng Hybrid Store chuẩn vận hành",
      },
  ]
  st.table(pd.DataFrame(timeline_events))

with tab6:
  st.subheader("💡 Tổng Kết Chiến Lược & Đề Xuất Cho CEO Mátchoa")
  c_rec1, c_rec2 = st.columns(2)
  with c_rec1:
    st.markdown("### 📌 3 Hành Động Ưu Tiên Hàng Đầu (Mục 5.2 Báo cáo)")
    st.markdown("""
        1. **Ưu tiên Ngắn hạn (0–3 tháng):** Hoàn thiện menu chính thức, chuẩn hóa công thức bằng văn bản Recipe Sheet/SOP và khóa chi phí đầu vào bằng hợp đồng giá trần MK4 (ST1).
        2. **Ưu tiên Trung hạn (3–12 tháng):** Chuẩn hóa bộ nhận diện thương hiệu và chuyển đổi 15% lượng đơn qua kênh Zalo Mini-App (WO1) để tiết kiệm 20–30% phí sàn.
        3. **Năng lực cạnh tranh cốt lõi:** Biến quan hệ độc quyền MK4 thành lợi thế nhìn thấy bằng cách kể câu chuyện nguồn gốc ở mọi điểm chạm.
        """)
  with c_rec2:
    st.markdown("### 🎯 Khuyến Nghị Dài Hạn & Điều Kiện Giải Ngân")
    st.markdown("""
        * **Kỷ luật giải ngân mở cửa hàng:** Chỉ mở cửa hàng vật lý Hybrid Store khi đã **đạt đủ 7 nhóm điều kiện** tại Mục 3.2.1 của Báo cáo.
        * **Đảm bảo không nợ vay:** Tuyệt đối dùng 100% dòng tiền ròng tích lũy từ Cloud Kitchen để tự đầu tư, triệt tiêu hoàn toàn rủi ro tài chính.
        """)
  st.markdown("---")
  st.info(
      "💡 **Thông điệp cốt lõi:** Tận dụng mô hình Cloud Kitchen tinh gọn làm"
      " nền tảng tích lũy vốn an toàn, tạo đà mở rộng bền vững sang mô hình"
      " Hybrid Store mà không gánh chi phí cố định quá sớm."
  )

