from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# تخزين الرسائل في الذاكرة
messages = []

# صفحة عرض الرسائل
HTML_PAGE = '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🖥️ Server - لوحة التحكم</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, sans-serif; }
body {
    background: linear-gradient(135deg, #0f0f1e, #1a1a3e);
    color: #fff;
    min-height: 100vh;
    padding: 20px;
}
.container { max-width: 800px; margin: 0 auto; }
h1 {
    text-align: center;
    font-size: 32px;
    margin-bottom: 20px;
    background: linear-gradient(90deg, #00dcc8, #a064ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.status {
    background: rgba(0, 220, 200, 0.1);
    border: 1px solid rgba(0, 220, 200, 0.3);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 20px;
    text-align: center;
    color: #00dcc8;
    font-weight: bold;
}
.messages {
    background: rgba(30, 30, 55, 0.6);
    border-radius: 16px;
    padding: 20px;
    min-height: 400px;
    border: 1px solid rgba(100, 120, 200, 0.2);
}
.empty {
    text-align: center;
    color: #667;
    padding: 100px 20px;
    font-size: 18px;
}
.message {
    background: rgba(0, 220, 200, 0.08);
    border-right: 4px solid #00dcc8;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 12px;
    animation: slideIn 0.3s ease-out;
}
@keyframes slideIn {
    from { opacity: 0; transform: translateX(20px); }
    to { opacity: 1; transform: translateX(0); }
}
.msg-text { font-size: 17px; margin-bottom: 8px; }
.msg-info { font-size: 12px; color: #8892c0; }
.refresh-btn {
    width: 100%;
    padding: 14px;
    margin-top: 15px;
    background: linear-gradient(135deg, #00dcc8, #a064ff);
    color: #fff;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    font-family: inherit;
}
.refresh-btn:active { transform: scale(0.98); }
.counter {
    display: inline-block;
    background: linear-gradient(90deg, #00dcc8, #a064ff);
    color: #fff;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 14px;
    margin-right: 10px;
}
</style>
</head>
<body>
<div class="container">
    <h1>🖥️ لوحة تحكم السيرفر</h1>
    <div class="status">
        <span class="counter">{{ count }}</span>
        ✅ السيرفر شغال — في انتظار الرسائل
    </div>
    <div class="messages">
        {% if messages %}
            {% for msg in messages %}
            <div class="message">
                <div class="msg-text">📩 {{ msg.text }}</div>
                <div class="msg-info">🕐 {{ msg.time }}</div>
            </div>
            {% endfor %}
        {% else %}
            <div class="empty">
                📭 لا توجد رسائل بعد
                <br><br>
                <small>افتح رابط العميل وابعت رسالة</small>
            </div>
        {% endif %}
    </div>
    <button class="refresh-btn" onclick="location.reload()">
        🔄 تحديث الرسائل
    </button>
</div>

<script>
// تحديث تلقائي كل 3 ثواني
setTimeout(() => location.reload(), 3000);
</script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(
        HTML_PAGE,
        messages=messages[::-1],  # الأحدث أولاً
        count=len(messages)
    )

@app.route('/send', methods=['POST'])
def send_message():
    """استقبال رسالة من العميل"""
    data = request.get_json()
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({'error': 'الرسالة فاضية'}), 400
    
    messages.append({
        'text': text,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    return jsonify({
        'success': True,
        'message': 'تم استلام الرسالة ✅',
        'total': len(messages)
    })

@app.route('/api/messages', methods=['GET'])
def get_messages():
    """API لاسترجاع كل الرسائل"""
    return jsonify({
        'count': len(messages),
        'messages': messages
    })

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
