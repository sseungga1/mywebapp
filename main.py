
import streamlit as st
import random

# --------------------------------------------------
# 페이지 설정
# --------------------------------------------------
st.set_page_config(
    page_title="별자리 여행지 추천소 💫",
    page_icon="🌙",
    layout="centered"
)

# --------------------------------------------------
# CSS
# --------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;500;700&display=swap');

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #ffe4f0 0, transparent 25%),
        radial-gradient(circle at 90% 20%, #e9ddff 0, transparent 25%),
        linear-gradient(180deg, #fff7fb 0%, #faf8ff 100%);
}

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

/* 메인 제목 */
.main-title {
    text-align: center;
    font-family: 'Jua', sans-serif;
    font-size: 44px;
    color: #ef82aa;
    margin-top: 15px;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    color: #9b8fa0;
    font-size: 16px;
    margin-bottom: 30px;
}

/* 귀여운 박스 */
.cute-box {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid #f7d8e7;
    border-radius: 28px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(190, 130, 170, 0.10);
}

/* 별자리 뱃지 */
.zodiac-badge {
    display: inline-block;
    background: #f3e8ff;
    color: #8b70ad;
    border-radius: 20px;
    padding: 7px 16px;
    font-weight: 700;
    font-size: 14px;
}

/* 결과 카드 */
.destination-card {
    background: white;
    border: 1.5px solid #f1dfe9;
    border-radius: 26px;
    padding: 24px;
    margin: 16px 0;
    box-shadow: 0 7px 22px rgba(100, 80, 110, 0.08);
}

.destination-title {
    font-family: 'Jua', sans-serif;
    color: #62576e;
    font-size: 27px;
    margin-top: 5px;
    margin-bottom: 10px;
}

.reason {
    color: #77717c;
    font-size: 15px;
    line-height: 1.8;
}

.tag {
    display: inline-block;
    background: #fff0f6;
    color: #d5799d;
    border-radius: 15px;
    padding: 5px 11px;
    margin: 3px;
    font-size: 12px;
}

/* 추천 버튼 */
div.stButton > button {
    width: 100%;
    border: none;
    border-radius: 22px;
    background: linear-gradient(90deg, #ff9fbd, #bfa5f5);
    color: white;
    font-size: 18px;
    font-weight: 700;
    padding: 13px;
}

div.stButton > button:hover {
    box-shadow: 0 8px 20px rgba(190, 140, 200, 0.25);
    transform: translateY(-2px);
}

/* Footer */
.footer {
    text-align: center;
    color: #aaa1ad;
    font-size: 13px;
    margin-top: 35px;
    padding-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 별자리 데이터
# --------------------------------------------------
zodiac_data = {

    "♈ 양자리 (3/21 ~ 4/19)": {
        "name": "양자리",
        "nickname": "두근두근 모험가 🔥",
        "description": "새로운 경험과 짜릿한 활동을 좋아하는 에너지 넘치는 여행자예요!",
        "places": [
            ("부산 🇰🇷", "바다부터 액티비티까지 다양한 활동을 즐길 수 있어서 양자리의 에너지와 잘 어울려요.", ["액티비티", "바다", "맛집"]),
            ("방콕 🇹🇭", "야시장과 맛집, 다양한 체험까지 지루할 틈 없이 신나는 여행을 즐길 수 있어요.", ["모험", "야시장", "먹방"]),
            ("퀸스타운 🇳🇿", "아름다운 자연 속에서 다양한 야외 활동을 즐길 수 있는 모험 여행지예요.", ["자연", "모험", "액티비티"])
        ]
    },

    "♉ 황소자리 (4/20 ~ 5/20)": {
        "name": "황소자리",
        "nickname": "느긋한 행복 여행자 🍰",
        "description": "맛있는 음식과 편안한 분위기, 아름다운 공간에서 천천히 쉬는 걸 좋아해요.",
        "places": [
            ("후쿠오카 🇯🇵", "맛있는 음식과 아기자기한 카페를 여유롭게 즐기기 좋아요.", ["맛집", "카페", "여유"]),
            ("제주도 🇰🇷", "아름다운 자연과 맛있는 음식, 편안한 숙소에서 느긋하게 쉬기 좋아요.", ["힐링", "자연", "맛집"]),
            ("파리 🇫🇷", "예쁜 카페에서 디저트를 즐기고 아름다운 거리를 천천히 걷기 좋아요.", ["디저트", "카페", "감성"])
        ]
    },

    "♊ 쌍둥이자리 (5/21 ~ 6/20)": {
        "name": "쌍둥이자리",
        "nickname": "호기심 가득 탐험가 💬",
        "description": "새로운 장소와 재미있는 이야기를 찾아다니는 것을 좋아해요.",
        "places": [
            ("도쿄 🇯🇵", "전통문화부터 최신 유행까지 다양한 모습을 한 번에 경험할 수 있어요.", ["트렌드", "문화", "도시"]),
            ("런던 🇬🇧", "박물관과 거리, 쇼핑 등 다양한 콘텐츠를 골고루 즐길 수 있어요.", ["문화", "박물관", "쇼핑"]),
            ("서울 🇰🇷", "카페, 전시, 쇼핑, 맛집 등 새로운 것을 발견할 곳이 정말 많아요.", ["카페", "전시", "쇼핑"])
        ]
    },

    "♋ 게자리 (6/21 ~ 7/22)": {
        "name": "게자리",
        "nickname": "포근포근 힐링 여행자 🐚",
        "description": "편안하고 따뜻한 분위기에서 소중한 사람들과 추억을 만드는 여행을 좋아해요.",
        "places": [
            ("제주도 🇰🇷", "잔잔한 바다와 자연 속에서 가족이나 친구와 편안한 시간을 보내기 좋아요.", ["가족", "힐링", "바다"]),
            ("경주 🇰🇷", "조용한 분위기에서 역사적인 장소를 둘러보며 여유를 즐길 수 있어요.", ["역사", "산책", "힐링"]),
            ("다낭 🇻🇳", "따뜻한 날씨와 바다를 즐기며 느긋하게 쉬기 좋은 곳이에요.", ["휴양", "바다", "여유"])
        ]
    },

    "♌ 사자자리 (7/23 ~ 8/22)": {
        "name": "사자자리",
        "nickname": "반짝반짝 주인공 여행자 👑",
        "description": "멋진 장소에서 특별한 추억을 만들고 예쁜 사진을 남기는 걸 좋아해요.",
        "places": [
            ("파리 🇫🇷", "아름다운 랜드마크와 감성적인 거리가 많아 특별한 여행 사진을 남기기 좋아요.", ["사진", "랜드마크", "감성"]),
            ("뉴욕 🇺🇸", "화려하고 에너지 넘치는 도시에서 주인공처럼 여행을 즐길 수 있어요.", ["도시", "쇼핑", "문화"]),
            ("두바이 🇦🇪", "화려한 건축물과 특별한 경험으로 색다른 여행 추억을 만들 수 있어요.", ["럭셔리", "건축", "사진"])
        ]
    },

    "♍ 처녀자리 (8/23 ~ 9/22)": {
        "name": "처녀자리",
        "nickname": "꼼꼼한 계획 여행자 📖",
        "description": "깔끔하고 체계적인 일정 속에서 알차게 여행하는 것을 좋아해요.",
        "places": [
            ("싱가포르 🇸🇬", "깔끔한 도시 환경과 체계적인 교통 덕분에 계획적인 여행을 하기 좋아요.", ["깔끔", "계획", "도시"]),
            ("교토 🇯🇵", "차분하고 정돈된 분위기 속에서 역사와 문화를 천천히 둘러볼 수 있어요.", ["문화", "역사", "산책"]),
            ("스위스 🇨🇭", "아름다운 자연과 편리한 교통 환경을 함께 즐길 수 있어요.", ["자연", "계획", "풍경"])
        ]
    },

    "♎ 천칭자리 (9/23 ~ 10/22)": {
        "name": "천칭자리",
        "nickname": "예쁜 것 가득 감성 여행자 🎀",
        "description": "예쁜 공간과 맛있는 음식, 아름다운 풍경을 사랑하는 여행자예요.",
        "places": [
            ("파리 🇫🇷", "예쁜 거리와 카페, 건축물까지 감성을 가득 채울 수 있어요.", ["감성", "카페", "사진"]),
            ("교토 🇯🇵", "전통적인 아름다움과 조용한 골목의 분위기를 즐기기 좋아요.", ["전통", "감성", "산책"]),
            ("프라하 🇨🇿", "동화 속에 들어온 듯한 아름다운 건축물과 풍경을 만날 수 있어요.", ["동화", "사진", "풍경"])
        ]
    },

    "♏ 전갈자리 (10/23 ~ 11/21)": {
        "name": "전갈자리",
        "nickname": "신비로운 탐험가 🌙",
        "description": "남들이 잘 모르는 특별한 장소와 깊이 있는 경험을 좋아해요.",
        "places": [
            ("이스탄불 🇹🇷", "동양과 서양의 문화가 만나는 독특한 분위기와 역사적인 공간을 경험할 수 있어요.", ["역사", "문화", "탐험"]),
            ("교토 🇯🇵", "오래된 전통과 고즈넉한 공간에서 깊이 있는 여행을 즐길 수 있어요.", ["전통", "역사", "감성"]),
            ("아이슬란드 🇮🇸", "신비로운 자연 풍경을 보며 평소와 다른 특별한 경험을 할 수 있어요.", ["자연", "신비", "풍경"])
        ]
    },

    "♐ 사수자리 (11/22 ~ 12/21)": {
        "name": "사수자리",
        "nickname": "자유로운 세계 여행자 🌎",
        "description": "자유롭게 돌아다니면서 새로운 문화와 자연을 경험하는 것을 좋아해요.",
        "places": [
            ("뉴질랜드 🇳🇿", "넓은 자연 속에서 자유롭게 여행하며 다양한 모험을 즐길 수 있어요.", ["자연", "자유", "모험"]),
            ("호주 🇦🇺", "도시와 자연, 해변까지 다양한 경험을 한 번에 할 수 있어요.", ["여행", "자연", "바다"]),
            ("태국 🇹🇭", "맛있는 음식과 아름다운 자연, 새로운 문화를 자유롭게 경험할 수 있어요.", ["문화", "맛집", "모험"])
        ]
    },

    "♑ 염소자리 (12/22 ~ 1/19)": {
        "name": "염소자리",
        "nickname": "야무진 알찬 여행자 🧳",
        "description": "계획을 세우고 목표한 곳을 하나씩 정복하는 여행을 좋아해요.",
        "places": [
            ("도쿄 🇯🇵", "쇼핑과 맛집, 관광지를 계획적으로 돌아보며 알찬 여행을 만들 수 있어요.", ["계획", "쇼핑", "맛집"]),
            ("싱가포르 🇸🇬", "주요 관광지를 효율적으로 돌아볼 수 있어 짧은 여행에도 잘 어울려요.", ["효율", "도시", "관광"]),
            ("런던 🇬🇧", "역사적인 장소와 박물관을 체계적으로 둘러보며 알찬 여행을 할 수 있어요.", ["역사", "박물관", "문화"])
        ]
    },

    "♒ 물병자리 (1/20 ~ 2/18)": {
        "name": "물병자리",
        "nickname": "톡톡 튀는 독특한 여행자 💜",
        "description": "남들과 조금 다른 특별하고 독특한 경험을 좋아해요.",
        "places": [
            ("베를린 🇩🇪", "개성 넘치는 예술과 독특한 문화가 가득해서 새로운 영감을 받을 수 있어요.", ["예술", "문화", "개성"]),
            ("도쿄 🇯🇵", "최신 기술과 독특한 문화가 공존해서 색다른 경험을 하기 좋아요.", ["미래", "트렌드", "문화"]),
            ("레이캬비크 🇮🇸", "독특하고 신비로운 자연을 경험할 수 있는 특별한 여행지예요.", ["자연", "신비", "독특"])
        ]
    },

    "♓ 물고기자리 (2/19 ~ 3/20)": {
        "name": "물고기자리",
        "nickname": "몽글몽글 감성 여행자 🫧",
        "description": "아름다운 풍경을 바라보며 천천히 쉬고 감성을 충전하는 여행을 좋아해요.",
        "places": [
            ("제주도 🇰🇷", "푸른 바다와 자연을 바라보며 복잡한 생각을 내려놓고 쉬기 좋아요.", ["바다", "힐링", "감성"]),
            ("프라하 🇨🇿", "동화 같은 풍경 속을 천천히 걸으며 감성을 충전하기 좋아요.", ["동화", "산책", "감성"]),
            ("스위스 🇨🇭", "웅장하고 아름다운 자연을 바라보며 마음을 편안하게 만들 수 있어요.", ["자연", "풍경", "힐링"])
        ]
    }
}


# --------------------------------------------------
# 제목
# --------------------------------------------------
st.markdown(
    '<div class="main-title">🌙 별자리 여행지 추천소 ✨</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">나의 별자리와 찰떡궁합인 여행지는 어디일까? 💕</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# 별자리 선택
# --------------------------------------------------
st.markdown('<div class="cute-box">', unsafe_allow_html=True)

st.markdown("### 💌 나의 별자리를 골라주세요!")

zodiac = st.selectbox(
    "별자리 선택",
    list(zodiac_data.keys())
)

st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# 별자리 성향
# --------------------------------------------------
info = zodiac_data[zodiac]

st.markdown(
    f"""
    <div class="cute-box">

        <div class="zodiac-badge">
            {zodiac}
        </div>

        <h2 style="color:#62576e; margin-top:12px; margin-bottom:5px;">
            {info["nickname"]}
        </h2>

        <p style="color:#77717c; line-height:1.8;">
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
        <div style="text-align:center; margin:28px 0 20px 0;">

            <h2 style="
                font-family:'Jua', sans-serif;
                color:#ed83aa;
            ">
                🌸 {info["name"]}에게 추천하는 여행지 🌸
            </h2>

            <p style="color:#999;">
                별자리의 여행 성향을 생각해서 골라봤어요!
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
                    ✨ RECOMMEND {i}
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
            background:linear-gradient(90deg,#fff0f7,#f5efff);
            border-radius:23px;
            padding:20px;
            margin-top:25px;
            color:#927789;
            line-height:1.8;
        ">
            🌷 별이 알려주는 여행지는 참고만 해주세요!<br>
            <b>가장 중요한 건 내가 즐거운 여행을 만드는 것</b>이에요 💕
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
        🌙 made with love for lovely travelers ✨<br>
        Zodiac Travel Finder
    </div>
    """,
    unsafe_allow_html=True
)
