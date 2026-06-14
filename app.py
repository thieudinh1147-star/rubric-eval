import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ── Cấu hình trang ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Đánh giá Playlist",
    page_icon="🎵",
    layout="centered"
)

# ── CSS tối giống Spotify ────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Nền tối toàn trang */
    .stApp { 
        background-color: #121212; 
        color: #ffffff; 
    }

    section[data-testid="stSidebar"] { 
        background-color: #000000; 
    }

    /* Tiêu đề */
    h1, h2, h3, h4 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Chữ thường */
    p, span, label, div {
        color: #ffffff !important;
    }

    /* Tab */
    .stTabs [data-baseweb="tab-list"] { 
        background-color: #000000; 
        border-radius: 8px; 
    }

    .stTabs [data-baseweb="tab"] { 
        color: #b3b3b3 !important; 
    }

    .stTabs [aria-selected="true"] { 
        color: #1DB954 !important; 
        border-bottom: 2px solid #1DB954; 
    }

    /* Nút submit */
    .stButton > button {
        background-color: #1DB954;
        color: #000000 !important;
        border-radius: 24px;
        border: none;
        font-weight: 600;
        padding: 10px 32px;
        width: 100%;
    }

    .stButton > button:hover { 
        background-color: #1ed760; 
        color: #000000 !important; 
    }

    /* Input text */
    .stTextInput input { 
        background-color: #2a2a2a; 
        color: #ffffff !important; 
        border-color: #535353; 
    }

    /* Card bài hát đang phát */
    .now-playing-card {
        background-color: #1a1a1a;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
        border: 1px solid #2a2a2a;
    }

    /* Danh sách bài hát */
    .song-item {
        background-color: #1a1a1a;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .song-item:hover { 
        background-color: #2a2a2a; 
    }

    .song-number { 
        color: #b3b3b3 !important; 
        font-size: 13px; 
        width: 20px; 
    }

    .song-title-text { 
        color: #ffffff !important; 
        font-size: 14px; 
        font-weight: 500; 
    }

    .song-artist-text { 
        color: #b3b3b3 !important; 
        font-size: 12px; 
    }

    /* Rubric section */
    .rubric-card {
        background-color: #1a1a1a;
        border-radius: 12px;
        padding: 20px;
        margin-top: 16px;
        border: 1px solid #2a2a2a;
    }

    /* Làm rõ label của phần chấm điểm */
    [data-testid="stWidgetLabel"] p {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }

    /* Làm rõ caption giải thích thang điểm */
    .stCaption, .stCaption p {
        color: #dddddd !important;
        font-size: 14px !important;
    }

    /* Hộp thang điểm màu Spotify */
    .scale-box {
        background-color: #1DB954;
        color: #000000 !important;
        padding: 14px 18px;
        border-radius: 12px;
        margin-bottom: 22px;
        border: none;
    }

    .scale-box p {
        color: #000000 !important;
        margin: 0;
        font-weight: 700;
    }

    .scale-box .scale-detail {
        margin-top: 8px;
        font-weight: 600;
    }

    /* Làm rõ phần slider */
    [data-testid="stSlider"] {
        background-color: #171717;
        padding: 14px 18px 18px 18px;
        border-radius: 12px;
        margin-bottom: 18px;
        border: 1px solid #2f2f2f;
    }

    /* Tên tiêu chí */
    [data-testid="stSlider"] label p {
        color: #ffffff !important;
        font-size: 17px !important;
        font-weight: 700 !important;
    }

    /* Chữ mô tả dưới mỗi tiêu chí */
    .stCaption, .stCaption p {
        color: #dcdcdc !important;
        font-size: 13px !important;
    }

    /* Nút kéo */
    [data-testid="stSlider"] div[role="slider"] {
        background-color: #1DB954 !important;
        border: 3px solid #ffffff !important;
        box-shadow: 0 0 0 2px #1DB954 !important;
    }

    /* Số trên thanh kéo */
    [data-testid="stSlider"] [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }

    /* Ẩn footer Streamlit */
    footer { 
        visibility: hidden; 
    }

    #MainMenu { 
        visibility: hidden; 
    }

    /* Thanh slider nền */
    .stSlider [data-baseweb="slider"] > div {
        background-color: #3a3a3a !important;
    }

    /* Phần thanh đã chọn */
    .stSlider [data-baseweb="slider"] > div > div {
        background-color: #1DB954 !important;
    }

    /* Nút kéo slider */
    .stSlider [role="slider"] {
        background-color: #1DB954 !important;
        border: 3px solid #ffffff !important;
        box-shadow: 0 0 0 2px #1DB954 !important;
    }

    /* Số trên slider */
    .stSlider [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Section header cho form đánh giá */
    .section-header {
        background-color: #1a1a1a;
        border-left: 4px solid #1DB954;
        padding: 10px 16px;
        border-radius: 0 8px 8px 0;
        margin: 24px 0 16px 0;
    }

    .section-header p {
        color: #1DB954 !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        margin: 0 !important;
    }

    /* Tip box màu xám */
    .tip-box {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 14px;
    }

    .tip-box p {
        color: #b3b3b3 !important;
        font-size: 12px !important;
        margin: 0 !important;
    }

    /* Radio buttons */
    .stRadio > div {
        background-color: #1a1a1a;
        border-radius: 8px;
        padding: 8px 14px;
    }

    .stRadio label {
        color: #ffffff !important;
    }

    /* Select box */
    .stSelectbox > div > div {
        background-color: #2a2a2a !important;
        color: #ffffff !important;
        border-color: #535353 !important;
    }

    /* Text area */
    .stTextArea textarea {
        background-color: #2a2a2a;
        color: #ffffff !important;
        border-color: #535353;
    }

    /* Score display box */
    .score-display {
        background: linear-gradient(135deg, #1DB954 0%, #158a3e 100%);
        border-radius: 12px;
        padding: 16px 20px;
        margin: 12px 0;
        text-align: center;
    }

    .score-display p {
        color: #000000 !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }

    /* So sánh playlist box */
    .compare-box {
        background-color: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }

    .compare-box p {
        margin: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Load dữ liệu playlist ────────────────────────────────────────────────────
@st.cache_data
def load_playlists():
    with open("playlist.json", "r", encoding="utf-8") as f:
        return json.load(f)

playlists = load_playlists()
PLAYLIST_NAMES = list(playlists.keys())   # ["X", "Y", "Z"]
RESULTS_FILE = "results.csv"
COMPARISON_FILE = "comparison.csv"
MIN_SONGS = 10   # Số bài tối thiểu phải nghe trước khi chấm


# ── Khởi tạo session state ───────────────────────────────────────────────────
if "heard" not in st.session_state:
    st.session_state.heard = {name: set() for name in PLAYLIST_NAMES}
if "submitted" not in st.session_state:
    st.session_state.submitted = {name: False for name in PLAYLIST_NAMES}
if "evaluator" not in st.session_state:
    st.session_state.evaluator = ""
if "comparison_submitted" not in st.session_state:
    st.session_state.comparison_submitted = False


# ── Hàm tính điểm theo form PDF ─────────────────────────────────────────────
def calculate_scores(answers: dict) -> dict:
    """Tính điểm theo công thức trong form đánh giá PDF."""
    # Diversity Score = TB(Câu 1 + Câu 2) + Serendipity bonus
    serendipity_bonus = 0.5 if answers.get("q3_serendipity") == "Có" else 0
    diversity_score = (answers["q1_coverage"] + answers["q2_ild"]) / 2 + serendipity_bonus

    # Coherence Score = TB(Câu 4 + Câu 5) + Outlier penalty
    outlier_penalty = -1 if answers.get("q6_outlier") == "Có" else 0
    coherence_score = (answers["q4_transition"] + answers["q5_tonal"]) / 2 + outlier_penalty

    # Balance Score = Câu 7
    balance_score = answers["q7_dcb"]

    # Satisfaction = Câu 8
    satisfaction_score = answers["q8_satisfaction"]

    # Final Score = (Diversity + Coherence + Balance + Satisfaction) / 4
    final_score = (diversity_score + coherence_score + balance_score + satisfaction_score) / 4

    return {
        "diversity_score": round(diversity_score, 2),
        "coherence_score": round(coherence_score, 2),
        "balance_score": round(balance_score, 2),
        "satisfaction_score": round(satisfaction_score, 2),
        "final_score": round(final_score, 2),
    }


# ── Hàm lưu kết quả chi tiết CSV ────────────────────────────────────────────
def save_result_detailed(evaluator, playlist_name, answers: dict, scores: dict):
    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "evaluator": evaluator,
        "playlist": playlist_name,
        # Raw answers
        "q1_coverage": answers["q1_coverage"],
        "q2_ild": answers["q2_ild"],
        "q3_serendipity": answers["q3_serendipity"],
        "q4_transition": answers["q4_transition"],
        "q5_tonal": answers["q5_tonal"],
        "q6_outlier": answers["q6_outlier"],
        "q6_outlier_song": answers.get("q6_outlier_song", ""),
        "q7_dcb": answers["q7_dcb"],
        "q8_satisfaction": answers["q8_satisfaction"],
        # Calculated scores
        "diversity_score": scores["diversity_score"],
        "coherence_score": scores["coherence_score"],
        "balance_score": scores["balance_score"],
        "satisfaction_score": scores["satisfaction_score"],
        "final_score": scores["final_score"],
    }
    if os.path.exists(RESULTS_FILE):
        df = pd.read_csv(RESULTS_FILE)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])
    df.to_csv(RESULTS_FILE, index=False)


# ── Hàm lưu so sánh 3 playlist ──────────────────────────────────────────────
def save_comparison(evaluator, comp_answers: dict):
    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "evaluator": evaluator,
        "q9_most_diverse": comp_answers["q9_most_diverse"],
        "q10_most_coherent": comp_answers["q10_most_coherent"],
        "q11_preferred": comp_answers["q11_preferred"],
        "q12_reason": comp_answers.get("q12_reason", ""),
    }
    if os.path.exists(COMPARISON_FILE):
        df = pd.read_csv(COMPARISON_FILE)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])
    df.to_csv(COMPARISON_FILE, index=False)


# ── Hàm nhúng YouTube player ─────────────────────────────────────────────────
def embed_youtube(link, height=220):
    if not link or "example" in link:
        st.info("🎵 Link nhạc chưa có — thay link thật vào playlist.json")
        return

    video_id = ""

    if "watch?v=" in link:
        video_id = link.split("watch?v=")[-1].split("&")[0]
    elif "youtu.be/" in link:
        video_id = link.split("youtu.be/")[-1].split("?")[0]
    elif "embed/" in link:
        video_id = link.split("embed/")[-1].split("?")[0]

    if not video_id:
        st.warning("Link YouTube chưa đúng định dạng.")
        return

    embed_url = f"https://www.youtube.com/embed/{video_id}"

    st.markdown(
        f"""
        <iframe 
            width="100%" 
            height="{height}" 
            src="{embed_url}" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
        </iframe>
        """,
        unsafe_allow_html=True
    )


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("## 🎵 Đánh giá Playlist — Blind Test")
st.markdown("<p style='color:#b3b3b3;margin-top:-12px'>Nghe ít nhất 10 bài mỗi playlist rồi chấm điểm chi tiết.</p>",
            unsafe_allow_html=True)

st.markdown("---")

# ── Nhập tên người đánh giá ───────────────────────────────────────────────────
evaluator_input = st.text_input("Tên người đánh giá", value=st.session_state.evaluator,
                                 placeholder="Ví dụ: Nguyễn Văn A")
st.session_state.evaluator = evaluator_input

if not evaluator_input.strip():
    st.warning("⚠️ Nhập tên trước khi bắt đầu nghe.")
    st.stop()

st.markdown("---")

# ── Tabs 3 Playlist ───────────────────────────────────────────────────────────
tabs = st.tabs([f"Playlist {name}" for name in PLAYLIST_NAMES])

for idx, (tab, pname) in enumerate(zip(tabs, PLAYLIST_NAMES)):
    with tab:
        songs = playlists[pname]
        heard_set = st.session_state.heard[pname]
        already_submitted = st.session_state.submitted[pname]

        # Tiến độ nghe
        progress = len(heard_set) / MIN_SONGS
        st.progress(min(progress, 1.0), text=f"Đã nghe: {len(heard_set)}/{MIN_SONGS} bài")

        # ── Danh sách bài hát ─────────────────────────────────────────────
        st.markdown("#### Danh sách bài hát")

        player_key = f"playing_{pname}"

        for i, song in enumerate(songs):
            heard_mark = "✅" if i in heard_set else f"{i + 1}."

            col1, col2 = st.columns([0.08, 0.92])

            with col1:
                st.markdown(
                    f"<p style='color:#b3b3b3;margin-top:8px'>{heard_mark}</p>",
                    unsafe_allow_html=True
                )

            with col2:
                if st.button(
                        f"{song['title']} — {song['artist']}",
                        key=f"song_{pname}_{i}",
                        use_container_width=True
                ):
                    st.session_state[player_key] = i
                    heard_set.add(i)
                    st.session_state.heard[pname] = heard_set
                    st.rerun()

            # Hiện video ngay dưới bài đang được chọn
            if st.session_state.get(player_key) == i:
                st.markdown(
                    f"""
                    <div class='now-playing-card'>
                        <p style='color:#1DB954;font-size:12px;margin:0'>Đang phát</p>
                        <p style='font-size:16px;font-weight:600;margin:4px 0'>{song['title']}</p>
                        <p style='color:#b3b3b3;font-size:13px;margin:0'>{song['artist']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                embed_youtube(song.get("link", ""), height=220)
        st.markdown("---")

        # ── Form đánh giá chi tiết ────────────────────────────────────────
        can_score = len(heard_set) >= MIN_SONGS

        if already_submitted:
            st.success(f"✅ Đã lưu điểm Playlist {pname}!")
        else:
            if not can_score:
                st.markdown(
                    f"<p style='color:#b3b3b3;font-size:13px'>"
                    f"🔒 Cần nghe thêm <b>{MIN_SONGS - len(heard_set)} bài</b> để mở khóa chấm điểm.</p>",
                    unsafe_allow_html=True)

            with st.container():
                # Thang điểm tổng quan
               st.markdown("""
                <p>📋 Bảng đánh giá chi tiết — Playlist </p>
                <div style="
                    background-color:#1DB954;
                    border-left:5px solid #000000;
                    padding:14px 18px;
                    border-radius:8px;
                    margin-top:8px;
                    margin-bottom:18px;
                ">
                    <p style="color:#000000 !important; font-size:15px; line-height:1.6; margin:0; font-weight:600;">
                        Vui lòng nghe toàn bộ các bài hát trong playlist trước khi đánh giá. 
                        Hãy chấm điểm dựa trên trải nghiệm tổng thể của playlist theo các tiêu chí được mô tả 
                        như độ đa dạng, độ mượt mà, cảm giác khám phá và mức độ hài lòng, 
                        thay vì dựa trên mức độ yêu thích cá nhân đối với một bài hát, nghệ sĩ hoặc thể loại nhạc cụ thể.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # ════════════════════════════════════════════════════
                # PHẦN 1 — Sự đa dạng
                # ════════════════════════════════════════════════════
                st.markdown("""
                <div class="section-header">
                    <p>🎨 PHẦN 1 — Sự đa dạng</p>
                </div>
                """, unsafe_allow_html=True)

                # Câu 1 — Coverage
                q1 = st.slider(
                    "Câu 1 — Các bài trong playlist có khác nhau không (nhịp điệu, cảm xúc, phong cách...)?",
                    min_value=1, max_value=5, value=3, step=1,
                    key=f"q1_{pname}", disabled=not can_score
                )
                st.caption("1 = Toàn bài na ná nhau  |  2 = Hầu hết giống nhau  |  3 = Có đa dạng nhưng chưa rõ  |  4 = Khá đa dạng  |  5 = Rất đa dạng, mỗi bài một màu sắc")

                st.markdown("<br>", unsafe_allow_html=True)

                # Câu 2 — ILD
                q2 = st.slider(
                    "Câu 2 — Khi chuyển từ bài này sang bài khác, bạn có cảm nhận được sự thay đổi không?",
                    min_value=1, max_value=5, value=3, step=1,
                    key=f"q2_{pname}", disabled=not can_score
                )
                st.caption("1 = Không, nghe đều đều  |  2 = Gần như không thay đổi  |  3 = Đôi chỗ có thay đổi  |  4 = Khá rõ  |  5 = Rất rõ, mỗi lần chuyển bài là cảm giác mới")

                st.markdown("<br>", unsafe_allow_html=True)

                # Câu 3 — Serendipity (Yes/No)
                q3 = st.radio(
                    "Câu 3 — Có bài nào khiến bạn bất ngờ thích không — kiểu nghe xong nghĩ 'ừ hay đấy, không ngờ'?",
                    options=["Không", "Có"],
                    horizontal=True,
                    key=f"q3_{pname}",
                    disabled=not can_score
                )

                # ════════════════════════════════════════════════════
                # PHẦN 2 — Độ mượt mà
                # ════════════════════════════════════════════════════
                st.markdown("""
                <div class="section-header">
                    <p>🔗 PHẦN 2 — Độ mượt mà</p>
                </div>
                """, unsafe_allow_html=True)

                # Câu 4 — Transition Smoothness
                q4 = st.slider(
                    "Câu 4 — Các bài chuyển tiếp nhau có tự nhiên không, hay bạn bị cảm giác hụt hẫng, gián đoạn?",
                    min_value=1, max_value=5, value=3, step=1,
                    key=f"q4_{pname}", disabled=not can_score
                )
                st.caption("1 = Chuyển bài rất cụt, liên tục hụt hẫng  |  2 = Nhiều chỗ khó chịu  |  3 = Đa số ổn, vài chỗ hơi cứng  |  4 = Hầu hết tự nhiên  |  5 = Rất mượt, liền mạch từ đầu đến cuối")

                st.markdown("<br>", unsafe_allow_html=True)

                # Câu 5 — Tonal Consistency
                q5 = st.slider(
                    "Câu 5 — Nhìn chung, các bài có cảm giác 'thuộc về nhau' không — hay nghe như bật random?",
                    min_value=1, max_value=5, value=3, step=1,
                    key=f"q5_{pname}", disabled=not can_score
                )
                st.caption("1 = Nghe như bật random hoàn toàn  |  2 = Rời rạc  |  3 = Tạm ổn, có liên kết nhưng chưa chặt  |  4 = Khá gắn kết  |  5 = Rất gắn kết, có chủ đích")

                st.markdown("<br>", unsafe_allow_html=True)

                # Câu 6 — Outlier Detection
                q6 = st.radio(
                    "Câu 6 — Có bài nào bạn nghĩ 'sao bài này lại ở đây?' — cảm giác nó không hợp với phần còn lại?",
                    options=["Không có bài nào như vậy", "Có"],
                    horizontal=True,
                    key=f"q6_{pname}",
                    disabled=not can_score
                )
                q6_song = ""
                if q6 == "Có" and can_score:
                    q6_song = st.text_input(
                        "Bài số / tên bài bị lạc đề:",
                        placeholder="Ví dụ: Bài số 3 — Tên bài",
                        key=f"q6_song_{pname}"
                    )

                # ════════════════════════════════════════════════════
                # PHẦN 3 — Cảm nhận tổng thể
                # ════════════════════════════════════════════════════
                st.markdown("""
                <div class="section-header">
                    <p>⭐ PHẦN 3 — Cảm nhận tổng thể</p>
                </div>
                """, unsafe_allow_html=True)

                # Câu 7 — DCB
                q7 = st.slider(
                    "Câu 7 — Playlist này có vừa đa dạng vừa mượt mà không — hay bị lệch về một phía?",
                    min_value=1, max_value=5, value=3, step=1,
                    key=f"q7_{pname}", disabled=not can_score
                )
                st.caption("1 = Hoàn toàn không cân bằng (quá nhàm hoặc quá lộn xộn)  |  2 = Hơi lệch nhiều  |  3 = Tạm được  |  4 = Khá cân bằng  |  5 = Rất cân bằng, đa dạng mà vẫn mượt")

                st.markdown("<br>", unsafe_allow_html=True)

                # Câu 8 — Overall Satisfaction
                q8 = st.slider(
                    "Câu 8 — Nếu playlist này tự phát trên Spotify, bạn có để yên cho nó chạy tiếp không?",
                    min_value=1, max_value=5, value=3, step=1,
                    key=f"q8_{pname}", disabled=not can_score
                )
                st.caption("1 = Tôi sẽ tắt hoặc chuyển ngay  |  2 = Nghe thêm 1–2 bài rồi chuyển  |  3 = Nghe tiếp được nhưng không hào hứng  |  4 = Khá muốn nghe tiếp  |  5 = Rất muốn, sẽ để nó chạy")

                # ── Hiển thị điểm dự kiến ─────────────────────────────────
                if can_score:
                    st.markdown("<br>", unsafe_allow_html=True)
                    answers_preview = {
                        "q1_coverage": q1, "q2_ild": q2, "q3_serendipity": q3,
                        "q4_transition": q4, "q5_tonal": q5, "q6_outlier": "Có" if q6 == "Có" else "Không",
                        "q6_outlier_song": q6_song, "q7_dcb": q7, "q8_satisfaction": q8,
                    }
                    scores_preview = calculate_scores(answers_preview)

                    col_d, col_c, col_b, col_s, col_f = st.columns(5)
                    with col_d:
                        st.markdown(f"""<div class="score-display">
                            <p style="font-size:11px">Diversity</p>
                            <p style="font-size:22px">{scores_preview['diversity_score']}</p>
                        </div>""", unsafe_allow_html=True)
                    with col_c:
                        st.markdown(f"""<div class="score-display">
                            <p style="font-size:11px">Coherence</p>
                            <p style="font-size:22px">{scores_preview['coherence_score']}</p>
                        </div>""", unsafe_allow_html=True)
                    with col_b:
                        st.markdown(f"""<div class="score-display">
                            <p style="font-size:11px">Balance</p>
                            <p style="font-size:22px">{scores_preview['balance_score']}</p>
                        </div>""", unsafe_allow_html=True)
                    with col_s:
                        st.markdown(f"""<div class="score-display">
                            <p style="font-size:11px">Satisfaction</p>
                            <p style="font-size:22px">{scores_preview['satisfaction_score']}</p>
                        </div>""", unsafe_allow_html=True)
                    with col_f:
                        st.markdown(f"""<div class="score-display" style="background:linear-gradient(135deg,#ffffff 0%,#cccccc 100%)">
                            <p style="font-size:11px;color:#000">Final</p>
                            <p style="font-size:22px;color:#000">{scores_preview['final_score']}</p>
                        </div>""", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button(f"💾 Lưu điểm Playlist {pname}", key=f"submit_{pname}"):
                        save_result_detailed(
                            evaluator=st.session_state.evaluator,
                            playlist_name=pname,
                            answers=answers_preview,
                            scores=scores_preview,
                        )
                        st.session_state.submitted[pname] = True
                        st.rerun()


# ── Phần so sánh 3 playlist (mở sau khi nghe cả 3) ───────────────────────────
all_submitted = all(st.session_state.submitted[n] for n in PLAYLIST_NAMES)

st.markdown("---")
st.markdown("## 🔀 Phần 4 — So sánh 3 Playlist")

if not all_submitted:
    remaining = [n for n in PLAYLIST_NAMES if not st.session_state.submitted[n]]
    st.markdown(
        f"<p style='color:#b3b3b3;font-size:13px'>🔒 Hoàn thành đánh giá Playlist {', '.join(remaining)} để mở phần so sánh.</p>",
        unsafe_allow_html=True
    )
else:
    if st.session_state.comparison_submitted:
        st.success("✅ Đã lưu phần so sánh! Cảm ơn bạn đã đánh giá.")
    else:
        st.markdown("<p style='color:#b3b3b3;font-size:13px'>Chỉ điền sau khi nghe xong cả 3 playlist.</p>",
                    unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header">
            <p>🏆 So sánh tổng thể</p>
        </div>
        """, unsafe_allow_html=True)

        # Câu 9 — Diversity tổng thể
        st.caption("Câu 9 — Playlist nào bạn thấy có nhiều bài đa dạng nhất?")
        q9 = st.radio(
            "Diversity tổng thể",
            options=[f"Playlist {n}" for n in PLAYLIST_NAMES],
            horizontal=True,
            key="q9_compare",
            label_visibility="collapsed"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Câu 10 — Coherence tổng thể
        st.caption("Câu 10 — Playlist nào bạn thấy nghe mượt mà, liền mạch nhất?")
        q10 = st.radio(
            "Coherence tổng thể",
            options=[f"Playlist {n}" for n in PLAYLIST_NAMES],
            horizontal=True,
            key="q10_compare",
            label_visibility="collapsed"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Câu 11 — Overall Preference
        st.caption("Câu 11 — Nếu chỉ chọn một, bạn muốn nghe lại playlist nào nhất?")
        q11 = st.radio(
            "Overall Preference",
            options=[f"Playlist {n}" for n in PLAYLIST_NAMES],
            horizontal=True,
            key="q11_compare",
            label_visibility="collapsed"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Câu 12 — Qualitative
        st.caption("Câu 12 — Lý do bạn chọn playlist đó? (Không bắt buộc)")
        q12 = st.text_area(
            "Lý do",
            placeholder="Ví dụ: Playlist X đa dạng nhưng vẫn mượt, không bị lộn xộn...",
            key="q12_compare",
            label_visibility="collapsed"
        )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Lưu so sánh", key="submit_compare"):
            save_comparison(
                evaluator=st.session_state.evaluator,
                comp_answers={
                    "q9_most_diverse": q9,
                    "q10_most_coherent": q10,
                    "q11_preferred": q11,
                    "q12_reason": q12,
                }
            )
            st.session_state.comparison_submitted = True
            st.rerun()


# ── Bảng kết quả tổng hợp ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown("## 📊 Kết quả tổng hợp")

if os.path.exists(RESULTS_FILE):
    df = pd.read_csv(RESULTS_FILE)
    if not df.empty:
        # Bảng tóm tắt điểm — chỉ dùng các cột thực sự tồn tại trong file
        score_cols_new = ["diversity_score", "coherence_score", "balance_score", "satisfaction_score", "final_score"]
        score_cols_old = ["coherence", "serendipity", "diversity", "overall_satisfaction", "average"]

        available_score_cols = [c for c in score_cols_new if c in df.columns]
        if not available_score_cols:
            # Fallback: file CSV cũ (bản app trước) — dùng cột cũ
            available_score_cols = [c for c in score_cols_old if c in df.columns]

        if available_score_cols and "playlist" in df.columns:
            summary = df.groupby("playlist")[available_score_cols].agg(["mean", "std"]).round(2)
            st.markdown("#### Điểm trung bình theo Playlist")
            st.dataframe(summary, use_container_width=True)
        else:
            st.warning("⚠️ File results.csv không có cột điểm hợp lệ. Hãy xóa file cũ và chạy lại.")

        # Bảng tất cả điểm
        st.markdown("#### Tất cả điểm đã ghi")
        st.dataframe(df, use_container_width=True)

        # Nút tải CSV
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Tải results.csv",
            data=csv_data,
            file_name="results.csv",
            mime="text/csv"
        )
    else:
        st.info("Chưa có kết quả nào được lưu.")
else:
    st.info("Chưa có kết quả nào — hãy hoàn thành ít nhất 1 playlist.")

# Bảng so sánh
if os.path.exists(COMPARISON_FILE):
    df_comp = pd.read_csv(COMPARISON_FILE)
    if not df_comp.empty:
        st.markdown("#### So sánh tổng thể từ người đánh giá")
        st.dataframe(df_comp, use_container_width=True)

        csv_comp = df_comp.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Tải comparison.csv",
            data=csv_comp,
            file_name="comparison.csv",
            mime="text/csv"
        )
