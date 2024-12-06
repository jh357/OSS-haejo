import wx
import time
import threading
import random
import searchtext

class ImagePanel(wx.Panel):
    def __init__(self, parent, image_path, *args, **kwargs):
        super(ImagePanel, self).__init__(parent, *args, **kwargs)
        self.image_path = image_path
        self.image = wx.Image(self.image_path, wx.BITMAP_TYPE_ANY)
        self.min_height = 200  # 최소 높이 설정
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_resize)

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        width, height = self.GetSize()

        # 최소 높이 보장
        height = max(height, self.min_height)

        img_width, img_height = self.image.GetSize()
        scale = min(width / img_width, height / img_height)  # 비율 유지하며 크기 조정
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        bitmap = wx.Bitmap(self.image.Scale(new_width, new_height, wx.IMAGE_QUALITY_HIGH))
        x = (width - new_width) // 2  # 중앙 정렬 (가로)
        y = (height - new_height) // 2  # 중앙 정렬 (세로)
        dc.DrawBitmap(bitmap, x, y)

    def on_resize(self, event):
        self.Refresh()  # 창 크기 변경 시 다시 그리기
        event.Skip()


class RoundedPanel(wx.Panel):
    def __init__(self, parent, radius=15, *args, **kwargs):
        super(RoundedPanel, self).__init__(parent, *args, **kwargs)
        self.radius = radius
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_size(self, event):
        self.Refresh()
        event.Skip()

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        brush = wx.Brush("#333333")
        gc.SetBrush(brush)
        rect = self.GetClientRect()
        path = gc.CreatePath()
        path.AddRoundedRectangle(0, 0, rect.width, rect.height, self.radius)
        gc.DrawPath(path)
    
    




class Chatbot:
    def __init__(self):
        # 기본 응답 설정
        self.responses = searchtext.search_data
        self.korean_to_english = searchtext.korean_to_english
        # search.py에서 데이터를 동적으로 추가
        self.load_responses_from_search()

        self.current_keyword = None  # 현재 키워드
        self.current_index = 0       # 응답 리스트의 현재 인덱스

    def load_responses_from_search(self):
        """search.py에서 데이터를 읽어와 responses에 추가"""
        for key in searchtext.search:
            if hasattr(searchtext, key):
                self.responses[key] = getattr(searchtext, key)

    def set_keyword(self, keyword):
        """사용자가 대화 시작 시 키워드를 설정"""
        keyword = keyword.strip().lower()  # 공백 제거 및 소문자로 변환
        key = self.korean_to_english.get(keyword, keyword)  # 한글이면 변환, 아니면 그대로

        # 키워드 존재 여부 확인 후 설정
        self.current_keyword = next((k for k in self.responses if k.lower() == key), None)

        if self.current_keyword:
            self.current_index = 0  # 키워드가 유효하면 인덱스를 초기화
            return True
        else:
            return False

    def get_next_response(self):
        """현재 키워드의 응답 리스트에서 현재 인덱스의 응답 반환"""
        if self.current_keyword is None:
            return "먼저 대화를 시작해주세요."

        responses = self.responses[self.current_keyword]
        return responses[self.current_index]







class GameFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(GameFrame, self).__init__(*args, **kwargs)
        self.chatbot = Chatbot()

        # search_data에서 데이터를 가져옴
        self.oss_property = searchtext.search_data.get("oss_property", ["OSS 데이터가 없습니다."])
        self.history = searchtext.search_data.get("history", ["역사 데이터가 없습니다."])
        self.copyright = searchtext.search_data.get("copyright", ["저작권 데이터가 없습니다."])
        self.goto_panel3 = False  # Panel1 종료 후 Panel3 이동 여부

        # 메인 패널과 레이아웃
        self.container = wx.Panel(self)
        self.container_sizer = wx.BoxSizer(wx.VERTICAL)

        # 이미지 패널
        self.image_panel = ImagePanel(self.container, "image/save23.png")
        self.container_sizer.Add(self.image_panel, proportion=3, flag=wx.EXPAND | wx.ALL, border=0)

        # Panel 1: 대화 패널
        self.panel1 = RoundedPanel(self.container, radius=20)
        panel1_sizer = wx.BoxSizer(wx.VERTICAL)

        self.text_display = wx.TextCtrl(
            self.panel1,
            value="",
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_NO_VSCROLL | wx.BORDER_NONE
        )
        self.text_display.SetForegroundColour("#FFFFFF")
        self.text_display.SetBackgroundColour("#333333")
        self.text_display.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        panel1_sizer.Add(self.text_display, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # 버튼 레이아웃 추가
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cancel_button = wx.Button(self.panel1, label="취소")
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel_button)
        button_sizer.Add(self.cancel_button, flag=wx.LEFT | wx.BOTTOM, border=8)

        button_sizer.AddStretchSpacer()

        self.next_button = wx.Button(self.panel1, label="다음")
        self.next_button.Bind(wx.EVT_BUTTON, self.on_next_button)
        button_sizer.Add(self.next_button, flag=wx.RIGHT | wx.BOTTOM, border=8)

        panel1_sizer.Add(button_sizer, flag=wx.EXPAND | wx.ALL, border=10)
        self.panel1.SetSizer(panel1_sizer)

        # Panel 2: 검색 패널
        self.panel2 = RoundedPanel(self.container, radius=20)
        panel2_sizer = wx.BoxSizer(wx.VERTICAL)

        # 검색 필드 및 버튼
        self.search_input = wx.TextCtrl(self.panel2, style=wx.TE_PROCESS_ENTER)
        self.search_input.Bind(wx.EVT_TEXT_ENTER, self.on_search_button)
        self.search_button = wx.Button(self.panel2, label="검색")
        self.search_button.Bind(wx.EVT_BUTTON, self.on_search_button)

        # 검색 필드와 버튼 여백 조정
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        search_sizer.Add(self.search_input, proportion=2, flag=wx.ALL | wx.EXPAND, border=5)
        search_sizer.Add(self.search_button, flag=wx.ALL, border=5)
        panel2_sizer.Add(search_sizer, flag=wx.EXPAND | wx.ALL, border=10)

        self.panel2.SetSizer(panel2_sizer)

        self.container.SetSizer(self.container_sizer)


        # Panel 3: OSS 관련 패널
        # Panel 3: OSS 관련 패널
        self.panel3 = RoundedPanel(self.container, radius=20)
        self.panel3_sizer = self.setup_panel3()
        self.panel3.SetSizer(self.panel3_sizer)

        # Panel 4 설정
        self.panel4 = RoundedPanel(self.container, radius=20)
        panel4_sizer = self.setup_panel4()
        self.panel4.SetSizer(panel4_sizer)
        # 컨테이너에 패널 추가 (중복 제거)
        self.container_sizer.Add(self.panel1, proportion=2, flag=wx.EXPAND | wx.ALL, border=16)
        self.container_sizer.Add(self.panel2, proportion=2, flag=wx.EXPAND | wx.ALL, border=16)
        self.container_sizer.Add(self.panel3, proportion=2, flag=wx.EXPAND | wx.ALL, border=16)
        self.container_sizer.Add(self.panel4, proportion=2, flag=wx.EXPAND | wx.ALL, border=16)
        self.panel2.Hide()
        self.panel3.Hide()
        self.panel4.Hide()
        self.container.SetSizer(self.container_sizer)

        wx.CallAfter(self.text_display.SetFocus)
        self.Bind(wx.EVT_SIZE, self.on_resize)

        self.concepts = [0,
            "안녕하세요 무정적분입니다.",
            "제가 여기에 발표에 나온 캐릭터입니다.",
            "제가 만약 여러분들이 만난다면 발표가 준비됐다는 거죠"
        ]
        self.current_index = 0
        self.full_text_displayed = True

    def setup_panel1(self):
        """Panel 1 설정"""
        panel1_sizer = wx.BoxSizer(wx.VERTICAL)

        self.text_display = wx.TextCtrl(
            self.panel1,
            value="",
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_NO_VSCROLL | wx.BORDER_NONE
        )
        self.text_display.SetForegroundColour("#FFFFFF")
        self.text_display.SetBackgroundColour("#333333")
        self.text_display.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        # Enter 키 이벤트 바인딩
        self.text_display.Bind(wx.EVT_KEY_DOWN, self.on_panel1_key_down)

        panel1_sizer.Add(self.text_display, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cancel_button = wx.Button(self.panel1, label="취소")
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel_button)
        button_sizer.Add(self.cancel_button, flag=wx.LEFT | wx.BOTTOM, border=8)

        button_sizer.AddStretchSpacer()

        self.next_button = wx.Button(self.panel1, label="다음")
        self.next_button.Bind(wx.EVT_BUTTON, self.on_next_button)
        button_sizer.Add(self.next_button, flag=wx.RIGHT | wx.BOTTOM, border=8)

        panel1_sizer.Add(button_sizer, flag=wx.EXPAND | wx.ALL, border=10)
        return panel1_sizer

    def setup_panel2(self):
        """Panel 2 설정"""
        panel2_sizer = wx.BoxSizer(wx.VERTICAL)

        self.search_input = wx.TextCtrl(self.panel2, style=wx.TE_PROCESS_ENTER)
        self.search_input.Bind(wx.EVT_TEXT_ENTER, self.on_search_button)
        self.search_button = wx.Button(self.panel2, label="검색")
        self.search_button.Bind(wx.EVT_BUTTON, self.on_search_button)

        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        search_sizer.Add(self.search_input, proportion=2, flag=wx.ALL | wx.EXPAND, border=5)
        search_sizer.Add(self.search_button, flag=wx.ALL, border=5)
        panel2_sizer.Add(search_sizer, flag=wx.EXPAND | wx.ALL, border=10)
        return panel2_sizer

    def setup_panel3(self):
        """Panel 3 설정"""
        panel3_sizer = wx.BoxSizer(wx.VERTICAL)

        # 기본 폰트 설정 (1.5배 크기 + 굵게)
        base_font_size = 12
        self.radio_font = wx.Font(
            int(base_font_size * 1.5),
            wx.FONTFAMILY_SWISS,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD  # 폰트를 굵게 설정
        )

        # 라디오 버튼 추가
        self.radio_oss = wx.RadioButton(self.panel3, label="OSS 특징", style=wx.RB_GROUP)
        self.radio_history = wx.RadioButton(self.panel3, label="역사")
        self.radio_copyright = wx.RadioButton(self.panel3, label="저작권")

        # 라디오 버튼 폰트와 배경 설정
        self.radio_oss.SetFont(self.radio_font)
        self.radio_history.SetFont(self.radio_font)
        self.radio_copyright.SetFont(self.radio_font)

        # 라디오 버튼 텍스트 색상 설정
        self.radio_oss.SetForegroundColour("#007ACC")  # 파란색
        self.radio_history.SetForegroundColour("#28A745")  # 녹색
        self.radio_copyright.SetForegroundColour("#DC3545")  # 빨간색

        # 배경색 설정 (버튼 배경을 패널 배경과 맞춤)
        self.radio_oss.SetBackgroundColour("#333333")  # 패널 배경색과 동일
        self.radio_history.SetBackgroundColour("#333333")
        self.radio_copyright.SetBackgroundColour("#333333")

        # 라디오 버튼 가로 정렬
        self.radio_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.radio_sizer.AddStretchSpacer(1)  # 왼쪽 여백
        self.radio_sizer.Add(self.radio_oss, flag=wx.ALL, border=10)
        self.radio_sizer.Add(self.radio_history, flag=wx.ALL, border=10)
        self.radio_sizer.Add(self.radio_copyright, flag=wx.ALL, border=10)
        self.radio_sizer.AddStretchSpacer(1)  # 오른쪽 여백

        panel3_sizer.AddStretchSpacer(1)  # 위쪽 여백
        panel3_sizer.Add(self.radio_sizer, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL)
        panel3_sizer.AddStretchSpacer(1)  # 아래쪽 여백

        # 버튼 추가 (아래 고정)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cancel_button3 = wx.Button(self.panel3, label="취소")
        self.cancel_button3.Bind(wx.EVT_BUTTON, self.on_cancel_to_panel2)
        button_sizer.Add(self.cancel_button3, flag=wx.LEFT, border=8)

        button_sizer.AddStretchSpacer()

        self.next_button3 = wx.Button(self.panel3, label="다음")
        self.next_button3.Bind(wx.EVT_BUTTON, self.on_next_from_panel3)
        button_sizer.Add(self.next_button3, flag=wx.RIGHT, border=8)

        # 버튼 부분은 아래 고정
        panel3_sizer.Add(button_sizer, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)

        # 창 크기에 따라 동적 레이아웃 조정
        self.Bind(wx.EVT_SIZE, self.on_resize_panel3)

        return panel3_sizer
  
    

    def on_next_from_panel3(self, event):
        """Panel3에서 '다음' 버튼 동작"""
        if self.radio_oss.GetValue():
            self.concepts = self.oss_property  # OSS 관련 데이터 로드
        elif self.radio_history.GetValue():
            self.concepts = self.history  # 역사 관련 데이터 로드
        elif self.radio_copyright.GetValue():
            self.concepts = self.copyright  # 저작권 관련 데이터 로드

        self.current_index = 0  # 선택된 리스트로 인덱스 초기화
        self.switch_to_panel4()
        self.display_next_text(self.text_display_panel4)



    def on_resize_panel3(self, event):
        """Panel 3 크기 변경에 따라 레이아웃 동적 조정"""
        width, _ = self.GetSize()
        margin = int(width * 0.05)  # 창 너비의 5%를 마진으로 설정

        # 라디오 버튼 간 마진 동적 조정
        for item in self.radio_sizer.GetChildren():
            item.SetFlag(wx.ALL)
            item.SetBorder(margin)

        self.panel3.Layout()
        event.Skip()

    def setup_panel4(self):
        """Panel 4 설정"""
        panel4_sizer = wx.BoxSizer(wx.VERTICAL)

        self.text_display_panel4 = wx.TextCtrl(
            self.panel4,
            value="",
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_NO_VSCROLL | wx.BORDER_NONE
        )
        self.text_display_panel4.SetForegroundColour("#FFFFFF")
        self.text_display_panel4.SetBackgroundColour("#333333")
        self.text_display_panel4.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        panel4_sizer.Add(self.text_display_panel4, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.cancel_button_panel4 = wx.Button(self.panel4, label="취소")
        self.cancel_button_panel4.Bind(wx.EVT_BUTTON, self.on_cancel_to_panel3)
        button_sizer.Add(self.cancel_button_panel4, flag=wx.LEFT | wx.BOTTOM, border=8)

        button_sizer.AddStretchSpacer()

        self.next_button_panel4 = wx.Button(self.panel4, label="다음")
        self.next_button_panel4.Bind(wx.EVT_BUTTON, self.on_next_button_panel4)
        button_sizer.Add(self.next_button_panel4, flag=wx.RIGHT | wx.BOTTOM, border=8)

        panel4_sizer.Add(button_sizer, flag=wx.EXPAND | wx.ALL, border=10)
        return panel4_sizer


    def on_cancel_to_panel3(self, event):
        """Panel4에서 '취소' 버튼 동작"""
        self.switch_to_panel3()



    def on_cancel_button(self, event):
        """Panel 1 취소 버튼"""
        self.switch_to_panel2()

    def on_cancel_to_panel2(self, event):
        """Panel3에서 '취소' 버튼 동작"""
        self.switch_to_panel2()


    def on_next_button_panel4(self, event):
        """Panel 4의 다음 버튼 동작"""
        if not self.full_text_displayed:
            self.full_text_displayed = True
            wx.CallAfter(self.text_display_panel4.SetValue, self.concepts[self.current_index])
        elif self.current_index < len(self.concepts) - 1:
            self.current_index += 1
            wx.CallAfter(self.display_next_text, self.text_display_panel4)
        else:
            # 대화 종료 후 Panel 3으로 이동
            self.switch_to_panel3()


    def switch_to_panel1(self):
        """Panel1로 전환"""
        self.panel2.Hide()
        self.panel3.Hide()
        self.panel4.Hide()
        self.panel1.Show()
        self.container.Layout()

    def switch_to_panel2(self):
        """Panel2로 전환"""
        self.panel1.Hide()
        self.panel3.Hide()
        self.panel4.Hide()
        self.panel2.Show()
        self.container.Layout()

    def switch_to_panel3(self):
        """Panel3로 전환"""
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel4.Hide()
        self.panel3.Show()
        self.container.Layout()

    def switch_to_panel4(self):
        """Panel4로 전환"""
        self.panel1.Hide()
        self.panel2.Hide()
        self.panel3.Hide()
        self.panel4.Show()
        self.container.Layout()

    def display_next_text(self, text_ctrl=None):
        """현재 인덱스의 텍스트를 출력"""
        if text_ctrl is None:
            text_ctrl = self.text_display  # 기본적으로 Panel1의 TextCtrl 사용

        if self.current_index < len(self.concepts):
            threading.Thread(target=self.type_text, args=(self.concepts[self.current_index], text_ctrl)).start()
        else:
            # 대화 종료 시 Panel3으로 전환
            self.switch_to_panel3()


    def on_next_button(self, event):
        """Panel1의 '다음' 버튼 동작"""
        if not self.full_text_displayed:
            # 텍스트가 완전히 표시되지 않았다면 바로 표시
            self.full_text_displayed = True
            self.text_display.SetValue(self.concepts[self.current_index])
        elif self.current_index < len(self.concepts) - 1:
            # 다음 텍스트로 이동
            self.current_index += 1
            self.display_next_text()
        else:
            # 대화 종료 후 이동
            if self.goto_panel3:
                self.switch_to_panel3()  # Panel3으로 이동
            else:
                self.switch_to_panel2()  # Panel2로 이동



    def on_search_button(self, event):
        """Panel2에서 검색 버튼 동작"""
        query = self.search_input.GetValue().strip().lower()  # 소문자로 변환하여 비교
        self.search_input.Clear()

        if not query:
            wx.MessageBox("검색어를 입력해주세요.", "알림", wx.OK | wx.ICON_INFORMATION)
            return

        if self.chatbot.set_keyword(query):
            self.concepts = self.chatbot.responses[self.chatbot.current_keyword]
            self.current_index = 0  # 검색 시 인덱스 초기화

            # OSS 검색 여부 확인
            if query == "oss":  # 검색어가 'oss'인 경우
                self.goto_panel3 = True  # Panel3으로 이동하도록 설정
            else:
                self.goto_panel3 = False  # Panel2로 이동하도록 설정

            self.switch_to_panel1()
            self.display_next_text()  # 첫 번째 응답만 표시
        else:
            wx.MessageBox("검색 결과가 없습니다.", "알림", wx.OK | wx.ICON_INFORMATION)




    def on_resize(self, event):
        width, height = self.GetSize()

        base_width, base_height = 100, 40
        scaling_factor = min(width / 400, height / 600)

        new_width = int(base_width * scaling_factor)
        new_height = int(base_height * scaling_factor)

        self.search_button.SetMinSize((new_width, new_height))
        button_font = wx.Font(max(12, int(new_height * 0.5)), wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.search_button.SetFont(button_font)

        self.search_input.SetMinSize((new_width * 4, new_height))
        input_font = wx.Font(max(12, int(new_height * 0.5)), wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.search_input.SetFont(input_font)

        self.search_input.SetMargins(5, 0)
        # 검색 필드 내부 여백 조정
        self.search_input.SetMargins(10, 5)  # 좌우 여백 10, 상하 여백 5

        self.container.Layout()
        event.Skip()

    def type_text(self, text, text_ctrl=None):
        """텍스트를 한 글자씩 출력"""
        self.full_text_displayed = False
        if text_ctrl is None:
            text_ctrl = self.text_display  # 기본적으로 Panel1의 TextCtrl 사용

        wx.CallAfter(text_ctrl.SetValue, "")  # 텍스트 초기화
        for char in text:
            if self.full_text_displayed:
                wx.CallAfter(text_ctrl.SetValue, text)  # 전체 텍스트 바로 출력
                return
            wx.CallAfter(text_ctrl.AppendText, char)  # 한 글자씩 추가
            time.sleep(0.05)  # 타이핑 효과
        self.full_text_displayed = True



app = wx.App(False)
frame = GameFrame(None, title="게임 스타일 대화창", size=(500, 600))
frame.Show()
app.MainLoop()

