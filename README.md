#English
# 🎮 Dich Game By Tu - Real-time On-Screen Translation Assistant

![Version](https://img.shields.io/badge/version-v1.3-blue.svg)
![Python](https://img.shields.io/badge/python-3.x-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

> **Dich Game By Tu** is an open-source software that helps gamers translate in-game dialogues and subtitles on their PC screen in real-time. The application combines the power of **Tesseract OCR** for text recognition and **Deep Translator** for high-speed translation.

---

## ✨ Key Features

*  **Smart Text Recognition (OCR):** Scans and extracts text from any selected area on the screen with high accuracy.
*  **Cloud Dictionary:** Automatically synchronizes and downloads specialized game dictionaries from the GitHub Server.
*  **High-speed Translation:** Supports smooth auto-detect translation into Vietnamese (or your target language).
*  **Silent Update:** Automatically detects new versions, downloads, and installs in the background without interrupting the user.
*  **Minimalist Experience:** Transparent overlay interface. Quickly dismiss translation results with a single **Right-Click**.

---

## 🛠️ Developer Guide (Source Code Modification)

This project highly welcomes developers to download, tinker, and upgrade features.

### 1. Prerequisites
* **Python 3.x**
* **Tesseract-OCR:** Must be installed on your machine, or you can copy the `Tesseract-OCR` folder into the root directory of the source code.

### 2. Environment Setup
Open Terminal and run the following command to install required libraries:
 ` pip install requests Pillow pytesseract opencv-python numpy deep-translator `
3. Run the App
 ` python main.py ` 
4. Build Executable (EXE)
The project uses PyInstaller to package the code and Inno Setup to create the installer.
Standard PyInstaller command (Note: move the Tesseract-OCR folder out of the dist directory before running this command):
 ` pyinstaller --noconsole --onedir --add-data "Tu_Dien;Tu_Dien" --add-data "snipping_tool.py;." main.py ` 
 
 🤝 Contributing
Any contributions (Pull Requests) to optimize the image recognition algorithm (OpenCV), add new languages, or redesign the UI (Tkinter) are warmly welcomed!

Fork this repository.

Create a new Branch (git checkout -b feature/NewFeature).

Commit your changes (git commit -m 'Add XYZ feature').

Push to the Branch (git push origin feature/NewFeature).

Open a Pull Request.

📝 License
This project is distributed under the MIT License. You are free to copy, modify, and distribute.



---
#VietNamese
# 🎮 Dich Game By Tu - Trợ Lý Dịch Thuật Màn Hình Trực Tiếp

![Version](https://img.shields.io/badge/version-v1.3-blue.svg)
![Python](https://img.shields.io/badge/python-3.x-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

> **Dich Game By Tu** là một phần mềm mã nguồn mở giúp game thủ Việt hóa trực tiếp các đoạn hội thoại, phụ đề trên màn hình máy tính theo thời gian thực. Ứng dụng kết hợp sức mạnh của **Tesseract OCR** để nhận diện chữ và **Deep Translator** để dịch thuật siêu tốc.

---

##  Tính Năng Nổi Bật

*  **Nhận diện chữ thông minh (OCR):** Quét và bóc tách text từ bất kỳ khu vực nào trên màn hình với độ chính xác cao.
*  **Từ Điển Đám Mây:** Tự động đồng bộ và tải từ điển chuyên ngành cho từng game từ GitHub Server.
*  **Dịch thuật siêu tốc:** Hỗ trợ dịch tự động (Auto-detect) sang Tiếng Việt mượt mà.
*  **Cập Nhật Tàng Hình (Silent Update):** Tự động phát hiện phiên bản mới, tải và cài đặt ngầm 100% không làm phiền người dùng.
*  **Trải nghiệm tối giản:** Giao diện Overlay trong suốt, tắt nhanh kết quả dịch chỉ bằng một cú **Click Chuột Phải**.

---

## 🛠️ Hướng Dẫn Dành Cho Developer (Chỉnh Sửa Mã Nguồn)

Dự án này rất hoan nghênh các lập trình viên tải về, vọc vạch và nâng cấp tính năng.

### 1. Yêu cầu hệ thống (Prerequisites)
* **Python 3.x**
* **Tesseract-OCR:** Cần cài đặt sẵn trên máy hoặc copy thư mục `Tesseract-OCR` vào chung thư mục với code.

### 2. Cài đặt môi trường
Mở Terminal và chạy lệnh sau để cài đặt các thư viện cần thiết:
 ` pip install requests Pillow pytesseract opencv-python numpy deep-translator `

 3. Chạy thử phần mềm
 `  python main.py  `
4. Đóng gói phần mềm (Build EXE)
Dự án sử dụng PyInstaller để đóng gói code và Inno Setup để tạo bộ cài.
Lệnh PyInstaller chuẩn để đóng gói (lưu ý cất thư mục Tesseract-OCR ra ngoài thư mục dist trước khi chạy):
` pyinstaller --noconsole --onedir --add-data "Tu_Dien;Tu_Dien" --add-data "snipping_tool.py;." main.py `

🤝 Đóng Góp (Contributing)
Mọi đóng góp (Pull Request) để tối ưu hóa thuật toán nhận diện ảnh (OpenCV), thêm ngôn ngữ, hoặc thiết kế lại giao diện (Tkinter) đều được chào đón!

Fork dự án này.

Tạo một Branch mới (git checkout -b feature/TinhNangMoi).

Commit thay đổi của bạn (git commit -m 'Thêm tính năng XYZ').

Push lên Branch (git push origin feature/TinhNangMoi).

Mở một Pull Request.

📝 Giấy Phép (License)
Dự án được phân phối dưới giấy phép MIT License. Bạn có thể tự do sao chép, chỉnh sửa và phân phối.
