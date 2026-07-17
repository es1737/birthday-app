import base64
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="수인수 생일 축하해", page_icon="🐵", layout="centered")

# ------------------------------------------------------------------
# 말풍선 문구
# ------------------------------------------------------------------
MESSAGES = [
    "안녕 수인수\n난 언순이얌",
    "오늘 너의 생일이구나!",
    "내가 선물을 줄게",
    "레츠끼끼~",
    "짜잔! 🎁",
    "선물은 바로... 나야 나!",
    "__CAKE__",  # 특수 마커: 케이크 촛불 끄기 
    "생일 축하해 수인수야~\n다음 생일도 같이 놀자 🎉",
]

CAKE_IDX = MESSAGES.index("__CAKE__")

# ------------------------------------------------------------------
# 문구별로 보여줄 이미지 설정
# key = MESSAGES 리스트의 인덱스, value = (파일명, 이미지 가로폭)
# ------------------------------------------------------------------
DEFAULT_IMAGE = ("끼끼언순이.png", 220)

IMAGE_OVERRIDES = {
    4: ("선물.png", 340),      # "내가 선물을 줄게" 문구일 때 크게 등장
    5: ("축하언순이.png", 340),  # "선물은 바로... 나야 나!" 문구일 때 크게 등장
}

if "msg_idx" not in st.session_state:
    st.session_state.msg_idx = 0
if "cake_done" not in st.session_state:
    st.session_state.cake_done = False


def next_message():
    st.session_state.msg_idx = (st.session_state.msg_idx + 1) % len(MESSAGES)
    # 케이크 단계를 벗어나면 촛불 상태 초기화 (한 바퀴 돌아 다시 케이크로 왔을 때 대비)
    if st.session_state.msg_idx != CAKE_IDX:
        st.session_state.cake_done = False


def blow_candle():
    st.session_state.cake_done = True


idx = st.session_state.msg_idx
is_cake_step = idx == CAKE_IDX

st.markdown(
    """
    <style>
    .stage {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 10px;
    }
    .bubble {
        position: relative;
        background: #ffffff;
        border: 3px solid #2b2b2b;
        border-radius: 24px;
        padding: 18px 24px;
        max-width: 340px;
        font-size: 18px;
        font-weight: 600;
        line-height: 1.5;
        text-align: center;
        color: #2b2b2b;
        box-shadow: 3px 3px 0px rgba(0,0,0,0.15);
    }
    .bubble:after {
        content: "";
        position: absolute;
        bottom: -18px;
        left: 50%;
        transform: translateX(-50%);
        border-width: 18px 12px 0 12px;
        border-style: solid;
        border-color: #2b2b2b transparent transparent transparent;
    }
    .bubble:before {
        content: "";
        position: absolute;
        bottom: -13px;
        left: 50%;
        transform: translateX(-50%);
        border-width: 15px 9px 0 9px;
        border-style: solid;
        border-color: #ffffff transparent transparent transparent;
        z-index: 1;
    }
    .monkey-img {
        margin-top: 12px;
        cursor: pointer;
        transition: transform 0.15s ease, width 0.2s ease;
    }
    .monkey-img:hover {
        transform: scale(1.05);
    }

    /* --- 케이크 & 촛불 --- */
    .cake-wrap {
        margin-top: 18px;
        text-align: center;
    }
    .candle-flame {
        font-size: 40px;
        display: inline-block;
        animation: flicker 1.1s infinite alternate;
    }
    @keyframes flicker {
        from { transform: translateY(0px) scale(1); }
        to   { transform: translateY(-2px) scale(1.08); }
    }
    .cake-emoji {
        font-size: 90px;
        line-height: 1;
    }
    .smoke {
        font-size: 28px;
        opacity: 0.6;
        animation: rise 1.6s ease-out infinite;
    }
    @keyframes rise {
        0%   { transform: translateY(0px); opacity: 0.6; }
        100% { transform: translateY(-20px); opacity: 0; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h2 style='text-align:center;'>🎂 생일을 축하합니다 🎂</h2>", unsafe_allow_html=True)

if is_cake_step:
    # ------------------------------------------------------------
    # 케이크 / 촛불 끄기 단계
    # ------------------------------------------------------------
    if not st.session_state.cake_done:
        bubble_text = "이제 소원을 빌고\n촛불을 꺼보자"
        candle_html = '<span class="candle-flame">🕯️</span>'
    else:
        bubble_text = "후우~ 잘했어!\n소원은 이루어질 거야"
        candle_html = '<span style="font-size:40px;">💨</span>'

    st.markdown(
        f"""
        <div class="stage">
            <div class="bubble">{bubble_text.replace(chr(10), '<br>')}</div>
            <div class="cake-wrap">
                <div>{candle_html}</div>
                <div class="cake-emoji">🎂</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.write("")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if not st.session_state.cake_done:
            st.button("후~ 촛불 끄기", on_click=blow_candle, use_container_width=True)
        else:
            st.balloons()
            st.button("다음", on_click=next_message, use_container_width=True)

else:
    # ------------------------------------------------------------
    # 일반 말풍선 + 캐릭터 이미지 단계
    # ------------------------------------------------------------
    current_text = MESSAGES[idx].replace("\n", "<br>")
    img_name, img_width = IMAGE_OVERRIDES.get(idx, DEFAULT_IMAGE)

    img_path = Path(__file__).parent / img_name
    img_base64 = base64.b64encode(img_path.read_bytes()).decode()

    st.markdown(
        f"""
        <div class="stage">
            <div class="bubble">{current_text}</div>
            <img class="monkey-img" style="width:{img_width}px;" src="data:image/png;base64,{img_base64}">
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.write("")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.button("다음", on_click=next_message, use_container_width=True)
