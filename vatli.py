import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. CẤU HÌNH TRANG (Tiêu chí V.1: Hồ sơ trình bày rõ ràng )
st.set_page_config(page_title="Vật Lí AI - Con lắc lò xo", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .step-card {
        background-color: #1e2130; padding: 20px; border-radius: 15px;
        border-left: 5px solid #00f2ff; margin-bottom: 20px;
    }
    .step-number {
        background-color: #00f2ff; color: #1e2130;
        padding: 2px 10px; border-radius: 50%; font-weight: bold; margin-right: 10px;
    }
    .challenge-card {
        background-color: #1e2130; padding: 15px; border-radius: 10px;
        border: 2px dashed #ff4b4b; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎢 Phòng Thí Nghiệm: Con Lắc Lò Xo Tương Tác")
st.caption("Ứng dụng mô phỏng tương tác kéo - thả để tạo dao động [Tiêu chí I.1, I.2]")

# 2. THANH ĐIỀU KHIỂN SIDEBAR
st.sidebar.title("⚙️ Thiết lập hệ thống")
with st.sidebar.expander("📝 Thông số vật lí", expanded=True):
    m = st.number_input("Khối lượng vật m (kg)", 0.1, 2.0, 0.5, 0.1)
    k = st.number_input("Độ cứng lò xo k (N/m)", 10.0, 100.0, 50.0, 5.0)

# TÍNH NĂNG KÉO THẢ: Học sinh chọn li độ ban đầu để thả vật
st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Thao tác thí nghiệm")
x_pull = st.sidebar.slider("Kéo vật ra khỏi VTCB (cm)", -15.0, 15.0, 10.0, 0.5)
A = abs(x_pull) / 100 # Biên độ (m)
phi = 0 if x_pull > 0 else np.pi # Pha ban đầu dựa vào hướng kéo

# Tính toán đại lượng đặc trưng
omega = np.sqrt(k / m)
T = 2 * np.pi / omega

# 3. LỘ TRÌNH KHÁM PHÁ (Tiêu chí II.2: Hiệu quả tác động người học )
st.markdown("### 📖 Hướng dẫn khám phá")
st.markdown('<div class="step-card"><span class="step-number">1</span> <b>Thao tác:</b> Sử dụng thanh trượt ở bên trái để "Kéo" vật nặng ra khỏi vị trí cân bằng (vạch 0).</div>', unsafe_allow_html=True)
st.markdown('<div class="step-card"><span class="step-number">2</span> <b>Khám phá:</b> Nhấn "BẮT ĐẦU THẢ VẬT" để xem AI mô phỏng dao động dựa trên lực kéo của bạn.</div>', unsafe_allow_html=True)
st.markdown('<div class="step-card"><span class="step-number">3</span> <b>Tư duy:</b> Khi ấn Tạm dừng, hãy soi bảng thông số để xem sự chuyển hóa giữa Động năng và Thế năng.</div>', unsafe_allow_html=True)
st.markdown('<div class="challenge-card">🎯 <b>Thử thách:</b> Kéo vật đến li độ 10cm. Hãy dự đoán vận tốc tại vị trí cân bằng là bao nhiêu? Sau đó thả vật và kiểm chứng.</div>', unsafe_allow_html=True)

# 4. TÍNH TOÁN DAO ĐỘNG
t_steps = np.linspace(0, 2 * T, num=100)
x_t = A * np.cos(omega * t_steps + phi)
v_t = -omega * A * np.sin(omega * t_steps + phi)
a_t = -(omega**2) * x_t

# 5. VẼ CON LẮC VÀ ĐỒ THỊ [Tiêu chí V.2: Demo, mô phỏng sản phẩm ]


fig = go.Figure()

# Vẽ các vạch chia tọa độ (Thước đo)
for val in range(-15, 16, 5):
    fig.add_shape(type="line", x0=val, y0=-2, x1=val, y1=-3, line=dict(color="gray", width=1))

# Vẽ lò xo (Dạng đường zigzag)
def get_spring_coords(x_end):
    points = 20
    x_coords = np.linspace(-25, x_end, points)
    y_coords = [0, 1, -1] * (points // 3) + [0] * (points % 3)
    return x_coords, y_coords

xs, ys = get_spring_coords(x_pull if 'started' not in st.session_state else x_t[0]*100)

# Lớp lò xo
fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', line=dict(color='white', width=2), name="Lò xo", hoverinfo='skip'))

# Lớp vật nặng (Hình vuông)
fig.add_trace(go.Scatter(
    x=[x_pull], y=[0], mode='markers', name='Vật nặng (m)',
    marker=dict(symbol='square', size=40, color='#ff4b4b', line=dict(color='white', width=2)),
    customdata=np.stack((v_t, a_t, t_steps), axis=-1),
    hovertemplate="Vận tốc: %{customdata[0]:.2f} m/s<br>Gia tốc: %{customdata[1]:.2f} m/s²<extra></extra>"
))

fig.update_layout(
    xaxis=dict(range=[-30, 30], title="Vị trí (cm)", gridcolor='#333'),
    yaxis=dict(range=[-5, 5], visible=False),
    template="plotly_dark", height=400,
    updatemenus=[{
        "type": "buttons", "showactive": False, "x": 0.5, "y": -0.3, "xanchor": "center",
        "buttons": [
            {"label": "🚀 BẮT ĐẦU THẢ VẬT", "method": "animate", "args": [None, {"frame": {"duration": 30, "redraw": True}, "fromcurrent": True}]},
            {"label": "⏸️ TẠM DỪNG", "method": "animate", "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]}
        ]
    }]
)

# Tạo frames chuyển động cho cả lò xo và vật nặng
frames = []
for i in range(len(t_steps)):
    curr_x = x_t[i] * 100
    xs_frame, ys_frame = get_spring_coords(curr_x)
    frames.append(go.Frame(data=[
        go.Scatter(x=xs_frame, y=ys_frame),
        go.Scatter(x=[curr_x], y=[0])
    ]))

fig.frames = frames
st.plotly_chart(fig, use_container_width=True)

# 6. HIỂN THỊ KẾT QUẢ [Tiêu chí II.1: Hiệu quả dạy và học ]
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("Chu kỳ T", f"{T:.2f} s")
col2.metric("Vận tốc cực đại", f"{omega*A:.2f} m/s")
col3.metric("Gia tốc cực đại", f"{(omega**2)*A:.2f} m/s²")

st.info("💡 **Hướng dẫn soi số liệu:** Ấn tạm dừng, sau đó đưa chuột vào 'Vật nặng' trên đồ thị để xem Vận tốc và Gia tốc tức thời tại vị trí đó.")
