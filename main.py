
import streamlit as st
import random

# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------
st.set_page_config(
    page_title="MBTI 여행지 추천소 💗",
    page_icon="🧳",
    layout="centered"
)

# --------------------------------------------------
# CSS
# --------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;500;700&display=swap');

    .stApp {
        background: linear-gradient(180deg, #fff5fa 0%, #fffaff 50%, #f7f9ff 100%);
    }

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }

    .main-title {
        text-align: center;
        font-family: 'Jua', sans-serif;
        font-size: 42px;
        color: #ff7fa8;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #9b8f98;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .cute-box {
        background: rgba(255,255,255,0.85);
        border: 2px solid #ffd6e5;
        border-radius: 25px;
        padding: 25px;
        box-shadow: 0 8px 25px rgba(255, 160, 190, 0.12);
        margin-bottom: 20px;
    }

    .mbti-badge {
        display: inline-block;
        background: #ffe1ec;
        color: #ed6895;
        border-radius: 20px;
        padding: 7px 16px;
        font-weight: 700;
        font-size: 15px;
        margin-bottom: 10px;
    }

    .destination-card {
        background: white;
        border-radius: 25px;
        padding: 24px;
        margin: 15px 0;
        border: 1.5px solid #f4dce7;
        box-shadow: 0 6px 20px rgba(100, 70, 100, 0.08);
    }

    .destination-title {
        font-family: 'Jua', sans-serif;
        font-size: 25px;
        color: #59506b;
        margin-bottom: 8px;
    }

    .reason {
        color: #77717b;
        line-height: 1.7;
        font-size: 15px;
    }

    .tag {
        display: inline-block;
        background: #f4efff;
        color: #8a70b5;
        border-radius: 15px;
        padding: 5px 11px;
        margin: 3px;
        font-size: 12px;
    }

    .footer {
        text-align: center;
        color: #aaa0aa;
        font-size: 13px;
        margin-top: 35px;
        padding-bottom: 20px;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 20px;
        border: none;
        background: linear-gradient(90deg, #ff9fbd, #c7a8f9);
        color: white;
        font-size: 18px;
        font-weight: 700;
        padding: 12px;
        transition: 0.2s;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 15px rgba(210, 150, 200, 0.25);
    }

    .stSelectbox label {
        color: #665b68;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 여행지 데이터
# --------------------------------------------------
travel_data = {

    "INFP": {
        "nickname": "몽글몽글 감성 여행자 🌷",
        "description": "조용한 골목을 걷고 예쁜 카페에서 천천히 쉬는 여행을 좋아해요.",
        "places": [
            ("교토 🇯🇵", "고즈넉한 골목과 작은 찻집을 천천히 둘러보며 감성을 충전하기 좋아요.", ["감성", "카페", "산책"]),
            ("제주도 🇰🇷", "바다를 바라보며 여유롭게 걷고 자연 속에서 마음을 쉬게 하기 좋은 곳이에요.", ["자연", "힐링", "바다"]),
            ("프라하 🇨🇿", "동화 같은 건물과 골목길을 걸으며 나만의 여행 이야기를 만들기 좋아요.", ["동화", "사진", "산책"])
        ]
    },

    "INFJ": {
        "nickname": "조용한 여행 설계자 🌙",
        "description": "사람이 너무 붐비지 않으면서 의미 있는 장소를 좋아해요.",
        "places": [
            ("교토 🇯🇵", "역사와 문화가 살아 있는 공간에서 천천히 생각을 정리하기 좋아요.", ["문화", "역사", "힐링"]),
            ("스위스 🇨🇭", "웅장한 자연 속에서 복잡한 생각을 내려놓고 휴식하기 좋아요.", ["자연", "힐링", "풍경"]),
            ("경주 🇰🇷", "역사적인 장소를 둘러보며 조용하고 깊이 있는 여행을 즐길 수 있어요.", ["역사", "문화", "산책"])
        ]
    },

    "ENFP": {
        "nickname": "두근두근 모험 여행자 🎀",
        "description": "새로운 경험과 맛있는 음식, 재미있는 사람들을 만나는 걸 좋아해요.",
        "places": [
            ("방콕 🇹🇭", "맛있는 음식부터 야시장, 쇼핑까지 다양한 경험을 한 번에 즐길 수 있어요.", ["맛집", "쇼핑", "활동"]),
            ("오사카 🇯🇵", "먹거리와 볼거리가 많아서 즉흥적으로 돌아다니기 딱 좋아요.", ["먹방", "도시", "재미"]),
            ("부산 🇰🇷", "바다와 맛집, 카페, 액티비티까지 다양하게 즐길 수 있어요.", ["바다", "맛집", "카페"])
        ]
    },

    "ENFJ": {
        "nickname": "사람 좋아하는 여행 리더 💕",
        "description": "친구들과 함께 추억을 만들고 다양한 체험을 하는 여행이 잘 맞아요.",
        "places": [
            ("파리 🇫🇷", "친구들과 예쁜 장소를 구경하고 맛있는 음식을 먹으며 추억을 만들기 좋아요.", ["사진", "문화", "맛집"]),
            ("싱가포르 🇸🇬", "깔끔하고 다양한 볼거리 덕분에 함께 여행하기 편하고 즐거워요.", ["도시", "관광", "맛집"]),
            ("서울 🇰🇷", "카페부터 쇼핑, 전시, 맛집까지 친구들과 함께 할 일이 정말 많아요.", ["카페", "쇼핑", "전시"])
        ]
    },

    "INTP": {
        "nickname": "호기심 가득 탐구 여행자 🔬",
        "description": "평범한 관광보다 독특한 장소와 새로운 지식을 발견하는 걸 좋아해요.",
        "places": [
            ("도쿄 🇯🇵", "과학관, 전자상가, 독특한 문화 공간 등 호기심을 자극하는 곳이 많아요.", ["과학", "도시", "탐험"]),
            ("런던 🇬🇧", "박물관과 역사적인 장소를 돌아다니며 새로운 지식을 얻기 좋아요.", ["박물관", "역사", "문화"]),
            ("싱가포르 🇸🇬", "미래적인 도시와 과학·기술 관련 볼거리가 많아 탐구심을 자극해요.", ["과학", "미래", "도시"])
        ]
    },

    "INTJ": {
        "nickname": "완벽주의 여행 전략가 🖤",
        "description": "계획적으로 움직이면서도 남들과 다른 특별한 경험을 선호해요.",
        "places": [
            ("스위스 🇨🇭", "교통과 일정이 비교적 체계적이고 아름다운 자연을 효율적으로 둘러볼 수 있어요.", ["계획", "자연", "풍경"]),
            ("도쿄 🇯🇵", "효율적인 교통과 다양한 콘텐츠 덕분에 알찬 여행을 계획하기 좋아요.", ["도시", "효율", "문화"]),
            ("싱가포르 🇸🇬", "깔끔한 도시 환경과 체계적인 관광 인프라가 여행 계획과 잘 맞아요.", ["깔끔", "도시", "계획"])
        ]
    },

    "ENTP": {
        "nickname": "아이디어 폭발 여행자 ⚡",
        "description": "새로운 것, 특이한 것, 예상하지 못한 경험을 좋아해요.",
        "places": [
            ("도쿄 🇯🇵", "전통과 최신 문화가 섞여 있어서 새로운 아이디어를 얻기 좋아요.", ["트렌드", "문화", "탐험"]),
            ("뉴욕 🇺🇸", "다양한 문화와 사람, 독특한 장소가 모여 있어 지루할 틈이 없어요.", ["도시", "문화", "예술"]),
            ("베를린 🇩🇪", "개성 있는 예술과 독특한 문화가 살아 있어서 색다른 경험을 할 수 있어요.", ["예술", "문화", "자유"])
        ]
    },

    "ENTJ": {
        "nickname": "당당한 여행 CEO 👑",
        "description": "알찬 일정과 다양한 경험을 빠르게 즐기는 여행이 잘 맞아요.",
        "places": [
            ("뉴욕 🇺🇸", "도시의 에너지와 다양한 볼거리를 빠르게 경험하기 좋아요.", ["도시", "쇼핑", "문화"]),
            ("싱가포르 🇸🇬", "짧은 시간에도 다양한 명소를 효율적으로 돌아볼 수 있어요.", ["효율", "도시", "관광"]),
            ("도쿄 🇯🇵", "쇼핑, 음식, 문화, 관광까지 바쁜 일정을 꽉 채울 수 있어요.", ["쇼핑", "맛집", "도시"])
        ]
    },

    "ISFP": {
        "nickname": "말랑말랑 자유 여행자 🧸",
        "description": "정해진 일정에 얽매이기보다 예쁜 풍경과 맛있는 것을 따라 움직이는 걸 좋아해요.",
        "places": [
            ("제주도 🇰🇷", "예쁜 바다와 카페를 따라 자유롭게 돌아다니기 좋아요.", ["바다", "카페", "자유"]),
            ("다낭 🇻🇳", "따뜻한 날씨와 바다를 즐기면서 느긋하게 쉬기 좋아요.", ["휴양", "바다", "힐링"]),
            ("후쿠오카 🇯🇵", "맛있는 음식과 아기자기한 공간을 부담 없이 즐길 수 있어요.", ["맛집", "카페", "여유"])
        ]
    },

    "ISFJ": {
        "nickname": "포근포근 힐링 여행자 ☁️",
        "description": "편안하고 안전하면서도 예쁜 장소에서 여유롭게 쉬는 걸 좋아해요.",
        "places": [
            ("제주도 🇰🇷", "아름다운 자연 속에서 무리하지 않고 편안하게 여행하기 좋아요.", ["힐링", "자연", "바다"]),
            ("후쿠오카 🇯🇵", "맛있는 음식과 편안한 분위기를 함께 즐길 수 있어요.", ["맛집", "여유", "도시"]),
            ("경주 🇰🇷", "조용한 분위기 속에서 문화와 자연을 함께 즐길 수 있어요.", ["역사", "산책", "힐링"])
        ]
    },

    "ESFP": {
        "nickname": "반짝반짝 행복 여행자 ✨",
        "description": "맛있는 음식과 예쁜 사진, 신나는 활동을 모두 놓치고 싶지 않아요!",
        "places": [
            ("부산 🇰🇷", "바다, 맛집, 카페, 쇼핑까지 재미있는 요소가 가득해요.", ["바다", "맛집", "카페"]),
            ("오사카 🇯🇵", "맛있는 음식과 활기찬 분위기를 마음껏 즐길 수 있어요.", ["먹방", "쇼핑", "도시"]),
            ("방콕 🇹🇭", "야시장과 맛집, 쇼핑을 즐기며 신나는 여행을 할 수 있어요.", ["야시장", "맛집", "쇼핑"])
        ]
    },

    "ESFJ": {
        "nickname": "다정다감 추억 여행자 💗",
        "description": "친구나 가족과 함께 맛있는 것을 먹고 예쁜 곳에서 사진 찍는 걸 좋아해요.",
        "places": [
            ("파리 🇫🇷", "예쁜 풍경과 맛있는 음식으로 함께 추억을 만들기 좋아요.", ["사진", "맛집", "감성"]),
            ("부산 🇰🇷", "친구나 가족과 함께 즐길 수 있는 볼거리와 먹거리가 많아요.", ["가족", "맛집", "바다"]),
            ("후쿠오카 🇯🇵", "가까운 거리에서 맛집과 쇼핑을 편하게 즐길 수 있어요.", ["맛집", "쇼핑", "여행"])
        ]
    },

    "ISTP": {
        "nickname": "쿨한 액티비티 여행자 🏄",
        "description": "관광지만 구경하기보다 직접 움직이고 경험하는 걸 좋아해요.",
        "places": [
            ("다낭 🇻🇳", "바다와 다양한 액티비티를 부담 없이 즐길 수 있어요.", ["바다", "액티비티", "휴양"]),
            ("제주도 🇰🇷", "드라이브와 자연 속 활동을 자유롭게 즐기기 좋아요.", ["드라이브", "자연", "활동"]),
            ("퀸스타운 🇳🇿", "아름다운 자연 속에서 다양한 야외 활동을 즐길 수 있어요.", ["자연", "모험", "액티비티"])
        ]
    },

    "ISTJ": {
        "nickname": "차분한 계획 여행자 📚",
        "description": "꼼꼼하게 계획하고 편안하게 여행하는 것을 좋아해요.",
        "places": [
            ("교토 🇯🇵", "정돈된 분위기와 역사적인 장소를 차분하게 둘러보기 좋아요.", ["역사", "문화", "산책"]),
            ("스위스 🇨🇭", "아름다운 자연과 체계적인 여행 환경이 잘 어울려요.", ["자연", "계획", "풍경"]),
            ("경주 🇰🇷", "역사와 문화가 잘 보존되어 있어 차분하게 여행하기 좋아요.", ["역사", "문화", "힐링"])
        ]
    },

    "ESTP": {
        "nickname": "짜릿짜릿 액션 여행자 🔥",
        "description": "즉흥적인 재미와 새로운 경험을 좋아하는 에너지 넘치는 여행자예요.",
        "places": [
            ("방콕 🇹🇭", "맛집부터 야시장까지 하루를 꽉 채워 재미있게 즐길 수 있어요.", ["맛집", "야시장", "활동"]),
            ("부산 🇰🇷", "바다와 액티비티, 맛집을 모두 즐길 수 있어요.", ["바다", "활동", "맛집"]),
            ("싱가포르 🇸🇬", "도시 관광부터 다양한 체험까지 빠르게 즐기기 좋아요.", ["도시", "체험", "관광"])
        ]
    },

    "ESTJ": {
        "nickname": "똑부러진 여행 대장 🧳",
        "description": "알찬 일정과 확실한 목적지가 있는 여행을 좋아해요.",
        "places": [
            ("도쿄 🇯🇵", "볼거리와 쇼핑, 맛집이 많아 알찬 일정을 만들기 좋아요.", ["쇼핑", "맛집", "도시"]),
            ("싱가포르 🇸🇬", "주요 관광지를 효율적으로 둘러보기 좋은 여행지예요.", ["계획", "도시", "관광"]),
            ("서울 🇰🇷", "짧은 시간에도 다양한 명소와 맛집을 효율적으로 즐길 수 있어요.", ["쇼핑", "맛집", "문화"])
        ]
    }
}


# --------------------------------------------------
# 제목
# --------------------------------------------------
st.markdown(
    '<div class="main-title">🧳 MBTI 여행지 추천소 💗</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">나의 MBTI와 찰떡궁합인 여행지는 어디일까? 🌷</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# MBTI 선택
# --------------------------------------------------
st.markdown('<div class="cute-box">', unsafe_allow_html=True)

st.markdown("### 💌 먼저 MBTI를 골라주세요!")

mbti_list = list(travel_data.keys())

mbti = st.selectbox(
    "나의 MBTI",
    mbti_list,
    format_func=lambda x: f"{x}  ✨"
)

st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# 선택한 MBTI 정보
# --------------------------------------------------
info = travel_data[mbti]

st.markdown(
    f"""
    <div class="cute-box">
        <div class="mbti-badge">{mbti}</div>
        <h2 style="color:#62566d; margin-bottom:5px;">
            {info["nickname"]}
        </h2>
        <p style="color:#77717b; line-height:1.7;">
            {info["description"]}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# 추천 버튼
# --------------------------------------------------
if st.button("💗 나에게 딱 맞는 여행지 추천받기 ✨"):

    st.balloons()

    places = info["places"].copy()
    random.shuffle(places)

    st.markdown(
        f"""
        <div style="
            text-align:center;
            margin:25px 0 20px 0;
        ">
            <h2 style="
                font-family:'Jua', sans-serif;
                color:#ff82aa;
            ">
                🌸 {mbti}에게 추천하는 여행지 🌸
            </h2>
            <p style="color:#999;">
                당신의 여행 취향을 생각해서 골라봤어요!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    for i, (place, reason, tags) in enumerate(places, start=1):

        tag_html = "".join(
            f'<span class="tag">#{tag}</span>'
            for tag in tags
        )

        st.markdown(
            f"""
            <div class="destination-card">
                <div style="
                    color:#ff9ab9;
                    font-size:13px;
                    font-weight:700;
                ">
                    RECOMMEND {i}
                </div>

                <div class="destination-title">
                    {place}
                </div>

                <div style="margin-bottom:12px;">
                    {tag_html}
                </div>

                <div class="reason">
                    💌 {reason}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div style="
            text-align:center;
            background:#fff0f6;
            border-radius:20px;
            padding:18px;
            margin-top:25px;
            color:#9b7182;
        ">
            🌷 여행은 어디로 가느냐보다<br>
            <b>누구와 어떤 추억을 만드느냐</b>가 더 중요할지도 몰라요! 💕 
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown(
    """
    <div class="footer">
        made with 💗 for lovely travelers · MBTI Travel Finder
    </div>
    """,
    unsafe_allow_html=True
)
```
