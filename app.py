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
MIN_SONGS = 10   # Số bài tối thiểu phải nghe trước khi chấm


# ── Khởi tạo session state ───────────────────────────────────────────────────
if "heard" not in st.session_state:
    st.session_state.heard = {name: set() for name in PLAYLIST_NAMES}
if "submitted" not in st.session_state:
    st.session_state.submitted = {name: False for name in PLAYLIST_NAMES}
if "evaluator" not in st.session_state:
    st.session_state.evaluator = ""


# ── Hàm lưu kết quả CSV ─────────────────────────────────────────────────────
def save_result(evaluator, playlist_name, coherence, serendipity, diversity, satisfaction):
    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "evaluator": evaluator,
        "playlist": playlist_name,
        "coherence": coherence,
        "serendipity": serendipity,
        "diversity": diversity,
        "overall_satisfaction": satisfaction,
        "average": round((coherence + serendipity + diversity + satisfaction) / 4, 2)
    }
    if os.path.exists(RESULTS_FILE):
        df = pd.read_csv(RESULTS_FILE)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])
    df.to_csv(RESULTS_FILE, index=False)


# ── Hàm nhúng YouTube player ─────────────────────────────────────────────────
def embed_youtube(link, height=80):
    video_id = link.split("v=")[-1].split("&")[0] if "v=" in link else ""
    if not video_id or "example" in video_id:
        st.info("🎵 Link nhạc chưa có — thay link thật vào playlist.json")
        return
    embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=0"
    st.markdown(
        f'<iframe width="100%" height="{height}" src="{embed_url}" '
        f'frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>',
        unsafe_allow_html=True
    )


# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("## 🎵 Đánh giá Playlist — Blind Test")
st.markdown("<p style='color:#b3b3b3;margin-top:-12px'>Nghe ít nhất 10 bài mỗi playlist rồi chấm điểm.</p>",
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
        selected_song = None

        for i, song in enumerate(songs):
            heard_mark = "✅" if i in heard_set else f"{i+1}."
            col1, col2 = st.columns([0.08, 0.92])
            with col1:
                st.markdown(f"<p style='color:#b3b3b3;margin-top:8px'>{heard_mark}</p>",
                            unsafe_allow_html=True)
            with col2:
                if st.button(f"{song['title']} — {song['artist']}",
                             key=f"song_{pname}_{i}",
                             use_container_width=True):
                    selected_song = i

        # ── Player ────────────────────────────────────────────────────────
        player_key = f"playing_{pname}"
        if selected_song is not None:
            st.session_state[player_key] = selected_song
            heard_set.add(selected_song)
            st.session_state.heard[pname] = heard_set

        if player_key in st.session_state:
            i = st.session_state[player_key]
            song = songs[i]
            st.markdown("---")
            st.markdown(f"<div class='now-playing-card'>"
                        f"<p style='color:#1DB954;font-size:12px;margin:0'>Đang phát</p>"
                        f"<p style='font-size:16px;font-weight:600;margin:4px 0'>{song['title']}</p>"
                        f"<p style='color:#b3b3b3;font-size:13px;margin:0'>{song['artist']}</p>"
                        f"</div>", unsafe_allow_html=True)
            embed_youtube(song["link"])

        st.markdown("---")

        # ── Rubric chấm điểm ──────────────────────────────────────────────
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
                # Hiển thị giải thích thang điểm
                st.markdown("""
                <div class="scale-box">
                    <p>Thang điểm đánh giá</p>
                    <p class="scale-detail">
                        1 = Rất thấp &nbsp; | &nbsp;
                        2 = Thấp &nbsp; | &nbsp;
                        3 = Trung bình &nbsp; | &nbsp;
                        4 = Tốt &nbsp; | &nbsp;
                        5 = Rất tốt
                    </p>
                </div>
                """, unsafe_allow_html=True)

                st.caption(
                    "1 = rất rời rạc | 2 = khá rời rạc | 3 = tạm ổn | 4 = khá liền mạch | 5 = rất liền mạch, chuyển bài tự nhiên")
                coherence = st.slider(
                    "Coherence — Độ mạch lạc của playlist",
                    min_value=1,
                    max_value=5,
                    value=3,
                    step=1,
                    key=f"coherence_{pname}",
                    disabled=not can_score
                )

                st.caption(
                    "1 = không có bài mới lạ | 2 = ít mới lạ | 3 = có vài bài mới | 4 = khá thú vị | 5 = mới lạ, bất ngờ nhưng vẫn hợp gu")
                serendipity = st.slider(
                    "Serendipity — Mức độ mới lạ nhưng vẫn phù hợp",
                    min_value=1,
                    max_value=5,
                    value=3,
                    step=1,
                    key=f"serendipity_{pname}",
                    disabled=not can_score
                )

                st.caption(
                    "1 = rất đơn điệu | 2 = hơi lặp lại | 3 = đa dạng vừa phải | 4 = khá đa dạng | 5 = rất đa dạng về thể loại, cảm xúc hoặc nghệ sĩ")
                diversity = st.slider(
                    "Diversity — Độ đa dạng của playlist",
                    min_value=1,
                    max_value=5,
                    value=3,
                    step=1,
                    key=f"diversity_{pname}",
                    disabled=not can_score
                )

                st.caption(
                    "1 = không hài lòng | 2 = hơi không hài lòng | 3 = bình thường | 4 = hài lòng | 5 = rất hài lòng và muốn nghe tiếp")
                satisfaction = st.slider(
                    "Overall Satisfaction — Mức độ hài lòng tổng thể",
                    min_value=1,
                    max_value=5,
                    value=3,
                    step=1,
                    key=f"satisfaction_{pname}",
                    disabled=not can_score
                )
                if can_score:
                    if st.button(f"💾 Lưu điểm Playlist {pname}", key=f"submit_{pname}"):
                        save_result(
                            evaluator=st.session_state.evaluator,
                            playlist_name=pname,
                            coherence=coherence,
                            serendipity=serendipity,
                            diversity=diversity,
                            satisfaction=satisfaction
                        )
                        st.session_state.submitted[pname] = True
                        st.rerun()


# ── Bảng kết quả tổng hợp ─────────────────────────────────────────────────────
st.markdown("---")
st.markdown("## 📊 Kết quả tổng hợp")

if os.path.exists(RESULTS_FILE):
    df = pd.read_csv(RESULTS_FILE)
    if not df.empty:
        summary = df.groupby("playlist")[
            ["coherence", "serendipity", "diversity", "overall_satisfaction", "average"]
        ].agg(["mean", "std"]).round(2)
        st.dataframe(summary, use_container_width=True)

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
