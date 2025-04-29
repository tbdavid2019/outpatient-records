import gradio as gr
import os
import requests
import logging
from dotenv import load_dotenv
from prompts import prompt_templates

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 讀取.env
load_dotenv()

# 檢查環境變數
def check_env_vars():
    required_vars = {
        "LLM_API_KEY": "大型語言模型 API 金鑰",
        "LLM_BASE_URL": "大型語言模型 API 網址",
        "LLM_MODEL": "大型語言模型名稱",
        "STT_API_KEY": "語音轉文字 API 金鑰",
        "STT_BASE_URL": "語音轉文字 API 網址",
        "STT_MODEL": "語音轉文字模型名稱"
    }
    
    missing_vars = []
    for var, desc in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"{var} ({desc})")
    
    if missing_vars:
        logging.error(f"缺少以下環境變數：{', '.join(missing_vars)}")
        return False
    return True

# LLM 設定
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")

# STT 設定
STT_API_KEY = os.getenv("STT_API_KEY")
STT_BASE_URL = os.getenv("STT_BASE_URL")
STT_MODEL = os.getenv("STT_MODEL")

# 場景選項 (注意：prompts.py 中有重複的鍵值，應該修正)
SCENARIOS = list(set(prompt_templates.keys()))  # 使用 set 去除重複項

# 語言選項
LANGUAGES = ["繁體中文", "英文", "日文"]


def transcribe_audio(audio_file):
    if audio_file is None:
        return ""
    
    # 檢查檔案是否存在
    if not os.path.exists(audio_file):
        logging.error(f"音頻檔案不存在: {audio_file}")
        return "(音頻檔案不存在)"
    
    # 檢查檔案大小
    if os.path.getsize(audio_file) == 0:
        logging.error("音頻檔案為空")
        return "(音頻檔案為空)"
    
    try:
        headers = {
            "Authorization": f"Bearer {STT_API_KEY}"
        }
        files = {
            'file': (os.path.basename(audio_file), open(audio_file, 'rb'), 'audio/mpeg')
        }
        data = {
            "model": STT_MODEL
        }
        
        logging.info(f"正在發送語音轉文字請求: {audio_file}")
        response = requests.post(f"{STT_BASE_URL}/transcriptions", headers=headers, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()['text']
            logging.info("語音轉文字成功")
            return result
        else:
            logging.error(f"語音轉文字失敗: {response.status_code} - {response.text}")
            return f"(語音轉文字失敗: {response.status_code})"
    except Exception as e:
        logging.error(f"語音轉文字過程中發生錯誤: {str(e)}")
        return f"(處理語音時發生錯誤: {str(e)})"
    finally:
        # 確保檔案被關閉
        if 'files' in locals() and 'file' in files:
            files['file'][1].close()


def call_llm(prompt):
    if not prompt:
        logging.error("提示詞為空")
        return "(提示詞不能為空)"
    
    try:
        headers = {
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        logging.info("正在發送 LLM 請求")
        response = requests.post(f"{LLM_BASE_URL}/chat/completions", headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()['choices'][0]['message']['content']
            logging.info("LLM 請求成功")
            return result
        else:
            logging.error(f"LLM 請求失敗: {response.status_code} - {response.text}")
            return f"(LLM錯誤: 狀態碼 {response.status_code})"
    except requests.exceptions.Timeout:
        logging.error("LLM 請求超時")
        return "(LLM請求超時，請稍後再試)"
    except requests.exceptions.ConnectionError:
        logging.error("LLM 連接錯誤")
        return "(無法連接到 LLM 服務，請檢查網絡連接)"
    except Exception as e:
        logging.error(f"LLM 請求過程中發生錯誤: {str(e)}")
        return f"(處理 LLM 請求時發生錯誤: {str(e)})"


def generate_prompt(scene, language, content):
    if not scene or scene not in prompt_templates:
        logging.warning(f"未知場景: {scene}，使用默認提示詞")
        return f"以下是描述內容：\n{content}"
    
    template = prompt_templates.get(scene)
    lang_phrase = {
        "繁體中文": "繁體中文",
        "英文": "English",
        "日文": "日本語"
    }.get(language, "繁體中文")
    
    logging.info(f"使用場景: {scene}, 語言: {language}")
    
    if template:
        return template.format(language=lang_phrase, content=content)
    else:
        return f"以下是描述內容：\n{content}"


def process(scene, language, text_input, audio_input):
    # 驗證輸入
    if not scene:
        return "請選擇場景。"
    
    if not language:
        return "請選擇語言。"
    
    final_text = text_input

    if not final_text and audio_input is not None:
        logging.info(f"使用語音輸入: {audio_input}")
        final_text = transcribe_audio(audio_input)

    if not final_text:
        return "請輸入文字或上傳語音。"

    logging.info(f"處理輸入文字，長度: {len(final_text)}")
    prompt = generate_prompt(scene, language, final_text)
    result = call_llm(prompt)
    return result


with gr.Blocks() as demo:
    gr.Markdown("# 🩺 醫療記錄格式產生器  -DAVID888-")
    
    gr.Markdown("""
    ## 📍 醫療記錄格式 × 場景選擇地圖
    
    | 場景 | 建議格式 | 為什麼用這個？ |
    |------|----------|----------------|
    | 🏥 一般門診看診 | SOAP | 主訴 → 檢查 → 判斷 → 計畫，結構清楚、標準化。 |
    | 🏥 住院病人每日進度 | SOAPIER / PIE | 需要記錄更多「介入行動」、「效果評估」，所以加上 IER 或強調 Problem。 |
    | 🚑 急診快速交班通報 | SBAR | 緊急情況下快速傳遞關鍵資訊：狀況、背景、判斷、建議。 |
    | 👩‍⚕️ 護理紀錄（特別是照護計畫） | SOAPIER / PIE / IER | 紀錄每次處置、病人反應、是否需要修正。 |
    | 🧠 心理諮商會談記錄 | DAP | 不強調客觀檢查，重在整理資料、評估與治療計畫。 |
    | 🩺 慢性病、長期追蹤患者 | SOAPIER / PIE | 每次看診都要追蹤療效、修正計劃，不能只記錄新症狀。 |
    | 📋 健檢簡單敘述、書面報告 | Narrative (自由記敘) | 沒有複雜病情，簡單描述觀察結果即可。 |
    | 📝 個案討論/多科會診簡報 | SOAP / SBAR 混用 | 有時要結構清楚，也要快速提出重點，視需求混搭。 |
    """)

    with gr.Row():
        scene = gr.Dropdown(choices=SCENARIOS, label="選擇場景", value=SCENARIOS[0] if SCENARIOS else None)
        language = gr.Dropdown(choices=LANGUAGES, label="選擇語言", value=LANGUAGES[0] if LANGUAGES else None)

    text_input = gr.Textbox(label="輸入病人狀況文字", placeholder="請輸入描述...", lines=4)
    audio_input = gr.Audio(label="或上傳語音檔案", type="filepath")

    submit_btn = gr.Button("產生記錄")

    result = gr.Textbox(label="結果（可複製）", lines=20)
    copy_btn = gr.Button("複製結果")

    # 提交按鈕事件
    submit_btn.click(
        process,
        inputs=[scene, language, text_input, audio_input],
        outputs=[result]
    )

    # 改進複製功能 - 使用標準方法
    def copy_text(text):
        # 在 Gradio 中，返回相同的文本會自動更新文本框
        # 這會觸發瀏覽器的選擇，使用戶可以手動複製
        return text
    
    copy_btn.click(
        copy_text,
        inputs=[result],
        outputs=[result]
    )


if __name__ == "__main__":
    # 檢查環境變數
    if check_env_vars():
        logging.info("啟動醫療記錄格式產生器應用")
        demo.launch()
    else:
        print("請設置所有必要的環境變數後再運行程式。")
        logging.error("由於缺少必要的環境變數，程式無法啟動")