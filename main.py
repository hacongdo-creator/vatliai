import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. Cấu hình giao diện di động
st.set_page_config(page_title="AI Physics - Bóng rổ", layout="centered")

st.title("🏀 Mô phỏng Vật lí AI: Ném bóng rổ")
st.markdown("---")

# 2. Thanh điều khiển (Sidebar)
st.sidebar.header("⚙️ Thông số ném")
mode = st.sidebar.selectbox("Chế độ ném", ["Ném từ mặt đất", "Ném từ độ cao h (Bóng rổ)"])

v0 = st.sidebar.slider("Vận tốc đầu v0 (m/s)", 5, 50, 20)
angle = st.sidebar.slider("Góc ném (độ)", 0, 90, 45)

if mode == "Ném từ độ cao h (Bóng rổ)":
    h0 = st.sidebar.slider("Chiều cao ném (h)", 1.0, 3.0, 2.0)
    target_x = st.sidebar.slider("Khoảng cách rổ (m)", 5.0, 20.0, 10.0)
    target_y = 3.05 # Chiều cao rổ tiêu chuẩn
else:
    h0 = 0.0

g = 9.8

# 3. Tính toán Vật lí
angle_rad = np.radians(angle)
vx0 = v0 * np.cos(angle_rad)
vy0 = v0 * np.sin(angle_rad)

# Giải phương trình bậc 2 để tìm thời gian bay: -0.5gt^2 + vy0.t + h0 = 0
t_flight = (vy0 + np.sqrt(vy0**2 + 2 * g * h0)) / g
t_range = np.linspace(0, t_flight, num=200)

# Tọa độ x, y
x = vx0 * t_range
y = h0 + vy0 * t_range - 0.5 * g * t_range**2

# Tính vận tốc tức thời v = sqrt(vx^2 + vy^2)
vx = np.full_like(t_range, vx0)
vy = vy0 - g * t_range
v_instant = np.sqrt(vx**2 + vy**2)

# 4. Vẽ đồ thị tương tác Plotly
fig = go.Figure()

# Đường quỹ đạo
fig.add_trace(go.Scatter(
    x=x, y=y, 
    mode='lines', 
    name='Quỹ đạo bóng',
    line=dict(color='#FF6600', width=4),
    customdata=np.stack((v_instant, t_range), axis=-1),
    hovertemplate="Tầm xa: %{x:.2f} m<br>Độ cao: %{y:.2f} m<br>Vận tốc: %{customdata[0]:.2f} m/s<br>Thời gian: %{customdata[1]:.2f} s"
))

# Vẽ rổ nếu ở chế độ bóng rổ
if mode == "Ném từ độ cao h (Bóng rổ)":
    fig.add_trace(go.Scatter(
        x=[target_x], y=[target_y],
        mode='markers+text',
        name='Vị trí rổ',
        marker=dict(size=15, color='red', symbol='circle-open', line=dict(width=3)),
        text=["Rổ"], textposition="top center"
    ))

fig.update_layout(
    xaxis=dict(title="Tầm xa (m)", range=[0, max(x)+2]),
    yaxis=dict(title="Độ cao (m)", range=[0, max(y)+2]),
    template="plotly_dark",
    height=450,
    margin=dict(l=10, r=10, t=10, b=10),
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# 5. Phân tích kết quả AI
st.subheader("💡 Phân tích từ AI")
col1, col2, col3 = st.columns(3)
col1.metric("Tầm xa", f"{max(x):.2f} m")
col2.metric("Độ cao cực đại", f"{max(y):.2f} m")
col3.metric("Thời gian bay", f"{t_flight:.2f} s")

# Tính năng AI kiểm tra xem có vào rổ không
if mode == "Ném từ độ cao h (Bóng rổ)":
    # Tìm y tại vị trí x xấp xỉ target_x
    idx = (np.abs(x - target_x)).argmin()
    y_at_target = y[idx]
    
    if abs(y_at_target - target_y) < 0.5:
        st.success("✅ TUYỆT VỜI! Bóng có khả năng đi vào rổ!")
    else:
        st.warning(f"❌ CHƯA TRÚNG! Bóng đang ở độ cao {y_at_target:.2f}m khi tới rổ.")

st.info("📌 **Hướng dẫn:** Chạm/Rê chuột vào đường kẻ trên đồ thị để xem vận tốc và tọa độ chi tiết.")