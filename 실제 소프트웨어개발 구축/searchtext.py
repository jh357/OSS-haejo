# searchtext.py
search = ['git', 'github', 'tml', 'oss', '!','oss_property']

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
        "자유로운 사용으로 누구나 무료로 소프트웨어를 사용할 수 있고"
        ,"소스 코드 접근 가능으로 사용자가 소스 코드를 열람하고 수정할 수 있고"
        ,"배포을 통해 수정된 버전이나 원본을 다른 사람들과 자유롭게 공유 가능하고"
        ,"커뮤니티 기반 개발으로 개발자들이 협업하여 소프트웨어를 개선합니다."
        ,"oss의 장단점이 궁금하면 검색해주세요 (oss 장단점)"
    ],
    "oss_property" : ["장점은  커스터마이징 가능으로 소스 코드를 수정하여 특정 요구 사항에 맞게 소프트웨어를 변경할 수 있습니다."
                      ," 또한 보안성으로는 코드가 공개되므로 전 세계 개발자들이 보안 취약점을 확인하고 수정할 수 있어 보안이 강화됩니다."
                      , "독립성에서는 상용 소프트웨어의 공급업체에 의존하지 않고 독립적으로 소프트웨어를 운영할 수 있습니다." 
                      , "또한 커뮤니티의 지원을 통해 문제를 해결하고 최신 기능을 빠르게 도입할 수 있습니다."
                      , "그러나 단점도 있습니다. oss 단점은" 
                      , "기술 지원 부족으로 일부 OSS는 공식적인 기술 지원이 부족할 수 있으며 이로 인해 문제 해결을 위해서는 사용자가 커뮤니티에 의존해야 할 수 밖에 없습니다."
                      ,"또한 일부 오픈 소스 소프트웨어는 사용법이나 설정이 복잡할 수 있으므로 초기 학습이 필요할 수 있습니다."
                        ]
    , "trap" : ["여기가 말하면 뭔가 제 코드가 엉망이 되였군요",
                "여기는 search 함수에 없는 속성입니다."
                ]
, "oss_history_1950_1960" : ["이 시기는 아직 오픈소스라는 용어가 존재하지 않았지만 소프트웨어의 공유와 협업을 통해 문제를 해결하려는 문화가 형성되었습니다."
                            ,"초기 소프트웨어 공유 문화에서 당시에는 소프트웨어가 독립적인 제품으로 여겨지지 않았고, 주로 하드웨어와 함께 무료로 제공되었습니다."
                             ,"컴퓨터 제조업체들은 사용자가 소프트웨어를 직접 수정하거나 개선할 수 있도록 소스 코드를 공개한 상태로 배포했습니다."
                             ,"그리고 주로 사용자들은 대학, 연구소, 그리고 정부기관은 초기 컴퓨터 기술의 주요 사용자였습니다."
                             ,"이들은 소프트웨어를 자유롭게 공유하며 서로의 코드를 개선하는 데 기여했습니다."
                             ,"이러한 문화는 오늘날 오픈소스 협업 방식의 초기 모델로 볼 수 있습니다."
                             ,"IBM은 당시 컴퓨터 하드웨어 시장의 선두주자였으며, 소프트웨어 역시 함께 제공했습니다."
                              , "1950년대에는 IBM 701, IBM 704와 같은 초기 컴퓨터용 소프트웨어가 연구 커뮤니티 내에서 공유되었습니다."
                             ,"이때 여려 오른소스에 대한 사용자 그룹이 있었습니다."
                             ,"IBM 컴퓨터 사용자들이 자발적으로 만든 사용자 그룹으로, 소프트웨어를 공유하고 공동 문제를 해결하기 위한 네트워크였습니다."
                             ,"SHARE는 소프트웨어 공유를 촉진하며, 초기의 오픈소스 철학과 유사한 활동을 전개했습니다."
                             , "ARPA와 초기 인터넷의 기반 마련 1960년대 말에 들어서면서 미국 방위고등연구계획국(ARPA)이 인터넷의 전신인 ARPANET을 개발하기 시작했습니다."
                             ,"ARPANET 개발 과정에서 네트워킹 프로토콜과 소프트웨어가 협업을 통해 개발되었고, 소스 코드가 공개된 상태로 사용되었습니다."
                             ,"MIT와 해커 문화도 있습니다."
                              ,"MIT의 인공지능 연구소(AI Lab)에서 초기 컴퓨터 과학자와 개발자들이 자유롭게 코드를 공유하며 협력하는 해커 문화가 시작되었습니다."
                             ,"이 해커들은 기술적 문제 해결과 코드 공유를 강조하며, 이후 오픈소스 운동에 지대한 영향을 미쳤습니다."
                             ,"이 문화는 후일 오픈소스 네트워크 기술의 탄생에 영향을 미쳤습니다."
                            ]
                            , "oss_history_1970_Unix" : [
                                
                            ]
                            , "oss_history_1970_Scct" : [
                                
                            ]
                            #1980년대
                            , "oss_history_1980_GNU": [
                                
                            ]
                            ,"oss_history_1980_X_window" :[
                                
                            ]
                            ,"oss_history_1980_FSF":[
                                
                            ]
                            ,"oss_history_1980_BSD" :[
                                
                            ]
                            ,"oss_history_1980_hacker_culture":[
                                
                            ]
                            #1990년대
                            ,"oss_history_1990_BSD" : [
                                
                            ]
                            ,"oss_history_1990_Lunux" : [
                                
                            ]
                            ,"oss_history_1990_GNU" : [
                                
                            ]
                            ,"oss_history_1990_python" : [
                                
                            ]
                            ,"oss_history_1990_Red_Hat" : [
                                
                            ]
                            , "oss_history_1990_Netscape" : [
                                
                            ]
                            ,"oss_history_1990_MySQL" : [
                                
                            ]
                            ,"oss_history_1990_GNOME" : [
                                
                            ]
                            ,"oss_history_1990_OSS" : [
                                
                            ]
                            ,"oss_history_1990_OSI" : [
                                
                            ]
                            ,"oss_history_1990_Mozilla" : [
                                
                            ]
                            ,"oss_history_1990_SourceForge" : [
                                
                            ]
                            ,"oss_history_2000_ASF" : [
                                
                            ]
                            ,"oss_history_2000_Red_Hat" : [
                                
                            ]
                            ,"oss_history_2000_OpenOffice_org" : [
                                
                            ]
                            ,"oss_history_2000_Mozilla_Firefox" : [
                                
                            ]
                            ,"oss_history_2000_Ubuntu" : [
                                
                            ]
                            ,"oss_history_2000_Git" : [
                                
                            ]
                            ,"oss_history_2000_WordPress" : [
                                
                            ]
                            ,"oss_history_2000_Hadoop" : [
                                
                            ]
                            ,"oss_history_2000_Ubuntu" : [
                                
                            ]
                            ,"oss_history_2000_MySQL" : [
                                
                            ]
                            ,"oss_history_2000_" : [
                                
                            ]
                            ,"oss_history_2000_Android" : [
                                
                            ]
                            #2010년대
                            ,"oss_history_2010_OpenStack" : [
                                
                            ]
                            ,"oss_history_2010_GitHub" : [
                                
                            ]
                            ,"oss_history_2010_Node.js" : [
                                
                            ]
                            ,"oss_history_2010_Apache_Hadoop" : [
                                
                            ]
                            ,"oss_history_2010_Docker" : [
                                
                            ]
                            ,"oss_history_2010_TensorFlow" : [
                                
                            ]
                            ,"oss_history_2010_Kubernetes" : [
                                
                            ]
                            ,"oss_history_2010_React" : [
                                
                            ]
                            ,"oss_history_2010_PyTorch" : [
                                
                            ]
                            ,"oss_history_2010_GitHub" : [
                                
                            ]
                            ,"oss_history_2010_Visual_Studio_Code" : [
                                
                            ]
                            ,"oss_history_2010_LibreOffice" : [
                                
                            ]
                            ,"oss_history_2010_Ansible" : [
                                
                            ]
                            #2020년대
                            ,"oss_history_2020" : [
                                
                            ]
                            ,"oss_history_2020_ChatGPT" : [
                                
                            ]
                            ,"oss_history_2020_Kubernetes" : [
                                
                            ]
                            ,"oss_history_2020_Flutter_and_React_Native" : [
                                
                            ]
                            ,"oss_history_2020_Popularization_of_data_engineering_tools" : [
                                
                            ]
                            ,"oss_history_2020_Stable_Diffusion" : [
                                
                            ]
                            ,"oss_history_2020_MLOps" : [
                                
                            ]
                            ,"oss_history_2020_GitHub_Copilot" : [
                                
                            ]
       # OSS 저작건
       ,"oss_copyright" : [
       "오픈 소스 소프트웨어의 코드, 문서, 기타 창작물은 저작권법에 따라 보호된다."
       "즉 오픈 소스 소프트웨어의 개발자는 해당 소스 코드에 대한 저작권을 보유해야 하고 이를 통해 코드의 복제, 배포, 수정 등을 제어할 수 있다."
       ,"저작권의 양도로 오픈 소스 프로젝트에서는 원저작자가 자신의 저작권을 그대로 두고, 특정 조건 하에 다른 사람들이 코드를 수정하고 배포할 수 있도록 허락하는 라이선스를 제공합니다"                        
                            ]
                            
                            
                            

}

# 한국어 매핑 (한글 키워드 -> 영문 키워드)
korean_to_english = {
    "깃": "git",
    "깃허브": "github",
    "티엠아이": "tml",
    "오픈소스": "os"
    , "오픈소스소프트웨어": "oss"
    ,"oss 장단점" : "oss_property"
    ,"oss의 장단점" : "oss_property"
    
    
    # 영어 문장을 적는데 한영키 안바꾸고 한국어로 적을떄 대비
    
    ,"ㅐㄴㄴ":"oss"
    ,"햣":"git"
    ,"햐소ㅕㅠ":"github"
}

keyword_combinations = {
    "oss 장단점": "oss_property",
    "oss 역사": "oss_history",
    "git 장단점": "git_property"
}


subkey = ["역사", "장단점", "개념", "사용 방법"]

panel3_keywords = ['vecter/panel3', '#panel3', '!panel3']






