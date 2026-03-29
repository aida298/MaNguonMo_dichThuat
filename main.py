import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
import json
from PIL import ImageGrab
import pytesseract
import snipping_tool
import threading
import cv2
import numpy as np
import re
import ctypes
import sys
import time
import subprocess
from deep_translator import GoogleTranslator

# === ĐỒNG BỘ TỌA ĐỘ MÀN HÌNH CAO (2K/4K) ===
try:
    ctypes.windll.user32.SetProcessDPIAware()
except:
    pass

# ================= CẤU HÌNH HỆ THỐNG TỰ ĐỘNG =================
def get_tesseract_path():
    # Ưu tiên tìm Tesseract ngay trong thư mục phần mềm (Dành cho bộ cài Portable)
    if getattr(sys, 'frozen', False):
        local_tess = os.path.join(os.path.dirname(sys.executable), "Tesseract-OCR", "tesseract.exe")
    else:
        local_tess = os.path.join(os.path.dirname(__file__), "Tesseract-OCR", "tesseract.exe")
    
    if os.path.exists(local_tess):
        return local_tess
    
    # Nếu không thấy, dùng đường dẫn mặc định ở ổ C
    return r'C:\Program Files\Tesseract-OCR\tesseract.exe'

pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()
fast_translator = GoogleTranslator(source='auto', target='vi')

# Tạo thư mục từ điển nếu chưa có
if not os.path.exists("Tu_Dien"):
    os.makedirs("Tu_Dien")

CLOUD_INDEX_URL = "https://raw.githubusercontent.com/aida298/PhanMemDich-Cloud/refs/heads/main/danh_sach_game.json?v=11"
CLOUD_DICT_BASE_URL = "https://raw.githubusercontent.com/aida298/PhanMemDich-Cloud/refs/heads/main/Tu_Dien/"
# =====================================================

# --- ĐÃ NÂNG CẤP LÊN BẢN 1.3 ĐỂ LÀM TÍNH NĂNG CÀI NGẦM ---
VERSION_CURRENT = "1.3" 
VERSION_URL = "https://raw.githubusercontent.com/aida298/PhanMemDich-Cloud/refs/heads/main/version.json"

class CloudDictionaryManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"Cập nhật Từ điển Game v{VERSION_CURRENT} - By Tu")
        self.root.geometry("450x330") 
        self.root.eval('tk::PlaceWindow . center')
        
        tk.Label(self.root, text="BỘ CÀI DỊCH GAME THÔNG MINH", font=("Arial", 12, "bold"), fg="blue").pack(pady=10)
        
        # --- Dòng trạng thái kiểm tra cập nhật ---
        self.lbl_status = tk.Label(self.root, text="Đang kiểm tra phiên bản...", fg="gray", font=("Arial", 9, "italic"))
        self.lbl_status.pack()
        
        tk.Label(self.root, text="Chọn game bạn đang chơi:", font=("Arial", 10)).pack(pady=5)
        
        self.game_catalog = {} 
        self.combo = ttk.Combobox(self.root, state="readonly", width=45)
        self.combo.pack(pady=10)
        
        self.btn_download = tk.Button(self.root, text="Tải Dữ Liệu & Bắt Đầu", bg="#28a745", fg="white", 
                                   font=("Arial", 10, "bold"), command=self.download_and_start, width=25, height=2)
        self.btn_download.pack(pady=10)
        
        self.btn_skip = tk.Button(self.root, text="Dịch không dùng từ điển (Dịch chay)", command=self.root.destroy)
        self.btn_skip.pack()
        
        # Tự động chạy kiểm tra cập nhật và lấy danh sách game
        threading.Thread(target=self.check_update, daemon=True).start()
        self.fetch_catalog()

    def check_update(self):
        """Kiểm tra bản cập nhật mới từ GitHub"""
        try:
            # Ép GitHub trả về file mới nhất, tránh bị Cache
            r = requests.get(f"{VERSION_URL}?t={int(time.time())}", timeout=5)
            data = r.json()
            latest_version = data['version']
            
            if latest_version > VERSION_CURRENT:
                self.lbl_status.config(text=f"Phát hiện bản mới: v{latest_version}!", fg="red", font=("Arial", 9, "bold"))
                msg = f"Có bản cập nhật mới v{latest_version}!\n\nChi tiết: {data['note']}\n\nPhần mềm sẽ tự động tải và cài đặt. Bạn có đồng ý không?"
                
                if messagebox.askyesno("Cập nhật Tự động", msg):
                    # Khởi chạy luồng tải ngầm
                    threading.Thread(target=self.perform_silent_update, args=(data['link'],), daemon=True).start()
            else:
                self.lbl_status.config(text="Bạn đang dùng phiên bản mới nhất.", fg="green")
        except:
            self.lbl_status.config(text="Không thể kiểm tra cập nhật (Lỗi mạng).", fg="orange")

    def perform_silent_update(self, download_url):
        """Hàm tự động tải và cài đặt tàng hình"""
        self.btn_download.config(state="disabled")
        self.btn_skip.config(state="disabled")
        self.lbl_status.config(text="Đang tải bản cập nhật... Vui lòng đợi!", fg="blue")
        self.root.update()
        
        try:
            temp_dir = os.environ.get('TEMP', '.')
            installer_path = os.path.join(temp_dir, "Update_DichGame_Tu.exe")
            
            response = requests.get(download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(installer_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192): 
                    f.write(chunk)
                    
            self.lbl_status.config(text="Tải xong! Đang tự động cài đặt...", fg="green")
            self.root.update()
            
            # Kích hoạt bộ cài Inno Setup chạy ngầm
            subprocess.Popen([installer_path, '/VERYSILENT', '/SUPPRESSMSGBOXES'])
            
            # Đóng phần mềm ngay lập tức để bộ cài ghi đè file
            os._exit(0)
            
        except Exception as e:
            self.lbl_status.config(text="Lỗi khi tải cập nhật. Vui lòng thử lại sau!", fg="red")
            self.btn_download.config(state="normal")
            self.btn_skip.config(state="normal")

    def fetch_catalog(self):
        """Lấy danh sách game từ GitHub"""
        try:
            response = requests.get(CLOUD_INDEX_URL, timeout=5)
            self.game_catalog = response.json()
            self.combo['values'] = list(self.game_catalog.keys())
            if self.combo['values']: self.combo.current(0)
        except:
            self.combo.set("Lỗi kết nối Server! Vui lòng kiểm tra mạng.")

    def download_and_start(self):
        """Tải file từ điển của game đã chọn"""
        selected = self.combo.get()
        if selected in self.game_catalog:
            file_name = self.game_catalog[selected]
            try:
                r = requests.get(CLOUD_DICT_BASE_URL + file_name, timeout=5)
                with open(os.path.join("Tu_Dien", file_name), 'w', encoding='utf-8') as f:
                    json.dump(r.json(), f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Thành công", f"Đã chuẩn bị xong từ điển cho {selected}!")
                self.root.destroy()
            except:
                messagebox.showerror("Lỗi", "Không thể tải dữ liệu từ điển.")

class OverlayTranslator:
    def __init__(self, root, coords):
        self.root = root
        self.coords = coords 
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True, "-transparentcolor", "black")
        self.root.config(bg='black')
        
        x, y, w, h = self.coords
        self.root.geometry(f"{w}x120+{x}+{y + h + 10}") 
        
        self.canvas = tk.Canvas(self.root, bg='black', highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.text_id = self.canvas.create_text(
            w // 2, 60, text="", 
            fill="#B8860B", font=("Arial", 18, "bold"), 
            width=w, justify="center"
        )
        
        self.canvas.bind("<ButtonPress-1>", self.start_drag) 
        self.canvas.bind("<B1-Motion>", self.do_drag)        
        
        # --- LỆNH TẮT BẰNG CHUỘT PHẢI ---
        self.canvas.bind("<Button-3>", lambda e: self.on_exit())
        self.root.bind("<Button-3>", lambda e: self.on_exit())

        self.last_text = ""
        self.is_scanning = False 
        self.current_dictionary = {} 
        self.current_game_name = ""
        self.running = True 

        self.scan_loop()

    def start_drag(self, event):
        self.drag_start_x = event.x; self.drag_start_y = event.y
        
    def do_drag(self, event):
        x = self.root.winfo_x() - self.drag_start_x + event.x
        y = self.root.winfo_y() - self.drag_start_y + event.y
        self.root.geometry(f"+{x}+{y}")

    def on_exit(self):
        """Hàm xử lý khi thoát ứng dụng sạch sẽ"""
        print("-> Đang đóng ứng dụng...")
        self.running = False
        self.root.after(0, self.root.destroy)

    def auto_detect_game(self):
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
            window_title = buff.value.lower()
            
            for filename in os.listdir("Tu_Dien"):
                if filename.endswith(".json"):
                    game_key = filename.replace(".json", "").lower()
                    if game_key in window_title and self.current_game_name != game_key:
                        self.current_dictionary = {}
                        self.current_game_name = game_key
                        with open(os.path.join("Tu_Dien", filename), 'r', encoding='utf-8') as f:
                            self.current_dictionary = json.load(f)
                        print(f"-> Chế độ Game: {game_key.upper()}")
                        return
        except: pass

    def translate_engine(self, text):
        if not text: return ""
        temp = text
        sorted_keys = sorted(self.current_dictionary.keys(), key=len, reverse=True)
        for i, eng in enumerate(sorted_keys):
            temp = re.sub(fr'\b{eng}\b', f' CODE{i} ', temp, flags=re.IGNORECASE)
        try:
            result = fast_translator.translate(temp)
            for i, eng in enumerate(sorted_keys):
                result = result.replace(f'CODE{i}', self.current_dictionary[eng]).replace(f'code{i}', self.current_dictionary[eng])
            return result
        except: return ""

    def update_ui(self, text):
        if not self.running: return
        self.canvas.delete("all")
        if text:
            w = self.root.winfo_width()
            self.canvas.create_text(w // 2, 60, text=text, fill="#B8860B", font=("Arial", 18, "bold"), width=w, justify="center")
        self.is_scanning = False

    def scan_background_task(self):
        if not self.running: return
        try:
            self.auto_detect_game()
            x, y, w, h = self.coords
            img = ImageGrab.grab(bbox=(x, y, x+w, y+h), all_screens=True)
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            resized = cv2.resize(img_cv, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            denoised = cv2.bilateralFilter(gray, 9, 75, 75)
            _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            data = pytesseract.image_to_data(thresh, lang='eng', config='--oem 3 --psm 6', output_type=pytesseract.Output.DICT)
            
            valid_words = []
            for i in range(len(data['text'])):
                word = data['text'][i].strip()
                if int(data['conf'][i]) > 65 and len(word) >= 1:
                    valid_words.append(word)
            
            raw_text = " ".join(valid_words).strip()
            clean_text = re.sub(r'[^a-zA-Z0-9\s.,!?\'-]', '', raw_text).strip()

            is_valid = False
            if clean_text and ' ' in clean_text:
                letters_only = re.sub(r'[^a-zA-Z]', '', clean_text)
                if len(letters_only) > len(clean_text) * 0.7:
                    is_valid = True

            if is_valid and clean_text != self.last_text:
                self.last_text = clean_text
                translated = self.translate_engine(clean_text)
                if self.running:
                    self.root.after(0, self.update_ui, translated)
            elif not is_valid:
                if self.running:
                    self.root.after(0, lambda: self.canvas.delete("all"))
                self.last_text = "" 
        except: pass
        finally: self.is_scanning = False

    def scan_loop(self):
        if self.running and not self.is_scanning:
            self.is_scanning = True
            threading.Thread(target=self.scan_background_task, daemon=True).start()
        
        if self.running:
            self.root.after(150, self.scan_loop)

def main():
    manager = CloudDictionaryManager()
    manager.root.mainloop()
    
    print("\n1. Kéo chuột khoanh vùng phụ đề...")
    coords = snipping_tool.get_selection_area()
    
    if coords and coords[2] > 10 and coords[3] > 10:
        root = tk.Tk()
        app = OverlayTranslator(root, coords)
        
        def on_closing():
            app.on_exit()
            
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()

if __name__ == '__main__':
    main()