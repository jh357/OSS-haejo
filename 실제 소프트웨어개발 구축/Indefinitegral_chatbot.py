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
        """현재 키워드의 응답 리스트에서 다음 응답 반환"""
        if self.current_keyword is None:
            return "먼저 대화를 시작해주세요."

        responses = self.responses[self.current_keyword]
        response = responses[self.current_index]

        # 인덱스를 다음으로 갱신 (리스트 순환 없음)
        if self.current_index < len(responses) - 1:
            self.current_index += 1
        return response






class GameFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(GameFrame, self).__init__(*args, **kwargs)
        self.chatbot = Chatbot()

        # 메인 패널과 레이아웃
        self.container = wx.Panel(self)
        self.container_sizer = wx.BoxSizer(wx.VERTICAL)

        # 이미지 패널
        self.image_panel = ImagePanel(self.container, "image/background.jpg")
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

        self.container_sizer.Add(self.panel1, proportion=2, flag=wx.EXPAND | wx.ALL, border=16)
        self.container_sizer.Add(self.panel2, proportion=2, flag=wx.EXPAND | wx.ALL, border=16)
        self.panel2.Hide()

        self.container.SetSizer(self.container_sizer)

        self.Bind(wx.EVT_SIZE, self.on_resize)

        self.concepts = [
            "안녕하세요 무정적분입니다.",
            "제가 여기에 발표에 나온 캐릭터입니다.",
            "제가 만약 여러분들이 만난다면 발표가 준비됐다는 거죠"
        ]
        self.current_index = 0
        self.full_text_displayed = True

    def switch_to_panel1(self):
        self.panel2.Hide()
        self.panel1.Show()
        self.container.Layout()

    def switch_to_panel2(self):
        self.panel1.Hide()
        self.panel2.Show()
        self.container.Layout()

    def on_next_button(self, event):
        if not self.full_text_displayed:
            self.full_text_displayed = True
        elif self.current_index < len(self.concepts):
            threading.Thread(target=self.type_text, args=(self.concepts[self.current_index],)).start()
            self.current_index += 1
        else:
            self.switch_to_panel2()

    def on_cancel_button(self, event):
        self.switch_to_panel2()

    def on_search_button(self, event):
        query = self.search_input.GetValue().strip()
        self.search_input.Clear()

        if not query:
            wx.MessageBox("검색어를 입력해주세요.", "알림", wx.OK | wx.ICON_INFORMATION)
            return

        if self.chatbot.set_keyword(query):
            self.concepts = self.chatbot.responses[self.chatbot.current_keyword]
            self.current_index = 0
            self.switch_to_panel1()
            self.text_display.SetValue(self.chatbot.get_next_response())
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

    def type_text(self, text):
        self.full_text_displayed = False
        self.text_display.SetValue("")
        for char in text:
            if self.full_text_displayed:
                wx.CallAfter(self.text_display.SetValue, text)
                return
            wx.CallAfter(self.text_display.AppendText, char)
            time.sleep(0.05)
        self.full_text_displayed = True



app = wx.App(False)
frame = GameFrame(None, title="게임 스타일 대화창", size=(600, 800))
frame.Show()
app.MainLoop()

