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
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_resize)

    def on_paint(self, event):
        dc = wx.PaintDC(self)
        width, height = self.GetSize()
        img_width, img_height = self.image.GetSize()

        # 비율 유지하며 이미지 크기 조정
        scale = min(width / img_width, height / img_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        bitmap = wx.Bitmap(self.image.Scale(new_width, new_height, wx.IMAGE_QUALITY_HIGH))
        x = (width - new_width) // 2  # 이미지 중앙 정렬 (가로)
        y = (height - new_height) // 2  # 이미지 중앙 정렬 (세로)
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
        self.responses = {
            "안녕": ["안녕하세요!", "여기 발표에 나와서 영광입니다."],
            "test": ["텍스트 크기 테스트텍스트 크기 테스트텍스트 크기 테스트텍스트 크기 테스트텍스트 크기 테스트텍스트 크기 테스트텍스트 크기 테스트텍스트 크기 테스트"]
        }
        
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
        if keyword in (key.lower() for key in self.responses):  # 대소문자 무시 비교
            self.current_keyword = next(key for key in self.responses if key.lower() == keyword)
            self.current_index = 0  # 키워드가 변경되면 인덱스를 초기화
            return True
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
        self.chatbot = Chatbot()  # 챗봇 인스턴스 생성
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 이미지 패널 추가
        image_panel = ImagePanel(panel, "image/background.jpg")  # 이미지 경로를 지정
        main_sizer.Add(image_panel, proportion=2, flag=wx.EXPAND | wx.ALL, border=0)

        # RoundedPanel 추가
        dialog_panel = RoundedPanel(panel, radius=20)
        dialog_sizer = wx.BoxSizer(wx.VERTICAL)

        # 텍스트 디스플레이
# 텍스트 디스플레이
        self.text_display = wx.TextCtrl(
            dialog_panel,
            value="",
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_NO_VSCROLL | wx.BORDER_NONE
        )
        self.text_display.SetForegroundColour("#FFFFFF")
        self.text_display.SetBackgroundColour("#333333")
        self.text_display.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        dialog_sizer.Add(self.text_display, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # 검색 입력 필드와 버튼
        # 검색 입력 필드와 버튼
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 취소 버튼 추가
        self.cancel_button = wx.Button(dialog_panel, label="취소")
        self.cancel_button.Disable()  # 초기 상태에서 비활성화
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel_button)

        self.search_input = wx.TextCtrl(dialog_panel)
        self.search_input.Disable()  # 초기 상태에서 비활성화
        self.search_button = wx.Button(dialog_panel, label="검색")
        self.search_button.Disable()  # 초기 상태에서 비활성화
        self.search_button.Bind(wx.EVT_BUTTON, self.on_search_button)

        # 버튼 및 입력 필드 레이아웃
        search_sizer.Add(self.cancel_button, flag=wx.ALL, border=5)
        search_sizer.Add(self.search_input, proportion=2, flag=wx.ALL | wx.EXPAND, border=5)
        search_sizer.Add(self.search_button, flag=wx.ALL, border=5)

        # 검색 창을 아래쪽에 추가
        dialog_sizer.AddStretchSpacer()
        dialog_sizer.Add(search_sizer, flag=wx.EXPAND | wx.ALL, border=10)

        dialog_panel.SetSizer(dialog_sizer)
        

        # RoundedPanel을 메인 레이아웃에 추가
        main_sizer.Add(dialog_panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # 다음 버튼 추가
        self.next_button = wx.Button(panel, label="다음")
        self.next_button.Bind(wx.EVT_BUTTON, self.on_next_button)
        main_sizer.Add(self.next_button, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=20)

        panel.SetSizer(main_sizer)

        self.concepts = [
            "안녕하세요 무정적분입니다.",
            "제가 여기에 발표에 나온 캐릭터입니다.",
            "제가 만약 여러분들이 만난다면 발표가 준비됐다는 거죠"
        ]
        self.current_index = 0
        self.full_text_displayed = True

    def set_font_size(self):
        _, screen_height = self.GetSize()
        font_size = max(15, min(30, screen_height // 30))
        font = wx.Font(font_size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, faceName="Roboto Bold")
        self.text_display.SetFont(font)

    def on_resize(self, event):
        self.set_font_size()
        self.Layout()
        event.Skip()
  
    def on_cancel_button(self, event):
        """취소 버튼 클릭 처리"""
        # 텍스트 디스플레이 초기화
        self.text_display.SetLabel("이제 질문할 수 있습니다!")
        
        # 검색 및 취소 버튼 상태 초기화
        self.search_input.Enable()
        self.search_button.Enable()
        self.cancel_button.Disable()
        
        # 다음 버튼 비활성화
        self.next_button.Disable()

        # 리스트 진행 초기화
        self.concepts = []
        self.current_index = 0
        self.full_text_displayed = True

    def on_search_button(self, event):
        """검색 입력 처리 및 키워드 설정"""
        query = self.search_input.GetValue().strip()
        self.search_input.Clear()

        if not query:
            self.text_display.SetLabel("입력을 입력하세요.")
            return

        # 키워드를 설정하고, 성공 여부에 따라 처리
        if self.chatbot.set_keyword(query):
            # 검색 창과 버튼 비활성화
            self.search_input.Disable()
            self.search_button.Disable()
            self.cancel_button.Enable()  # 취소 버튼 활성화

            # 'self.concepts'를 'self.chatbot.get_next_response()'로 업데이트
            self.concepts = self.chatbot.responses[self.chatbot.current_keyword]
            self.current_index = 0  # 인덱스를 0으로 초기화

            # 첫 번째 응답 바로 출력
            first_response = self.chatbot.get_next_response()
            threading.Thread(target=self.type_text, args=(first_response,)).start()

            # 첫 번째 응답을 이미 출력했으므로 current_index를 1로 설정
            self.current_index = 1

            # "다음" 버튼 활성화 (다음 응답을 위해)
            self.next_button.Enable()
        else:
            self.text_display.SetLabel("알 수 없는 입력입니다. 다시 시도해주세요.")


    def show_followup_message(self):
        time.sleep(2)  # 2초 대기 후 메시지 표시
        wx.CallAfter(self.text_display.SetLabel, "또 검색할 내용이 있습니까?")



    def type_text(self, text):
        """텍스트를 한 글자씩 출력"""
        self.full_text_displayed = False
        self.text_display.SetValue("")  # 기존 텍스트 초기화
        for char in text:
            if self.full_text_displayed:
                wx.CallAfter(self.text_display.SetValue, text)
                return
            wx.CallAfter(self.text_display.AppendText, char)
            time.sleep(0.05)
        self.full_text_displayed = True

    def on_next_button(self, event):
        """다음 버튼 클릭 처리"""
        if not self.full_text_displayed:
            self.full_text_displayed = True
        elif self.current_index < len(self.concepts):
            # 현재 인덱스의 응답을 출력
            threading.Thread(target=self.type_text, args=(self.concepts[self.current_index],)).start()
            self.current_index += 1  # 다음 응답을 준비
        else:
            # 모든 대사가 끝난 후 검색창 활성화
            self.text_display.SetLabel("이제 질문할 수 있습니다!")
            self.search_input.Enable()
            self.search_button.Enable()
            self.cancel_button.Disable()
            self.next_button.Disable()



app = wx.App(False)
frame = GameFrame(None, title="게임 스타일 대화창", size=(400, 600))
frame.Show()
app.MainLoop()
