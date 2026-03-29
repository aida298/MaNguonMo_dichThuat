[Setup]
; --- THÔNG TIN PHẦN MỀM ---
AppName=Dich Game By Tu
AppVersion=1.3
DefaultDirName={autopf}\DichGameTu
DefaultGroupName=Dich Game By Tu
UninstallDisplayIcon={app}\main.exe
Compression=lzma
SolidCompression=yes

; --- ĐƯỜNG DẪN XUẤT FILE SETUP (Lưu ra Desktop cho dễ tìm) ---
OutputDir=E:\setup
OutputBaseFilename=Setup_DichGame_Tu_v1.3

[Tasks]
Name: "desktopicon"; Description: "Tao bieu tuong ngoai Desktop"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
; 1. File thực thi chính từ thư mục dist mới của Tu
Source: "E:\HOCode2\dist\main\main.exe"; DestDir: "{app}"; Flags: ignoreversion

; 2. Lấy toàn bộ "nội thất" bên trong (DLL, Tesseract, Tu_Dien, snipping_tool...)
; Lưu ý: Tu phải đảm bảo đã copy thư mục Tesseract-OCR vào trong dist\main rồi nhé!
Source: "E:\HOCode2\dist\main\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Tạo shortcut trong Start Menu và Desktop
Name: "{group}\Dich Game By Tu"; Filename: "{app}\main.exe"
Name: "{autodesktop}\Dich Game By Tu"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Run]
; Tự động chạy app sau khi cài xong
Filename: "{app}\main.exe"; Description: "Chay phan mem ngay bay gio"; Flags: nowait postinstall skipifsilent

[Dirs]
Name: "{app}"; Permissions: users-modify