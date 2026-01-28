from flask import Flask, render_template, request, jsonify, send_file
import os
import time
import json
from datetime import datetime
from io import StringIO

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

# 开发期彻底禁用 static 缓存
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

# 数据存储目录
DATA_DIR = os.path.join(os.path.dirname(__file__), 'records')
os.makedirs(DATA_DIR, exist_ok=True)

def get_record_file(date_str):
    """获取某个日期的记录文件路径"""
    return os.path.join(DATA_DIR, f"{date_str}.json")

def load_record(date_str):
    """加载某个日期的记录"""
    file_path = get_record_file(date_str)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'date': date_str,
        'keywords': [],
        'today_done': '',
        'tomorrow_plan': [],
        'insights': '',
        'todos': [],
        'focus_sessions': []
    }

def save_record(date_str, data):
    """保存某个日期的记录"""
    file_path = get_record_file(date_str)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template("index.html", v=int(time.time()))


@app.route("/records")
def records_page():
    """渲染独立的记录页面（原主页上的详细记录功能已迁移到此处）"""
    return render_template("records.html", v=int(time.time()))


@app.route("/api/heatmap", methods=['GET'])
def heatmap_api():
    """返回已有记录文件的日期计数，供前端绘制打卡热图"""
    counts = {}
    try:
        for fname in os.listdir(DATA_DIR):
            if not fname.endswith('.json'):
                continue
            date_str = fname[:-5]
            counts[date_str] = counts.get(date_str, 0) + 1
    except Exception:
        pass
    return jsonify(counts)

@app.route("/api/record/<date_str>", methods=['GET'])
def get_record(date_str):
    """获取某个日期的记录"""
    record = load_record(date_str)
    return jsonify(record)

@app.route("/api/record/<date_str>", methods=['POST'])
def save_record_api(date_str):
    """保存某个日期的记录"""
    data = request.get_json()
    save_record(date_str, data)
    return jsonify({'status': 'success'})

@app.route("/api/export/<date_str>", methods=['GET'])
def export_record(date_str):
    """导出某个日期的记录为纯文本"""
    record = load_record(date_str)
    
    text_content = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 每日记录 - {record['date']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    if record.get('keywords'):
        text_content += f"🏷️  关键词: {', '.join(record['keywords'])}\n\n"
    
    text_content += f"""✅ 今天做了什么:
{record.get('today_done', '')}

📋 明天打算做:
"""
    for i, plan in enumerate(record.get('tomorrow_plan', []), 1):
        text_content += f"  {i}. {plan}\n"
    
    if record.get('insights'):
        text_content += f"\n💭 感悟:\n{record['insights']}\n"
    
    if record.get('focus_sessions'):
        total_time = sum(s.get('duration', 0) for s in record['focus_sessions'])
        text_content += f"\n⏱️  今日专注时长: {total_time}分钟\n"
        text_content += "📊 专注记录:\n"
        for session in record['focus_sessions']:
            text_content += f"  • {session.get('duration')}分钟 - {session.get('task', '任务')}\n"
    
    text_content += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    output = StringIO()
    output.write(text_content)
    output.seek(0)
    
    return send_file(
        StringIO(text_content),
        mimetype='text/plain; charset=utf-8',
        as_attachment=True,
        download_name=f"record_{date_str}.txt"
    )

if __name__ == "__main__":
    print("🔥 Flask 正在启动，用的是这个 app.py")
    print("🔥 当前绝对路径：", os.path.abspath(__file__))
    print("🔥 TEMPLATE DIR:", app.template_folder)
    print("🔥 STATIC DIR:", app.static_folder)
    print("🔥 数据存储目录：", DATA_DIR)
    app.run(debug=True, use_reloader=False)
