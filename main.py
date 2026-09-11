# main.py
# ============================================================
# 전국 시군구별 인구 구조 지도
# - 고령화율: 65세 이상 인구 비율
# - 유소년 비율: 0~14세 인구 비율
#
# 필요한 라이브러리:
# streamlit, pandas, numpy, plotly, requests
#
# 행정구역 코드는 반드시 문자열로 처리합니다.
# ============================================================

import io
import gzip
import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


# ============================================================
# 1. 페이지 설정
# ============================================================

st.set_page_config(
    page_title="전국 인구구조 지도",
    page_icon="🗺️",
    layout="wide",
)


# ============================================================
# 2. 데이터 주소
# ============================================================

POPULATION_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/main/"
    "data/population_yearly.csv.gz"
)

GEOJSON_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/main/"
    "data/boundaries/sigungu_kr.geojson"
)


# ============================================================
# 3. 색상 설정
# ============================================================

# 고령화율:
# 19%, 23%, 28%, 38%를 경계로 5단계
ELDERLY_COLORS = [
    "#E8F5E9",
    "#C8E6C9",
    "#81C784",
    "#43A047",
    "#1B5E20",
]

ELDERLY_LABELS = [
    "19% 미만",
    "19% 이상 ~ 23% 미만",
    "23% 이상 ~ 28% 미만",
    "28% 이상 ~ 38% 미만",
    "38% 이상",
]


# 유소년 비율은 고령화율보다 훨씬 낮기 때문에
# 별도의 경계값을 사용합니다.
#
# 0~14세 인구 비율을 0~15% 범위에서 5단계로 나눕니다.
YOUTH_COLORS = [
    "#FFF3E0",
    "#FFE0B2",
    "#FFCC80",
    "#FF9800",
    "#E65100",
]

YOUTH_LABELS = [
    "6% 미만",
    "6% 이상 ~ 8% 미만",
    "8% 이상 ~ 10% 미만",
    "10% 이상 ~ 12% 미만",
    "12% 이상",
]


# 실제 단계 경계값
ELDERLY_BREAKS = [19, 23, 28, 38]
YOUTH_BREAKS = [6, 8, 10, 12]


# ============================================================
# 4. 데이터 다운로드
# ============================================================

@st.cache_data(ttl=60 * 60 * 24)
def load_population_data():
    """
    전국 읍·면·동 인구 데이터를 다운로드합니다.

    코드 열은 나중에 앞 5자리를 잘라야 하므로
    숫자로 변환하지 않고 문자열로 유지합니다.
    """

    response = requests.get(
        POPULATION_URL,
        timeout=120,
    )
    response.raise_for_status()

    compressed = io.BytesIO(response.content)

    with gzip.GzipFile(fileobj=compressed) as gz:
        df = pd.read_csv(
            gz,
            low_memory=False,
            dtype={"코드": "string"},
        )

    return df


@st.cache_data(ttl=60 * 60 * 24)
def load_geojson():
    """전국 시군구 경계 GeoJSON을 다운로드합니다."""

    response = requests.get(
        GEOJSON_URL,
        timeout=120,
    )
    response.raise_for_status()

    return response.json()


# ============================================================
# 5. 행정구역 코드 보정
# ============================================================

def fix_sigungu_code(code):
    """
    과거 연도의 시군구 코드를 현재 경계 파일에 맞게 보정합니다.

    42xxx → 51xxx
    45xxx → 52xxx
    47720 → 27720
    """

    if pd.isna(code):
        return None

    code = str(code).strip().zfill(5)

    # 강원 지역 과거 코드
    if code.startswith("42"):
        code = "51" + code[2:]

    # 전북 지역 과거 코드
    elif code.startswith("45"):
        code = "52" + code[2:]

    # 군위군
    if code == "47720":
        code = "27720"

    return code


# ============================================================
# 6. 나이 열 찾기
# ============================================================

def get_age_columns(df):
    """'계_0세' 같은 전체 인구 나이 열을 찾아냅니다."""

    return [
        column
        for column in df.columns
        if str(column).startswith("계_")
    ]


def age_from_column(column):
    """
    '계_15세' → 15
    '계_100세 이상' → 100
    """

    text = str(column).replace("계_", "").replace("세", "").strip()

    if text == "100세 이상":
        return 100

    try:
        return int(text)
    except ValueError:
        return None


# ============================================================
# 7. 연도별 시군구 데이터 계산
# ============================================================

@st.cache_data(ttl=60 * 60 * 24)
def make_yearly_sigungu_data(df):
    """
    읍·면·동 데이터를 시군구 단위로 합칩니다.

    모든 연도를 미리 계산해 두기 때문에
    화면에서 연도 슬라이더를 움직일 때 빠르게 바뀝니다.
    """

    data = df.copy()

    # --------------------------------------------------------
    # 코드 열은 반드시 문자열
    # --------------------------------------------------------

    data["코드"] = (
        data["코드"]
        .astype("string")
        .str.strip()
        .str.zfill(10)
    )

    # 행정동 코드 앞 5자리 = 시군구 코드
    data["시군구코드"] = data["코드"].str[:5]

    # 과거 코드 보정
    data["시군구코드"] = data["시군구코드"].apply(
        fix_sigungu_code
    )

    # 연도 숫자화
    data["연도"] = pd.to_numeric(
        data["연도"],
        errors="coerce",
    )

    data = data.dropna(subset=["연도", "시군구코드"])

    data["연도"] = data["연도"].astype(int)

    # --------------------------------------------------------
    # 나이별 '계_' 열
    # --------------------------------------------------------

    age_columns = get_age_columns(data)

    if not age_columns:
        raise ValueError(
            "계_0세, 계_1세 등의 나이별 인구 열을 찾을 수 없습니다."
        )

    # 나이별 열 숫자 변환
    for column in age_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce",
        ).fillna(0)

    # --------------------------------------------------------
    # 전체 / 유소년 / 고령 인구 계산
    # --------------------------------------------------------

    age_info = {
        column: age_from_column(column)
        for column in age_columns
    }

    youth_columns = [
        column
        for column, age in age_info.items()
        if age is not None and 0 <= age <= 14
    ]

    elderly_columns = [
        column
        for column, age in age_info.items()
        if age is not None and age >= 65
    ]

    data["전체인구"] = data[age_columns].sum(axis=1)

    data["유소년인구"] = data[youth_columns].sum(axis=1)

    data["고령인구"] = data[elderly_columns].sum(axis=1)

    # --------------------------------------------------------
    # 시군구 단위로 합치기
    # --------------------------------------------------------

    yearly = (
        data.groupby(
            ["연도", "시군구코드"],
            as_index=False,
        )
        .agg(
            전체인구=("전체인구", "sum"),
            유소년인구=("유소년인구", "sum"),
            고령인구=("고령인구", "sum"),
            시군구=("시군구", "first"),
            시도=("시도", "first"),
        )
    )

    # --------------------------------------------------------
    # 비율 계산
    # --------------------------------------------------------

    yearly["고령화율"] = (
        yearly["고령인구"]
        / yearly["전체인구"]
        * 100
    )

    yearly["유소년비율"] = (
        yearly["유소년인구"]
        / yearly["전체인구"]
        * 100
    )

    yearly["고령화율"] = yearly["고령화율"].round(2)
    yearly["유소년비율"] = yearly["유소년비율"].round(2)

    return yearly


# ============================================================
# 8. 단계 계산
# ============================================================

def get_grade(value, indicator):
    """선택한 지표의 값을 0~4단계로 변환합니다."""

    if pd.isna(value):
        return None

    if indicator == "고령화율 (65세 이상)":
        breaks = ELDERLY_BREAKS

    else:
        breaks = YOUTH_BREAKS

    if value < breaks[0]:
        return 0

    if value < breaks[1]:
        return 1

    if value < breaks[2]:
        return 2

    if value < breaks[3]:
        return 3

    return 4


# ============================================================
# 9. GeoJSON 코드 준비
# ============================================================

def prepare_geojson(geojson):
    """
    GeoJSON의 시군구 코드도 문자열 5자리로 통일합니다.
    """

    for feature in geojson.get("features", []):

        properties = feature.get("properties", {})

        if "코드" in properties:
            properties["코드"] = (
                str(properties["코드"])
                .strip()
                .zfill(5)
            )

    return geojson


# ============================================================
# 10. 지도 만들기
# ============================================================

def make_map(
    geojson,
    data,
    indicator,
):
    """
    선택한 연도 / 지표 / 시도에 맞춰
    단계구분도를 만듭니다.
    """

    fig = go.Figure()

    # --------------------------------------------------------
    # 지표별 색상과 범례
    # --------------------------------------------------------

    if indicator == "고령화율 (65세 이상)":

        colors = ELDERLY_COLORS
        labels = ELDERLY_LABELS
        value_column = "고령화율"

    else:

        colors = YOUTH_COLORS
        labels = YOUTH_LABELS
        value_column = "유소년비율"

    # --------------------------------------------------------
    # 5단계 각각 별도의 trace를 만듭니다.
    #
    # 이렇게 하면 색이 연속적으로 변하지 않고
    # 정확히 5단계로 끊어집니다.
    # --------------------------------------------------------

    for grade in range(5):

        part = data[
            data["등급"] == grade
        ].copy()

        if part.empty:
            continue

        customdata = part[
            [
                "시군구",
                "시도",
                value_column,
            ]
        ].values

        fig.add_trace(
            go.Choropleth(
                geojson=geojson,

                # 지역을 이름이 아닌 코드로 연결
                locations=part["시군구코드"],

                featureidkey="properties.코드",

                z=part[value_column],

                zmin=0,
                zmax=100,

                colorscale=[
                    [0, colors[grade]],
                    [1, colors[grade]],
                ],

                marker_line_color="white",
                marker_line_width=0.7,

                name=labels[grade],

                customdata=customdata,

                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "시도: %{customdata[1]}<br>"
                    f"{indicator.split(' ')[0]}: "
                    "%{customdata[2]:.2f}%"
                    "<extra></extra>"
                ),

                showscale=False,
                showlegend=True,
            )
        )

    # --------------------------------------------------------
    # 경계 파일에는 있지만 인구 데이터와 매칭되지 않는 지역
    # --------------------------------------------------------

    geo_codes = {
        feature["properties"]["코드"]
        for feature in geojson.get("features", [])
        if "코드" in feature.get("properties", {})
    }

    matched_codes = set(
        data["시군구코드"].dropna().astype(str)
    )

    unmatched_codes = geo_codes - matched_codes

    if unmatched_codes:

        # 회색 지역을 별도 trace로 표시합니다.
        unmatched_features = [
            feature
            for feature in geojson["features"]
            if feature["properties"].get("코드")
            in unmatched_codes
        ]

        gray_geojson = {
            "type": "FeatureCollection",
            "features": unmatched_features,
        }

        fig.add_trace(
            go.Choropleth(
                geojson=gray_geojson,
                locations=list(unmatched_codes),
                featureidkey="properties.코드",

                z=[0] * len(unmatched_codes),

                colorscale=[
                    [0, "#D9D9D9"],
                    [1, "#D9D9D9"],
                ],

                zmin=0,
                zmax=1,

                marker_line_color="white",
                marker_line_width=0.7,

                name="자료 없음",

                hovertemplate=(
                    "<b>%{location}</b><br>"
                    "해당 연도 자료 없음"
                    "<extra></extra>"
                ),

                showscale=False,
                showlegend=True,
            )
        )

    # --------------------------------------------------------
    # 지도 설정
    # --------------------------------------------------------

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
        showcountries=False,
        showcoastlines=False,
        showland=False,
        showlakes=False,
        bgcolor="rgba(0,0,0,0)",
    )

    fig.update_layout(
        height=780,

        margin=dict(
            l=0,
            r=0,
            t=5,
            b=5,
        ),

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        legend=dict(
            title=dict(
                text=f"<b>{indicator}</b>"
            ),

            orientation="h",

            yanchor="bottom",
            y=0.01,

            xanchor="center",
            x=0.5,

            bgcolor="rgba(255,255,255,0.92)",

            bordercolor="#DDDDDD",
            borderwidth=1,

            font=dict(size=12),
        ),

        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
        ),
    )

    return fig


# ============================================================
# 11. 제목
# ============================================================

st.title("🗺️ 전국 인구구조 지도")

st.markdown(
    """
    연도와 지표를 선택해서 전국 시군구의 인구 구조를 비교해 보세요.

    **색이 진할수록 선택한 지표의 비율이 높습니다.**
    """
)


# ============================================================
# 12. 데이터 불러오기
# ============================================================

try:

    with st.spinner("전국 인구 데이터를 불러오는 중입니다..."):

        population_df = load_population_data()
        geojson = load_geojson()

        geojson = prepare_geojson(geojson)

        yearly_df = make_yearly_sigungu_data(
            population_df
        )

except Exception as error:

    st.error(
        "데이터를 불러오거나 계산하는 과정에서 문제가 발생했습니다."
    )

    st.code(str(error))

    st.stop()


# ============================================================
# 13. 선택 컨트롤
# ============================================================

available_years = sorted(
    yearly_df["연도"].dropna().unique()
)

available_years = [
    int(year)
    for year in available_years
]

min_year = min(available_years)
max_year = max(available_years)


st.subheader("🔎 지도 조건 선택")


# ------------------------------------------------------------
# 연도 슬라이더
# ------------------------------------------------------------

selected_year = st.slider(
    "연도",
    min_value=min_year,
    max_value=max_year,
    value=max_year,
    step=1,
)


# ------------------------------------------------------------
# 지표 선택
# ------------------------------------------------------------

indicator = st.selectbox(
    "보고 싶은 지표",
    [
        "고령화율 (65세 이상)",
        "유소년 비율 (0~14세)",
    ],
)


# ------------------------------------------------------------
# 시도 선택
# ------------------------------------------------------------

year_df = yearly_df[
    yearly_df["연도"] == selected_year
].copy()

sido_list = sorted(
    year_df["시도"]
    .dropna()
    .astype(str)
    .unique()
)

selected_sido = st.selectbox(
    "시도",
    ["전국"] + sido_list,
)


# ============================================================
# 14. 현재 조건 데이터
# ============================================================

current_df = year_df.copy()

if selected_sido != "전국":

    current_df = current_df[
        current_df["시도"] == selected_sido
    ].copy()


# ============================================================
# 15. 코드 매칭
# ============================================================

geo_codes = {
    feature["properties"]["코드"]
    for feature in geojson.get("features", [])
    if "코드" in feature.get("properties", {})
}

current_df["시군구코드"] = (
    current_df["시군구코드"]
    .astype("string")
    .str.strip()
    .str.zfill(5)
)

matched_df = current_df[
    current_df["시군구코드"].isin(geo_codes)
].copy()

unmatched_df = current_df[
    ~current_df["시군구코드"].isin(geo_codes)
].copy()


# ============================================================
# 16. 지도용 등급
# ============================================================

value_column = (
    "고령화율"
    if indicator == "고령화율 (65세 이상)"
    else "유소년비율"
)

matched_df["등급"] = matched_df[value_column].apply(
    lambda value: get_grade(value, indicator)
)


# ============================================================
# 17. 지표 카드
# ============================================================

if not current_df.empty:

    # 전국 카드에서는 해당 연도의 전국 전체 데이터를 사용하고,
    # 시도를 선택하면 그 시도의 시군구 데이터를 기준으로 합니다.

    total_population = current_df["전체인구"].sum()

    if indicator == "고령화율 (65세 이상)":

        total_indicator_population = current_df[
            "고령인구"
        ].sum()

    else:

        total_indicator_population = current_df[
            "유소년인구"
        ].sum()

    if total_population > 0:

        national_rate = (
            total_indicator_population
            / total_population
            * 100
        )

    else:
        national_rate = 0

    highest = current_df.loc[
        current_df[value_column].idxmax()
    ]

    lowest = current_df.loc[
        current_df[value_column].idxmin()
    ]

else:

    national_rate = 0
    highest = None
    lowest = None


# ------------------------------------------------------------
# 카드 3개
# ------------------------------------------------------------

card1, card2, card3 = st.columns(3)


with card1:

    st.metric(
        label=(
            "전국 고령화율"
            if selected_sido == "전국"
            else f"{selected_sido} 고령화율"
        ),
        value=(
            f"{national_rate:.2f}%"
            if highest is not None
            else "-"
        ),
    )


with card2:

    if highest is not None:

        st.metric(
            label="가장 높은 시군구",
            value=str(highest["시군구"]),
            delta=f"{highest[value_column]:.2f}%",
        )

    else:

        st.metric(
            label="가장 높은 시군구",
            value="-",
        )


with card3:

    if lowest is not None:

        st.metric(
            label="가장 낮은 시군구",
            value=str(lowest["시군구"]),
            delta=f"{lowest[value_column]:.2f}%",
        )

    else:

        st.metric(
            label="가장 낮은 시군구",
            value="-",
        )


st.caption(
    f"현재 선택: {selected_year}년 · "
    f"{selected_sido} · {indicator}"
)


# ============================================================
# 18. 지도
# ============================================================

st.plotly_chart(
    make_map(
        geojson,
        matched_df,
        indicator,
    ),
    use_container_width=True,
    config={
        "displayModeBar": False,
        "scrollZoom": False,
    },
)


# ============================================================
# 19. 코드 매칭 실패 안내
# ============================================================

if not unmatched_df.empty:

    unmatched_names = (
        unmatched_df["시군구"]
        .dropna()
        .astype(str)
        .drop_duplicates()
        .tolist()
    )

    st.warning(
        f"""
        **지도 경계와 코드가 맞지 않는 지역이 "
        f"{len(unmatched_names)}곳 있습니다.**

        이 지역은 지도에서 회색으로 표시되거나 지도 경계와
        연결되지 않아 표시되지 않을 수 있습니다.

        해당 연도의 행정구역 개편 등으로 인해 현재 경계 파일과
        코드가 일치하지 않는 지역입니다.

        확인된 지역:
        {", ".join(unmatched_names)}
        """
    )


# ============================================================
# 20. TOP 10 표
# ============================================================

st.divider()

st.subheader(
    f"📊 {selected_year}년 {selected_sido} "
    f"{indicator} 비교"
)


high_10 = (
    current_df
    .sort_values(
        value_column,
        ascending=False,
    )
    .head(10)
    .reset_index(drop=True)
)

low_10 = (
    current_df
    .sort_values(
        value_column,
        ascending=True,
    )
    .head(10)
    .reset_index(drop=True)
)


left, right = st.columns(2)


# ------------------------------------------------------------
# 높은 지역
# ------------------------------------------------------------

with left:

    st.markdown("### 🔴 높은 곳 TOP 10")

    if not high_10.empty:

        high_table = high_10[
            [
                "시도",
                "시군구",
                value_column,
            ]
        ].copy()

        high_table.index = range(
            1,
            len(high_table) + 1,
        )

        high_table[value_column] = (
            high_table[value_column]
            .map(lambda x: f"{x:.2f}%")
        )

        st.dataframe(
            high_table,
            use_container_width=True,
            height=390,
        )

    else:

        st.info("표시할 데이터가 없습니다.")


# ------------------------------------------------------------
# 낮은 지역
# ------------------------------------------------------------

with right:

    st.markdown("### 🟢 낮은 곳 TOP 10")

    if not low_10.empty:

        low_table = low_10[
            [
                "시도",
                "시군구",
                value_column,
            ]
        ].copy()

        low_table.index = range(
            1,
            len(low_table) + 1,
        )

        low_table[value_column] = (
            low_table[value_column]
            .map(lambda x: f"{x:.2f}%")
        )

        st.dataframe(
            low_table,
            use_container_width=True,
            height=390,
        )

    else:

        st.info("표시할 데이터가 없습니다.")


# ============================================================
# 21. 하단 설명
# ============================================================

st.divider()

if indicator == "고령화율 (65세 이상)":

    st.caption(
        "고령화율 = 65세 이상 인구 ÷ 전체 인구 × 100"
    )

    st.caption(
        "색상 구간: 19% 미만 / 19~23% / 23~28% / "
        "28~38% / 38% 이상"
    )

else:

    st.caption(
        "유소년 비율 = 0~14세 인구 ÷ 전체 인구 × 100"
    )

    st.caption(
        "색상 구간: 6% 미만 / 6~8% / 8~10% / "
        "10~12% / 12% 이상"
    )

st.caption(
    "※ 읍·면·동 인구를 행정동 코드 앞 5자리 기준으로 "
    "시군구 단위로 합산하여 계산했습니다."
)

st.caption(
    "※ 과거 행정구역 코드는 42→51, 45→52, "
    "47720→27720으로 보정했습니다."
)
