prompt_templates = {
    "一般門診看診": '''
請根據以下病人描述內容，使用標準 SOAP 格式撰寫完整門診病歷。
請遵循以下規則：
- 每個欄位皆需顯示標題。
- 無資料時，請明確寫「未提供」或「未描述」等。
- 排版整齊，方便醫療人員閱讀。

Outpatient Record:

S (Subjective data):
- Chief Complaint:
- Description of Symptoms:
- Negative Symptoms:
- Past Illnesses:
- Medication Use:
- Family History:
- Allergies:
- Lifestyle Habits:

O (Objective data):
- Physical Examination:
- Laboratory Tests:
- Medical Images:

A (Assessment):
- Primary Diagnosis:
- Differential Diagnosis (if applicable):

P (Plan):
- Possible Examinations:
- Possible Medical Treatment:
- Follow-Up Instructions:

請以 {language} 撰寫。
以下是病人描述：
---
{content}
---
''',

    "住院病人每日進度": '''
請使用 SOAPIER 格式撰寫病患住院紀錄。
- 每項請依欄位明確列出內容。
- 無資料請寫「未提供」。
- 符合臨床醫院使用習慣。

Inpatient Record (SOAPIER):
S (Subjective):
O (Objective):
A (Assessment):
P (Plan):
I (Intervention):
E (Evaluation):
R (Revision):

請以 {language} 撰寫。
病人描述如下：
---
{content}
---
''',

    "急診快速交班通報": '''
請根據下列病人描述，撰寫急診交班摘要，使用 SBAR 結構。
即使資訊缺乏，也需列出各段並標明「未提供」。

Emergency Handoff Report:
S (Situation):
B (Background):
A (Assessment):
R (Recommendation):

請以 {language} 撰寫。
描述內容如下：
---
{content}
---
''',

    "護理紀錄（特別是照護計畫）": '''
請使用 SOAPIER 格式撰寫完整護理紀錄。
- 針對照護計畫、介入措施、反應與修正做詳盡記錄。
- 每段需標題明確。
- 無資料請標明未提供。

Nursing Note:
S (Subjective):
O (Objective):
A (Assessment):
P (Plan):
I (Intervention):
E (Evaluation):
R (Revision):

請以 {language} 撰寫。
以下是觀察紀錄或病患敘述：
---
{content}
---
''',

    "心理諮商會談記錄": '''
請使用 DAP 格式撰寫心理會談紀錄。
- 每段皆需標示標題，即使無資料也須說明。

Psychotherapy Note:
D (Data):
A (Assessment):
P (Plan):

請以 {language} 撰寫。
以下是會談內容摘要：
---
{content}
---
''',

    "慢性病、長期追蹤患者": '''
請使用 PIE 格式撰寫慢性病或長期照護記錄。
- 明確列出 Problem, Intervention, Evaluation。
- 無資料者請明確註記。
- 記錄重點應涵蓋追蹤期間內的變化、處置與成效。

Long-term Care Note (PIE):
P (Problem): 
I (Intervention): 
E (Evaluation): 

請以 {language} 撰寫。
以下是患者描述或觀察內容：
---
{content}
---
''',

    "健檢簡單敘述、書面報告": '''
請使用 Narrative（敘事）格式撰寫簡易健檢或常規健康報告。
- 需有開頭、觀察、結語。
- 如資料不詳，請明確說明。
- 報告須清楚易讀，方便個人或轉介醫療使用。

Health Report (Narrative):

請以 {language} 撰寫以下敘述：
---
{content}
---
''',

    "個案討論/多科會診簡報": '''
請以 SOAP 與 SBAR 混合格式撰寫個案摘要，供多科會診使用。
- 每段需清楚標題。
- 如無資料請註明未提供。
- 強調臨床重點、問題判斷、後續建議。

Case Summary:

S (Subjective): 
O (Objective): 
A (Assessment): 
P (Plan): 
R (Recommendation): 

請以 {language} 撰寫。
以下是個案描述：
---
{content}
---
'''
}