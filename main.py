from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox

import pyperclip
import pyautogui
pyautogui.PAUSE = 0.5
import pygetwindow as gw

import random
# import socket
# pc_name = "LAPTOP-OR8N1RC3"
# pc_name = "DESKTOP-66QHPJP"

import time

##################################################
def add_image_files():
    """파일 추가"""
    image_list.delete(0, END)
    image_files = filedialog.askopenfilenames(
        title="이미지 파일을 선택하세요",
        filetypes=(("모든 파일", "*.*"), ("PNG 파일", "*.PNG"), ("JPG 파일", "*.JPG")),
        initialdir=r"C:\\") # 최초 경로 - C:\\
    # 사용자가 선택한 파일 목록
    for image_file in image_files:
        image_list.insert(END, image_file.replace("/", "\\"))


def del_image_files():
    """선택한 파일 삭제"""
    for index in reversed(image_list.curselection()):
        image_list.delete(index)


def activate_window(title):
    """윈도우 활성화"""
    w = gw.getWindowsWithTitle(title)[0]
    if w.isActive == False:
        w.activate()
    if w.isMaximized == False:
        w.maximize()
    w.restore()
    return w


def friend_filtering():
    """전송할 그룹 필터링"""
    w = activate_window("카카오톡")
    if screen_magnification_var.get() == 0:
        msgbox.showerror("에러", "화면 배율을 설정해 주세요\n\n[카카오톡 - 설정 - 화면 - 기본 - 화면 배율]")
        return
    elif screen_magnification_var.get() == 1:
        pyautogui.click(w.left + 30, w.top + 50) # 사람 아이콘
        pyautogui.hotkey('ctrl', 'f') # 돋보기 아이콘
        pyautogui.press('esc') # X 아이콘
        pyautogui.hotkey('ctrl', 'f') # 돋보기 아이콘
    elif screen_magnification_var.get() == 2:
        pyautogui.click(w.left + 38, w.top + 70) # 사람 아이콘
        pyautogui.hotkey('ctrl', 'f') # 돋보기 아이콘
        pyautogui.press('esc') # X 아이콘
        pyautogui.hotkey('ctrl', 'f') # 돋보기 아이콘
    
    filtering_keyword = filtering_entry.get()
    if filtering_keyword.strip() == "":
        msgbox.showerror("에러", "필터링 할 문자를 입력하세요\n\n예시)\nㄱ1홍길동, ㄱ1임꺽정 -> ㄱ1\n*이순신, *장보고 -> *")
        return
    else:
        pyperclip.copy(filtering_keyword)
        pyautogui.hotkey("ctrl", "v")


def init_starting_point():
    """전송 시작 위치 초기화"""
    if starting_point_entry.get().strip() == "":
        msgbox.showerror("에러", "메세지 전송 시작 위치를 입력하세요\n\n예시)\n처음부터 보내기: 1\n10번째 친구부터 보내기: 10")
        return
    else:
        pyautogui.press("down", int(starting_point_entry.get()) - 1)


def send_text():
    """텍스트 전송"""
    pyperclip.copy(text_message.get("1.0", END))
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    pyautogui.sleep(random.uniform(0.5, 1.0))


def send_image():
    """이미지 전송"""
    pyautogui.hotkey("ctrl", "t")
    pyautogui.press("enter")
    
    num_image = image_list.size()
    images = list(image_list.get(0, END))
    if num_image == 1:
        image = images[0]
        pyperclip.copy(image)
        pyautogui.hotkey("ctrl", "v")
    else:
        for image in images:
            file_name = '"' + image + '" '
            pyperclip.copy(file_name)
            pyautogui.hotkey("ctrl", "v")

    pyautogui.press("enter")
    pyautogui.press("enter")
    pyautogui.sleep(random.uniform(1.5, 2.0) * image_list.size())
    # pyautogui.press("esc")


def calculate_time(spend_time):
    unit_of_time = 60
    min_for_spend_time = spend_time // unit_of_time
    
    if min_for_spend_time < 1:
        return f"{spend_time}초"
    elif 1 <= min_for_spend_time < 60:
        sec_for_spend_time = spend_time % unit_of_time
        return f"{min_for_spend_time}분 {sec_for_spend_time}초"
    else:
        hour_for_spend_time = min_for_spend_time // unit_of_time
        min_for_spend_time = min_for_spend_time % unit_of_time
        sec_for_spend_time = spend_time % unit_of_time
        return f"{hour_for_spend_time}시간 {min_for_spend_time}분 {sec_for_spend_time}초"


def run():
    start_time = time.time()
    # if pc_name != socket.gethostname():
    #   msgbox.showerror("에러", "이 PC에서는 사용할 수 없습니다.\n-불법복제방지-")
    #   return
    if filtered_num_entry.get().strip() == "":
        msgbox.showerror("에러", "필터링 된 친구 수를 입력하세요\n\n카카오톡 - 좌측 상단 사람 아이콘 - 우축 상단 돋보기 아이콘 - 필터링 문자 입력 - 친구 수")
        return
    if sending_num_entry.get().strip == "":
        msgbox.showerror("에러", "메세지를 보낼 친구 수를 입력하세요")
        return

    len_text = len(text_message.get("1.0", END).strip())
    len_image = len(image_list.get(0, END))
    if len_text == 0 and len_image == 0:
        msgbox.showerror("에러", "텍스트를 입력하거나, 이미지를 선택하세요")
        return

    friend_filtering()
    init_starting_point()
    
    progress = 0
    p_var.set(progress)
    progressbar.update()
    
    n_filtered = int(filtered_num_entry.get())
    n_repeat = int(sending_num_entry.get())
    starting_point = int(starting_point_entry.get())
    n_sent = 0
    
    while progress < 100:
        try:
            pyautogui.press("enter")
            if len_text != 0 and len_image == 0:
                send_text()
            elif len_text == 0 and len_image != 0:
                send_image()
            elif len_text != 0 and len_image != 0:
                send_text()
                send_image()
            pyautogui.press("esc")
            
            try:
                w = gw.getWindowsWithTitle(filtering_entry.get())[0]
                pyautogui.sleep(random.uniform(2.5, 3.0) * image_list.size())
                pyautogui.press("enter")
            except Exception as e:
                pass
        
            n_sent += 1
            progress = n_sent / n_repeat * 100
            p_var.set(progress)
            progressbar.update()
                
            print("전송 요청 :", n_repeat)
            print("전송 완료 :", n_sent)
            print("전송 대기 :", n_repeat - n_sent)
            print("진행 상황 :", progress)
            print()
            pyautogui.press("down")
        
        except Exception as e:
            print(e)
            msgbox.showerror("에러", f"전송 요청 수 : {n_repeat}\n전송 완료 수 : {n_sent}\n재시작 위치 : {starting_point+n_sent}\n재전송 인원 수 : {n_repeat-n_sent}")
            return
        
    end_time = time.time()
    spend_time = calculate_time(int(end_time - start_time))
    
    msgbox.showinfo("알림", f"전송을 완료하였습니다.\n전송 요청 수 : {n_repeat}\n전송 완료 수 : {n_sent}\n전송 소요 시간 : {spend_time}")
    return
##################################################

root = Tk()
root.title("autoTalk")
root.geometry("+50+50")

# 화면 배율
# frame
screen_magnification_frame = LabelFrame(master=root, text="화면 배율")
screen_magnification_frame.pack(fill="x", padx=5, pady=5)
# radio box
screen_magnification_var = IntVar()
screen_100 = Radiobutton(master=screen_magnification_frame, text="100%", value=1, variable=screen_magnification_var)
screen_125 = Radiobutton(master=screen_magnification_frame, text="125%", value=2, variable=screen_magnification_var)
screen_100.pack(side="left", padx=30)
screen_125.pack(side="left", padx=30)

# 전송할 그룹 필터링
# frame
filtering_frame = LabelFrame(master=root, text="전송할 그룹 필터링")
filtering_frame.pack(fill="x", padx=5, pady=5)
# entry
filtering_entry = Entry(master=filtering_frame)
filtering_entry.pack(side="left", fill="both", expand=True)

# 필터링 된 인원 수
# frame
filtered_num_frame = LabelFrame(master=root, text="필터링 된 인원 수")
filtered_num_frame.pack(fill="x", padx=5, pady=5)
# entry
filtered_num_entry = Entry(master=filtered_num_frame)
filtered_num_entry.pack(side="left", fill="both", expand=True)

# 전송 시작 위치
# frame
starting_point_frame = LabelFrame(master=root, text="전송 시작 위치")
starting_point_frame.pack(fill="x", padx=5, pady=5)
# entry
starting_point_entry = Entry(master=starting_point_frame)
starting_point_entry.pack(side="left", fill="both", expand=True)

# 전송할 인원 수
# frame
sending_num_frame = LabelFrame(master=root, text="전송할 인원 수")
sending_num_frame.pack(fill="x", padx=5, pady=5)
# entry
sending_num_entry = Entry(master=sending_num_frame)
sending_num_entry.pack(side="left", fill="both", expand=True)

# 텍스트 메세지
# frame
text_message_frame = LabelFrame(master=root, text="텍스트 메세지 입력")
text_message_frame.pack(fill="x", padx=5, pady=5)
# scroll bar
scrollbar_1 = Scrollbar(master=text_message_frame)
scrollbar_1.pack(side="right", fill="y")
# input text
text_message = Text(master=text_message_frame, width=70, height=15, yscrollcommand=scrollbar_1)
text_message.pack(side="left", fill="both", expand=True)
scrollbar_1.config(command=text_message.yview)

# 이미지 메세지
# frame
image_message_frame = LabelFrame(master=root, text="전송할 이미지 선택")
image_message_frame.pack(fill="x", padx=5, pady=5)
# listbox
image_list = Listbox(master=image_message_frame, selectmode="extended", height=5)
image_list.pack(side="left", fill="both", expand=True)
# image selection button
find_image_btn = Button(master=image_message_frame, text="선택", width=7, command=add_image_files)
find_image_btn.pack(side="top", padx=5, pady=5)
# image deletion button
del_image_btn = Button(master=image_message_frame, text="삭제", width=7, command=del_image_files)
del_image_btn.pack(side="bottom", padx=5, pady=5)

# 진행 상황
# frame
progressbar_frame = LabelFrame(master=root, text="진행 상황")
progressbar_frame.pack(fill="x", padx=5, pady=5, ipady=5)
# progress bar
p_var = DoubleVar()
progressbar = ttk.Progressbar(master=progressbar_frame, maximum=100, variable=p_var)
progressbar.pack(fill="x", padx=5, pady=5)

# 실행
# frame
run_frame = Frame(master=root)
run_frame.pack(fill="x", padx=5, pady=5)
# close button
close_btn = Button(master=run_frame, text="종료", width=10, padx=5, pady=5, command=root.quit)
close_btn.pack(side="right", padx=5, pady=5)
# run button
run_btn = Button(master=run_frame, text="전송", width=10, padx=5, pady=5, command=run)
run_btn.pack(side="right", padx=5, pady=5)

root.mainloop()