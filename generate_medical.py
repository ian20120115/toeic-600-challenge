import os
import json
import random

# Medical Theme Template
TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medical English - {title}</title>
    <style>
        /* Medical Theme Variables */
        :root {{
            --bg-color: #fcfdfe;   /* Clean White */
            --card-bg: #ffffff;    /* White */
            --text-main: #2c3e50;  /* Dark Blue Grey */
            --text-sub: #7f8c8d;   /* Grey */
            --accent: #e74c3c;     /* Medical Red */
            --accent-glow: #ff7675; 
            --secondary: #3498db;  /* Blue */
            --font-main: 'Segoe UI', 'Roboto', sans-serif;
            --font-code: 'Consolas', 'Monaco', monospace;
        }}

        body {{ 
            font-family: var(--font-main); 
            background-color: var(--bg-color); 
            /* Cross pattern */
            background-image: linear-gradient(#e6f2fa 1px, transparent 1px), linear-gradient(90deg, #e6f2fa 1px, transparent 1px);
            background-size: 40px 40px;
            margin: 0; padding: 20px; 
            color: var(--text-main); 
            min-height: 100vh;
        }}
        
        .container {{ 
            max-width: 800px; margin: 0 auto; 
            background: var(--card-bg); 
            padding: 30px; 
            border-radius: 12px; 
            box-shadow: 0 4px 20px rgba(231, 76, 60, 0.1); 
            border: 1px solid #eee;
        }}

        h1 {{ 
            text-align: center; color: var(--accent); 
            font-family: var(--font-main);
            text-transform: uppercase;
            letter-spacing: 2px;
            border-bottom: 2px solid var(--accent);
            padding-bottom: 10px;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}
        
        .nav {{ display: flex; justify-content: center; gap: 15px; margin-bottom: 30px; flex-wrap: wrap; }}
        .btn {{ 
            padding: 10px 25px; border: 1px solid var(--accent); background: transparent;
            color: var(--accent); border-radius: 30px;
            cursor: pointer; font-size: 16px; transition: 0.3s; font-weight: bold; 
        }}
        
        .btn:hover, .btn-active {{ 
            background: var(--accent); color: white; 
            box-shadow: 0 4px 10px rgba(231, 76, 60, 0.3);
        }}

        /* Learning Mode Cards */
        .word-card {{ 
            border-left: 4px solid var(--accent); 
            background: #fff; 
            padding: 20px; margin-bottom: 20px; 
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }}
        .word-card:hover {{ transform: translateY(-2px); }}
        
        .word-header {{ display: flex; align-items: center; gap: 15px; margin-bottom: 10px; flex-wrap: wrap; }}
        .english-word {{ 
            font-size: 24px; font-weight: bold; color: var(--text-main); 
        }}
        .speak-btn {{ 
            background: #ecf0f1; border: none; 
            border-radius: 50%; width: 32px; height: 32px; color: var(--text-main);
            cursor: pointer; display: flex; align-items: center; justify-content: center; transition: 0.2s; 
        }}
        .speak-btn:hover {{ background: var(--secondary); color: white; }}
        .meaning {{ color: var(--accent); font-weight: bold; font-size: 20px; }}
        
        .sentence-box {{ margin-top: 10px; padding-top: 10px; border-top: 1px dashed #eee; }}
        .sentence {{ font-style: italic; color: #555; font-size: 1.1em; margin-bottom: 4px; }}
        .sentence-zh {{ color: var(--text-sub); font-size: 0.95em; }}

        /* Quiz Mode */
        #quiz-section {{ display: none; text-align: center; }}
        .question-word {{ 
            font-size: 32px; font-weight: bold; margin-bottom: 30px; 
            color: var(--accent);
        }}
        .options-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
        .option-btn {{ 
            background: #fdfdfd; border: 1px solid #ddd; color: var(--text-main);
            padding: 15px; border-radius: 8px; cursor: pointer; font-size: 16px; transition: 0.2s; 
            font-weight: bold;
        }}
        .option-btn:hover {{ background-color: #fafafa; border-color: var(--accent); }}
        .option-btn:disabled {{ opacity: 0.6; cursor: not-allowed; }}
        
        .result-message {{ font-size: 22px; font-weight: bold; margin-top: 25px; padding: 15px; border-radius: 4px; }}
        .correct {{ color: #27ae60; background: #eafaf1; border: 1px solid #d5f5e3; }}
        .wrong {{ color: #c0392b; background: #fadbd8; border: 1px solid #f5b7b1; }}
        .score-board {{ font-size: 28px; color: var(--accent); margin-top: 30px; }}
    </style>
</head>
<body>

<div class="container">
    <h1>🏥 {title}</h1>
    
    <div class="nav">
        <a href="index.html" class="btn">🏠 Home</a>
        <button class="btn btn-active" onclick="showSection('learn')">📖 Learn</button>
        <button class="btn" onclick="startQuiz()">📝 Quiz</button>
    </div>

    <div id="learn-section"></div>

    <div id="quiz-section">
        <div id="quiz-container">
            <div class="question-word" id="q-word">Word</div>
            <div class="options-grid" id="options-area"></div>
            <div id="result-msg"></div>
        </div>
        <div id="final-score" style="display:none;" class="score-board"></div>
        <button id="restart-btn" class="btn" style="display:none; margin-top:20px;" onclick="startQuiz()">🔄 Retry Quiz</button>
    </div>
</div>

<script>
    const wordsDB = {json_data};

    function initLearn() {{
        const container = document.getElementById('learn-section');
        container.innerHTML = '';
        wordsDB.forEach((item, index) => {{
            const card = document.createElement('div');
            card.className = 'word-card';
            card.innerHTML = `
                <div class="word-header">
                    <span class="english-word">${{item.en}}</span>
                    <button class="speak-btn" onclick="speak('${{item.en.replace(/'/g, "\\'") }}')" title="Pronounce">🔊</button>
                    <span class="meaning">${{item.zh}}</span>
                </div>
                <div class="sentence-box">
                    <div class="sentence">"${{item.sent}}"
                         <button class="speak-btn" style="width:24px; height:24px; font-size:12px; display:inline-flex; vertical-align:middle; margin-left:5px;" onclick="speak(wordsDB[${{index}}].sent.replace(/'/g, '\\\\\\''))" title="Pronounce Sentence">🔊</button>
                    </div>
                    <div class="sentence-zh">${{item.sentZh}}</div>
                </div>
            `;
            container.appendChild(card);
        }});
    }}

    function speak(text) {{
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US'; 
        window.speechSynthesis.speak(utterance);
    }}

    function showSection(section) {{
        document.getElementById('learn-section').style.display = section === 'learn' ? 'block' : 'none';
        document.getElementById('quiz-section').style.display = section === 'quiz' ? 'block' : 'none';
        
        // Reset button states
        const btns = document.querySelectorAll('.nav .btn');
        btns[1].classList.toggle('btn-active', section === 'learn');
        btns[2].classList.toggle('btn-active', section === 'quiz');
    }}

    let currentQuestion = 0;
    let score = 0;
    let quizList = [];
    let wrongAnswers = [];

    function startQuiz() {{
        showSection('quiz');
        currentQuestion = 0;
        score = 0;
        wrongAnswers = [];
        document.getElementById('final-score').style.display = 'none';
        document.getElementById('restart-btn').style.display = 'none';
        document.getElementById('quiz-container').style.display = 'block';
        quizList = [...wordsDB].sort(() => 0.5 - Math.random());
        loadQuestion();
    }}

    function loadQuestion() {{
        if (currentQuestion >= quizList.length) {{
            endQuiz();
            return;
        }}
        const currentWord = quizList[currentQuestion];
        document.getElementById('q-word').textContent = currentWord.en;
        document.getElementById('result-msg').className = '';
        document.getElementById('result-msg').innerHTML = '';

        let options = [currentWord.zh];
        while (options.length < 4) {{
            const randomWord = wordsDB[Math.floor(Math.random() * wordsDB.length)];
            if (!options.includes(randomWord.zh)) options.push(randomWord.zh);
        }}
        options.sort(() => 0.5 - Math.random());

        const optionsArea = document.getElementById('options-area');
        optionsArea.innerHTML = '';
        options.forEach(opt => {{
            const btn = document.createElement('button');
            btn.className = 'option-btn';
            btn.textContent = opt;
            btn.onclick = () => checkAnswer(opt, currentWord.zh);
            optionsArea.appendChild(btn);
        }});
    }}

    function checkAnswer(selected, correct) {{
        const resultDiv = document.getElementById('result-msg');
        document.querySelectorAll('.option-btn').forEach(b => b.disabled = true);
        if (selected === correct) {{
            score++;
            resultDiv.textContent = "✅ Correct!";
            resultDiv.className = "result-message correct";
        }} else {{
            resultDiv.textContent = `❌ Incorrect! Answer: ${{correct}}`;
            resultDiv.className = "result-message wrong";
            wrongAnswers.push({{...quizList[currentQuestion], selected: selected}});
        }}
        setTimeout(() => {{
            currentQuestion++;
            loadQuestion();
        }}, 1500);
    }}

    function endQuiz() {{
        document.getElementById('quiz-container').style.display = 'none';
        const scoreBoard = document.getElementById('final-score');
        scoreBoard.style.display = 'block';
        let report = `Quiz Complete!<br>Score: ${{score}} / ${{wordsDB.length}}`;
        if (wrongAnswers.length > 0) {{
            report += '<div style="margin-top:20px; text-align:left; background:#fff; padding:15px; border-radius:8px; border:1px solid #ffeba7; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">';
            report += '<h3 style="color:#e74c3c; margin-top:0;">Review Needed:</h3><ul style="padding-left:20px; color:#555;">';
            wrongAnswers.forEach(w => {{
                report += `<li style="margin-bottom:5px;"><strong>${{w.en}}</strong>: <span style="color:#27ae60;">${{w.zh}}</span> <span style="color:#999; font-size:0.9em;">(You chose: ${{w.selected}})</span></li>`;
            }});
            report += '</ul></div>';
        }}
        scoreBoard.innerHTML = report;
        document.getElementById('restart-btn').style.display = 'inline-block';
    }}

    initLearn();
</script>

<div style="text-align: center; margin-top: 40px; margin-bottom: 20px;">
    <button onclick="markComplete()" style="padding: 15px 30px; background: #27ae60; color: white; border: none; border-radius: 50px; font-size: 18px; cursor: pointer; font-weight: bold; box-shadow: 0 4px 15px rgba(39,174,96,0.3); transition: 0.3s;">✅ Mark Complete</button>
</div>

<script>
    function markComplete() {{
        const pageId = window.location.pathname.split('/').pop().replace('.html', '');
        localStorage.setItem('EnglishHub_Progress_' + pageId, 'true');
        alert('Good job! Progress saved.');
        location.href = 'index.html';
    }}
</script>
</body>
</html>"""

# Medical Vocabulary Pool
POOL = [
    {"en": "Symptom", "zh": "症狀", "sent": "What are your symptoms?", "sentZh": "你有什麼症狀？"},
    {"en": "Headache", "zh": "頭痛", "sent": "I have a splitting headache.", "sentZh": "我頭痛欲裂。"},
    {"en": "Fever", "zh": "發燒", "sent": "He has a high fever.", "sentZh": "他發高燒了。"},
    {"en": "Nausea", "zh": "噁心(想吐)", "sent": "I feel sudden nausea.", "sentZh": "我突然感到噁心。"},
    {"en": "Dizziness", "zh": "頭暈", "sent": "She complained of dizziness.", "sentZh": "她抱怨說頭暈。"},
    {"en": "Prescription", "zh": "處方籤", "sent": "The doctor gave me a prescription.", "sentZh": "醫生給了我一張處方籤。"},
    {"en": "Pharmacy", "zh": "藥局", "sent": "Pick up medicine at the pharmacy.", "sentZh": "去藥局領藥。"},
    {"en": "Painkiller", "zh": "止痛藥", "sent": "Take a painkiller for the pain.", "sentZh": "吃止痛藥止痛。"},
    {"en": "Antibiotic", "zh": "抗生素", "sent": "You need a course of antibiotics.", "sentZh": "你需要接受抗生素療程。"},
    {"en": "Side Effect", "zh": "副作用", "sent": "Drowsiness is a side effect.", "sentZh": "嗜睡是副作用之一。"},
    {"en": "Allergy", "zh": "過敏", "sent": "I have an allergy to peanuts.", "sentZh": "我對花生過敏。"},
    {"en": "Diagnosis", "zh": "診斷", "sent": "The diagnosis was flu.", "sentZh": "診斷結果是流感。"},
    {"en": "Treatment", "zh": "治療", "sent": "Early treatment is key.", "sentZh": "早期治療是關鍵。"},
    {"en": "Surgery", "zh": "手術", "sent": "He requires emergency surgery.", "sentZh": "他需要緊急手術。"},
    {"en": "Recovery", "zh": "康復", "sent": "We wish you a speedy recovery.", "sentZh": "祝你早日康復。"},
    {"en": "Appointment", "zh": "預約(看診)", "sent": "I have a doctor's appointment.", "sentZh": "我有預約看醫生。"},
    {"en": "Insurance", "zh": "保險", "sent": "Does your insurance cover this?", "sentZh": "你的保險有承保這個嗎？"},
    {"en": "Emergency", "zh": "緊急情況/急診", "sent": "Call 911 in an emergency.", "sentZh": "緊急情況請撥打 911。"},
    {"en": "Ambulance", "zh": "救護車", "sent": "The ambulance arrived quickly.", "sentZh": "救護車很快就到了。"},
    {"en": "Vaccine", "zh": "疫苗", "sent": "The vaccine prevents disease.", "sentZh": "疫苗可預防疾病。"},
    {"en": "Infection", "zh": "感染", "sent": "Clean the wound to prevent infection.", "sentZh": "清潔傷口以防感染。"},
    {"en": "Blood Pressure", "zh": "血壓", "sent": "Check your blood pressure regularly.", "sentZh": "定期檢查你的血壓。"},
    {"en": "Diabetes", "zh": "糖尿病", "sent": "Manage diabetes with diet.", "sentZh": "透過飲食控制糖尿病。"},
    {"en": "Asthma", "zh": "氣喘", "sent": "He uses an inhaler for asthma.", "sentZh": "他使用吸入器治療氣喘。"},
    {"en": "Checkup", "zh": "健康檢查", "sent": "Go for an annual checkup.", "sentZh": "去做年度健康檢查。"}
]

def generate_day(day_num):
    filename = f"c:/Users/ian20/OneDrive/桌面/English/Medical_Day{day_num}.html"
    title = f"Day {day_num} - Medical English"
    
    # Simple logic to cycle pool if < 20
    words = []
    while len(words) < 20:
        w = random.choice(POOL)
        if w not in words:
            words.append(w)

    html_content = TEMPLATE.format(title=title, json_data=json.dumps(words, ensure_ascii=False))
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated {filename}")

def main():
    for i in range(1, 31):
        generate_day(i)

if __name__ == "__main__":
    main()
