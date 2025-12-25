import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Cấu hình giao diện di động
st.set_page_config(page_title="Vật Lí AI", layout="centered")

st.title("🍎 Mô phỏng Ném Xiên")
st.write("Chỉnh thông số và xem quỹ đạo dự đoán bên dưới")

# Thanh điều khiển ở cột bên trái (hoặc phía trên trên điện thoại)
v0 = st.slider("Vận tốc đầu v0 (m/s)", 10, 100, 40)
angle = st.slider("Góc ném (độ)", 0, 90, 45)
g = 9.8

# Tính toán Vật lí
angle_rad = np.radians(angle)
t_max = 2 * v0 * np.sin(angle_rad) / g
t_range = np.linspace(0, t_max, num=100)
x = v0 * np.cos(angle_rad) * t_range
y = v0 * np.sin(angle_rad) * t_range - 0.5 * g * t_range**2

# Vẽ đồ thị tương tác
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Quỹ đạo', line=dict(color='#00FFCC', width=4)))

fig.update_layout(
    xaxis_title="Tầm xa (m)",
    yaxis_title="Độ cao (m)",
    template="plotly_dark",
    margin=dict(l=20, r=20, t=20, b=20),
    height=400
)

# Hiển thị đồ thị
st.plotly_chart(fig, use_container_width=True)

# Kết quả phân tích (AI dự đoán)
st.success(f"📍 Tầm xa cực đại: {max(x):.2f} m")
st.info(f"🚀 Độ cao cực đại: {max(y):.2f} m")