# searchtext.py
search = ['git', 'github', 'tml', 'oss', '!']

# 데이터 사전
search_data = {
    "git": ["git에 대하여 설명 하겠습니다."],
    "github": [
        "GitHub는 git의 허브로 여러 오픈소스를 관리하고 협업할 수 있는 플랫폼입니다.",
        "여기까지 GitHub의 이야기였습니다."
    ],
    "tml": ["저는 krita는 오픈소스소프트웨어로 형채를 나타내고 있습니다."],
    "oss": [
        "OSS(Open Source Software)는 누구나 접근 가능하고 기여할 수 있는 소프트웨어를 의미합니다.",
        "OSS의 주로 특성이란",
        "자유로운 사용으로 누구나 무료로 소프트웨어를 사용할 수 있고",
        ""
    ]
    
    , "trap" : []
}

# 한국어 매핑 (한글 키워드 -> 영문 키워드)
korean_to_english = {
    "깃": "git",
    "깃허브": "github",
    "형태": "tml",
    "오픈소스": "oss"
}
