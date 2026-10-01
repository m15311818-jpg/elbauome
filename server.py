import socket
import mss
import io
from PIL import Image

HOST = '0.0.0.0'
PORT = 9999

def send_screen():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        
        # اطبع عنوان IP
        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
        except:
            local_ip = '127.0.0.1'
        
        print('=' * 50)
        print('✅ Server شغال')
        print(f'📡 IP: {local_ip}')
        print(f'🔌 Port: {PORT}')
        print('=' * 50)
        print('⏳ في انتظار الاتصال...')
        print('=' * 50)
        
        conn, addr = s.accept()
        print(f'🎉 جهاز اتصل: {addr}')
        
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            while True:
                try:
                    screenshot = sct.grab(monitor)
                    img = Image.frombytes(
                        'RGB',
                        screenshot.size,
                        screenshot.bgra,
                        'raw', 'BGRX'
                    )
                    
                    # تصغير عشان السرعة
                    img = img.resize((img.width // 2, img.height // 2))
                    
                    buffer = io.BytesIO()
                    img.save(buffer, format='JPEG', quality=50)
                    data = buffer.getvalue()
                    
                    conn.sendall(len(data).to_bytes(4, 'big'))
                    conn.sendall(data)
                except Exception as e:
                    print(f'❌ خطأ: {e}')
                    break

if __name__ == '__main__':
    send_screen()
