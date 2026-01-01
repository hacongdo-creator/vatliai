import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. CẤU HÌNH TRANG (Tiêu chí V.1: Hồ sơ trình bày rõ ràng)
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

st.title("🎢 Phòng Thí Nghiệm: Con Lắc Lò Xo Đồ Thị Thực")
st.caption("Mô phỏng dao động duy trì và phân tích đồ thị li độ đồng bộ [Tiêu chí I.1, I.2]")

# 2. THANH ĐIỀU KHIỂN SIDEBAR
st.sidebar.title("⚙️ Thiết lập hệ thống")
with st.sidebar.expander("📝 Thông số vật lí", expanded=True):
    m = st.number_input("Khối lượng vật m (kg)", 0.1, 2.0, 0.5, 0.1)
    k = st.number_input("Độ cứng lò xo k (N/m)", 10.0, 100.0, 50.0, 5.0)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Thao tác thí nghiệm")
x_pull = st.sidebar.slider("Kéo vật ra khỏi VTCB (cm)", -15.0, 15.0, 10.0, 0.5)

# Tính toán các đại lượng động học
A = abs(x_pull) / 100 # Biên độ (m)
phi = 0 if x_pull > 0 else np.pi
omega = np.sqrt(k / m)
T = 2 * np.pi / omega

# 3. HƯỚNG DẪN KHÁM PHÁ (Tiêu chí II.2: Tác động tích cực đến người học)
st.markdown("### 📖 Hướng dẫn khám phá và Thử thách")
st.markdown('<div class="step-card"><span class="step-number">1</span> <b>Trải nghiệm:</b> Kéo thanh trượt để đặt li độ ban đầu, sau đó nhấn BẮT ĐẦU.</div>', unsafe_allow_html=True)
st.markdown('<div class="step-card"><span class="step-number">2</span> <b>Quan sát:</b> Đồ thị bên dưới sẽ vẽ ra đường hình sin của li độ x(t) đồng bộ với chuyển động của vật nặng.</div>', unsafe_allow_html=True)
st.markdown('<div class="step-card"><span class="step-number">3</span> <b>Phân tích:</b> Nhấn Tạm dừng. Rê chuột vào con lắc hoặc đồ thị để xem các giá trị Vận tốc và Gia tốc tại thời điểm đó.</div>', unsafe_allow_html=True)
st.markdown('<div class="challenge-card">🎯 <b>Thử thách:</b> Tìm vị trí trên đồ thị mà tại đó vận tốc đạt giá trị cực đại. Vị trí đó tương ứng với li độ x bằng bao nhiêu?</div>', unsafe_allow_html=True)

# 4. TẠO DỮ LIỆU DAO ĐỘNG (Duy trì mãi bằng cách tăng t_max)
t_steps = np.linspace(0, 4 * T, num=200) # Mô phỏng 4 chu kỳ
x_t = A * np.cos(omega * t_steps + phi)
v_t = -omega * A * np.sin(omega * t_steps + phi)
a_t = -(omega**2) * x_t

# 5. VẼ ĐỒ THỊ TỔNG HỢP [Tiêu chí V.2: Demo, mô phỏng sản phẩm]


# Tạo 2 đồ thị con (Subplots)
from plotly.subplots import make_subplots
fig = make_subplots(rows=2, cols=1, 
                    subplot_titles=("Mô phỏng chuyển động cơ học", "Đồ thị Li độ - Thời gian x(t)"),
                    vertical_spacing=0.15)

# --- Đồ thị 1: Con lắc lò xo ---
def get_spring_coords(x_end):
    points = 30
    x_c = np.linspace(-25, x_end, points)
    y_c = [0, 1, -1] * (points // 3) + [0] * (points % 3)
    return x_c, y_c

xs_spring, ys_spring = get_spring_coords(x_pull)
fig.add_trace(go.Scatter(x=xs_spring, y=ys_spring, mode='lines', line=dict(color='white', width=2), hoverinfo='skip'), row=1, col=1)
fig.add_trace(go.Scatter(
    x=[x_pull], y=[0], mode='markers', name='Vật nặng',
    marker=dict(symbol='square', size=40, color='#ff4b4b', line=dict(color='white', width=2)),
    customdata=np.stack((x_t*100, v_t, a_t), axis=-1),
    hovertemplate="Li độ: %{customdata[0]:.2f} cm<br>Vận tốc: %{customdata[1]:.2f} m/s<br>Gia tốc: %{customdata[2]:.2f} m/s²<extra></extra>"
), row=1, col=1)

# --- Đồ thị 2: Li độ thời gian ---
fig.add_trace(go.Scatter(
    x=t_steps, y=x_t*100, mode='lines', name='Đồ thị x(t)',
    line=dict(color='#00f2ff', width=2),
    customdata=np.stack((v_t, a_t), axis=-1),
    hovertemplate="Vận tốc: %{customdata[0]:.2f} m/s<br>Gia tốc: %{customdata[1]:.2f} m/s²<extra></extra>"
), row=2, col=1)

# Điểm đánh dấu trên đồ thị x(t)
fig.add_trace(go.Scatter(x=[0], y=[x_pull], mode='markers', marker=dict(color='yellow', size=10), name="Vị trí hiện tại"), row=2, col=1)

# 6. CẤU HÌNH ANIMATION
fig.update_layout(
    template="plotly_dark", height=700, showlegend=False,
    updatemenus=[{
        "type": "buttons", "showactive": False, "x": 0.5, "y": -0.05, "xanchor": "center",
        "buttons": [
            {"label": "🚀 BẮT ĐẦU", "method": "animate", "args": [None, {"frame": {"duration": 20, "redraw": True}, "fromcurrent": True, "mode": "immediate", "loop": True}]},
            {"label": "⏸️ TẠM DỪNG", "method": "animate", "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]}
        ]
    }]
)

fig.update_xaxes(range=[-30, 30], title_text="Vị trí vật nặng (cm)", row=1, col=1)
fig.update_xaxes(title_text="Thời gian (s)", row=2, col=1)
fig.update_yaxes(range=[-3, 3], visible=False, row=1, col=1)
fig.update_yaxes(title_text="Li độ (cm)", row=2, col=1)

# Tạo frames đồng bộ
frames = []
for i in range(len(t_steps)):
    curr_x = x_t[i] * 100
    xs_f, ys_f = get_spring_coords(curr_x)
    frames.append(go.Frame(data=[
        go.Scatter(x=xs_f, y=ys_f),
        go.Scatter(x=[curr_x], y=[0]),
        go.Scatter(x=t_steps, y=x_t*100),
        go.Scatter(x=[t_steps[i]], y=[curr_x])
    ]))

fig.frames = frames
st.plotly_chart(fig, use_container_width=True)

# 7. KẾT QUẢ ĐỘNG LỰC HỌC [Tiêu chí II.1: Hiệu quả trong dạy và học]
st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("Cơ năng hệ", f"{0.5*k*A**2:.4f} J")
c2.metric("Vận tốc cực đại", f"{omega*A:.2f} m/s")
c3.metric("Gia tốc cực đại", f"{(omega**2)*A:.2f} m/s²")
