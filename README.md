---
title: Outpatient Records
emoji: ⚡
colorFrom: purple
colorTo: pink
sdk: gradio
sdk_version: 6.2.0
app_file: app.py
pinned: false
short_description: 病歷
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

---



🩺 醫療記錄格式產生器 - DAVID888

本專案是一個基於 Gradio 的 Web 應用程式，協助醫師或護理師，將初步整理的病人狀況描述，自動轉換為標準化的醫療記錄格式（如 SOAP、SBAR、SOAPIER 等），支援文字與語音輸入，並可依場景選擇最適合的格式生成完整病歷。

⸻

✨ 功能特色
	•	📝 支援 8 種醫療場景（門診、住院、急診、護理、心理諮商等）
	•	🌏 多語言輸出（繁體中文、英文、日文）
	•	🎙️ 支援文字輸入與語音上傳（自動轉換文字）
	•	🤖 自訂 LLM (大型語言模型) 與 STT (語音轉文字模型) API
	•	📋 產出格式化、可直接複製的醫療記錄內容
	•	🔒 詳細錯誤處理與日誌記錄，方便除錯

⸻

🚀 快速開始

1. 安裝依賴套件

pip install -r requirements.txt

2. 設置環境變數 .env

建立一個 .env 檔案，填入下列參數：

# LLM 相關
LLM_API_KEY=your-llm-api-key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o

# 語音轉文字 (STT) 相關
STT_API_KEY=your-stt-api-key
STT_BASE_URL=https://api.openai.com/v1/audio
STT_MODEL=whisper-1

預設對接 OpenAI，如需自訂其他伺服器，修改 Base URL 與 Model 即可。

⸻

3. 啟動應用

python app.py

成功啟動後，Gradio 介面將於本地端開啟！

⸻

📍 支援場景與對應格式

場景	建議格式
🏥 一般門診看診	SOAP
🏥 住院病人每日進度	SOAPIER / PIE
🚑 急診快速交班通報	SBAR
👩‍⚕️ 護理紀錄（照護計畫）	SOAPIER / PIE / IER
🧠 心理諮商會談記錄	DAP
🩺 慢性病、長期追蹤患者	SOAPIER / PIE
📋 健檢簡單敘述、書面報告	Narrative
📝 個案討論/多科會診簡報	SOAP / SBAR 混合



⸻

⚙️ 系統架構
	•	Gradio — 用於建立網頁介面
	•	Requests — 用於呼叫 LLM 與 STT API
	•	dotenv — 管理 API 金鑰與設定
	•	Logging — 全面錯誤追蹤與日誌記錄

⸻

🛠 注意事項
	•	請確保 .env 內所有變數正確無誤，否則系統將無法啟動。
	•	音檔上傳支援 .wav, .mp3 格式，且須為有效檔案。
	•	目前僅支援單一語音檔案上傳，未支援批次轉換。
	•	API 超時或錯誤將提供友善提示，請依訊息排除錯誤。

⸻

📄 授權

本專案由 David888 製作，僅供學術研究與個人使用。
如需商業應用，請事先取得授權。