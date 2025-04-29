import gradio as gr
import os
import requests
from dotenv import load_dotenv
from prompts import prompt_templates

# 讀取.env
load_dotenv()

# LLM 設定
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")

# STT 設定
STT_API_KEY = os.getenv("STT_API_KEY")
STT_BASE_URL = os.getenv("STT_BASE_URL")
STT_MODEL = os.getenv("STT_MODEL")

# 場景選項
SCENARIOS = list(prompt_templates.keys())

# 語言選項
LANGUAGES = ["繁體中文", "英文", "日文"]


def transcribe_audio(audio_file):
    if audio_file is None:
        return ""

    headers = {
        "Authorization": f"Bearer {STT_API_KEY}"
    }
    files = {
        'file': (audio_file.name, audio_file, 'audio/mpeg')
    }
    data = {
        "model": STT_MODEL
    }
    response = requests.post(f"{STT_BASE_URL}/transcriptions", headers=headers, files=files, data=data)

    if response.status_code == 200:
        return response.json()['text']
    else:
        return "(語音轉文字失敗)"


def call_llm(prompt):
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(f"{LLM_BASE_URL}/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"(LLM錯誤: {response.text})"


def generate_prompt(scene, language, content):
    template = prompt_templates.get(scene)
    lang_phrase = {
        "繁體中文": "繁體中文",
        "英文": "English",
        "日文": "日本語"
    }.get(language, "繁體中文")

    if template:
        return template.format(language=lang_phrase, content=content)
    else:
        return f"以下是描述內容：\n{content}"


def process(scene, language, text_input, audio_input):
    final_text = text_input

    if not final_text and audio_input is not None:
        final_text = transcribe_audio(audio_input)

    if not final_text:
        return "請輸入文字或上傳語音。"

    prompt = generate_prompt(scene, language, final_text)
    result = call_llm(prompt)
    return result


with gr.Blocks() as demo:
    gr.Markdown("# 🩺 醫療記錄格式產生器")

    with gr.Row():
        scene = gr.Dropdown(choices=SCENARIOS, label="選擇場景")
        language = gr.Dropdown(choices=LANGUAGES, label="選擇語言")

    text_input = gr.Textbox(label="輸入病人狀況文字", placeholder="請輸入描述...", lines=4)
    audio_input = gr.Audio(label="或上傳語音檔案", type="file")

    submit_btn = gr.Button("產生記錄")

    result = gr.Textbox(label="結果（可複製）", lines=20)
    copy_btn = gr.Button("複製結果")

    submit_btn.click(
        process,
        inputs=[scene, language, text_input, audio_input],
        outputs=[result]
    )

    copy_btn.click(lambda x: x, inputs=[result], outputs=[result], api_name="copy")


if __name__ == "__main__":
    demo.launch()