import os
import json
import random

# Food Theme Template
TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Food & Dining - {title}</title>
    <style>
        /* Food Theme Variables */
        :root {{
            --bg-color: #fff9e6;   /* Cream */
            --card-bg: #ffffff;    /* White */
            --text-main: #5d4037;  /* Brown */
            --text-sub: #8d6e63;   /* Light Brown */
            --accent: #ff9800;     /* Orange */
            --accent-glow: #ffb74d; 
            --secondary: #8bc34a;  /* Fresh Green */
            --font-main: 'Segoe UI', 'Comic Sans MS', sans-serif;
            --font-code: 'Consolas', 'Monaco', monospace;
        }}

        body {{ 
            font-family: var(--font-main); 
            background-color: var(--bg-color); 
            /* Food pattern (dots) */
            background-image: radial-gradient(#ffcc80 20%, transparent 20%), radial-gradient(#ffe0b2 20%, transparent 20%);
            background-size: 50px 50px;
            background-position: 0 0, 25px 25px;
            margin: 0; padding: 20px; 
            color: var(--text-main); 
            min-height: 100vh;
        }}
        
        .container {{ 
            max-width: 800px; margin: 0 auto; 
            background: var(--card-bg); 
            padding: 30px; 
            border-radius: 20px; 
            box-shadow: 0 8px 30px rgba(255, 152, 0, 0.2); 
            border: 2px solid #fff3e0;
        }}

        h1 {{ 
            text-align: center; color: var(--accent); 
            font-family: var(--font-main);
            text-transform: uppercase;
            letter-spacing: 2px;
            border-bottom: 2px dashed var(--accent);
            padding-bottom: 15px;
            margin-bottom: 30px;
        }}
        
        .nav {{ display: flex; justify-content: center; gap: 15px; margin-bottom: 30px; flex-wrap: wrap; }}
        .btn {{ 
            padding: 10px 25px; border: 2px solid var(--accent); background: white;
            color: var(--accent); border-radius: 50px;
            cursor: pointer; font-size: 16px; transition: 0.3s; font-weight: bold; 
        }}
        
        .btn:hover, .btn-active {{ 
            background: var(--accent); color: white; 
            box-shadow: 0 4px 15px rgba(255, 152, 0, 0.4);
            transform: translateY(-2px);
        }}

        /* Learning Mode Cards */
        .word-card {{ 
            border-left: 5px solid var(--secondary); 
            background: #fff; 
            padding: 25px; margin-bottom: 25px; 
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }}
        .word-card:hover {{ transform: scale(1.02); }}
        
        .word-header {{ display: flex; align-items: center; gap: 15px; margin-bottom: 10px; flex-wrap: wrap; }}
        .english-word {{ 
            font-size: 26px; font-weight: bold; color: var(--text-main); 
        }}
        .speak-btn {{ 
            background: #fff3e0; border: none; 
            border-radius: 50%; width: 36px; height: 36px; color: var(--accent);
            cursor: pointer; display: flex; align-items: center; justify-content: center; transition: 0.2s; 
        }}
        .speak-btn:hover {{ background: var(--secondary); color: white; }}
        .meaning {{ color: var(--secondary); font-weight: bold; font-size: 22px; }}
        
        .sentence-box {{ margin-top: 15px; padding: 15px; background: #fafafa; border-radius: 10px; }}
        .sentence {{ font-style: italic; color: #555; font-size: 1.1em; margin-bottom: 5px; }}
        .sentence-zh {{ color: var(--text-sub); font-size: 0.95em; }}

        /* Quiz Mode */
        #quiz-section {{ display: none; text-align: center; }}
        .question-word {{ 
            font-size: 32px; font-weight: bold; margin-bottom: 30px; 
            color: var(--accent);
        }}
        .options-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
        .option-btn {{ 
            background: #fff; border: 2px solid #eee; color: var(--text-main);
            padding: 15px; border-radius: 15px; cursor: pointer; font-size: 18px; transition: 0.2s; 
            font-weight: bold;
        }}
        .option-btn:hover {{ background-color: #fff8e1; border-color: var(--accent); }}
        .option-btn:disabled {{ opacity: 0.6; cursor: not-allowed; }}
        
        .result-message {{ font-size: 22px; font-weight: bold; margin-top: 25px; padding: 15px; border-radius: 10px; }}
        .correct {{ color: #2e7d32; background: #e8f5e9; border: 2px solid #c8e6c9; }}
        .wrong {{ color: #c62828; background: #ffebee; border: 2px solid #ffcdd2; }}
        .score-board {{ font-size: 28px; color: var(--accent); margin-top: 30px; }}
    </style>
</head>
<body>

<div class="container">
    <h1>🍔 {title}</h1>
    
    <div class="nav">
        <a href="index.html" class="btn">🏠 Home</a>
        <button class="btn btn-active" onclick="showSection('learn')">😋 Learn</button>
        <button class="btn" onclick="startQuiz()">🥢 Quiz</button>
    </div>

    <div id="learn-section"></div>

    <div id="quiz-section">
        <div id="quiz-container">
            <div class="question-word" id="q-word">Word</div>
            <div class="options-grid" id="options-area"></div>
            <div id="result-msg"></div>
        </div>
        <div id="final-score" style="display:none;" class="score-board"></div>
        <button id="restart-btn" class="btn" style="display:none; margin-top:20px;" onclick="startQuiz()">🔄 More Food!</button>
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
            resultDiv.textContent = "✅ Yummy!";
            resultDiv.className = "result-message correct";
        }} else {{
            resultDiv.textContent = `❌ Oh no! Answer: ${{correct}}`;
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
        let report = `Full (Quiz Complete)!<br>Score: ${{score}} / ${{wordsDB.length}}`;
        if (wrongAnswers.length > 0) {{
            report += '<div style="margin-top:20px; text-align:left; background:#fff; padding:15px; border-radius:15px; border:2px solid #ef5350;">';
            report += '<h3 style="color:#d32f2f; margin-top:0;">Leftovers (Errors):</h3><ul style="padding-left:20px; color:#555;">';
            wrongAnswers.forEach(w => {{
                report += `<li style="margin-bottom:5px;"><strong>${{w.en}}</strong>: <span style="color:#2e7d32;">${{w.zh}}</span> <span style="color:#999; font-size:0.9em;">(Your choice: ${{w.selected}})</span></li>`;
            }});
            report += '</ul></div>';
        }}
        scoreBoard.innerHTML = report;
        document.getElementById('restart-btn').style.display = 'inline-block';
    }}

    initLearn();
</script>

<div style="text-align: center; margin-top: 40px; margin-bottom: 20px;">
    <button onclick="markComplete()" style="padding: 15px 30px; background: #27ae60; color: white; border: none; border-radius: 50px; font-size: 18px; cursor: pointer; font-weight: bold; box-shadow: 0 4px 15px rgba(39,174,96,0.3); transition: 0.3s;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">✅ Eat It All (Complete)</button>
</div>

<script>
    function markComplete() {{
        const pageId = window.location.pathname.split('/').pop().replace('.html', '');
        localStorage.setItem('EnglishHub_Progress_' + pageId, 'true');
        alert('Delicious! Progress saved.');
        location.href = 'index.html';
    }}
</script>
</body>
</html>"""

# Food Vocabulary Pool
POOL = [
    {"en": "Menu", "zh": "菜單", "sent": "May I see the menu?", "sentZh": "我可以看菜單嗎？"},
    {"en": "Appetizer", "zh": "開胃菜", "sent": "We ordered garlic bread as an appetizer.", "sentZh": "我們點了大蒜麵包當開胃菜。"},
    {"en": "Entree / Main Course", "zh": "主餐", "sent": "For the entree, I'll have the steak.", "sentZh": "主餐我要點牛排。"},
    {"en": "Dessert", "zh": "甜點", "sent": "Is there room for dessert?", "sentZh": "還有肚子吃甜點嗎？"},
    {"en": "Beverage", "zh": "飲料", "sent": "Would you like a beverage?", "sentZh": "你需要飲料嗎？"},
    {"en": "Recipe", "zh": "食譜", "sent": "This is a family recipe.", "sentZh": "這是家傳食譜。"},
    {"en": "Ingredient", "zh": "食材", "sent": "Fresh ingredients are essential.", "sentZh": "新鮮食材很關鍵。"},
    {"en": "Spicy", "zh": "辣", "sent": "I love spicy food.", "sentZh": "我愛吃辣。"},
    {"en": "Salty", "zh": "鹹", "sent": "The soup is too salty.", "sentZh": "這湯太鹹了。"},
    {"en": "Sour", "zh": "酸", "sent": "Lemons are sour.", "sentZh": "檸檬是酸的。"},
    {"en": "Bitter", "zh": "苦", "sent": "Coffee can be bitter.", "sentZh": "咖啡可能會苦。"},
    {"en": "Sweet", "zh": "甜", "sent": "This cake is very sweet.", "sentZh": "這蛋糕很甜。"},
    {"en": "Crispy", "zh": "酥脆", "sent": "The fried chicken is crispy.", "sentZh": "炸雞很酥脆。"},
    {"en": "Reservation", "zh": "訂位", "sent": "I have a reservation at 7 PM.", "sentZh": "我晚上 7 點有訂位。"},
    {"en": "Waiter / Server", "zh": "服務生", "sent": "The waiter brought the bill.", "sentZh": "服務生拿來了帳單。"},
    {"en": "Chef", "zh": "主廚", "sent": "Compliments to the chef.", "sentZh": "向主廚致敬（這頓飯很棒）。"},
    {"en": "Vegetarian", "zh": "素食者", "sent": "Do you have vegetarian options?", "sentZh": "你們有素食選項嗎？"},
    {"en": "Allergy", "zh": "過敏", "sent": "I have a shellfish allergy.", "sentZh": "我對貝類過敏。"},
    {"en": "Takeout / Takeaway", "zh": "外帶", "sent": "Let's get takeout tonight.", "sentZh": "今晚叫外帶吧。"},
    {"en": "Delivery", "zh": "外送", "sent": "Food delivery is convenient.", "sentZh": "叫外送很方便。"},
    {"en": "Buffet", "zh": "自助餐", "sent": "All-you-can-eat buffet.", "sentZh": "吃到飽自助餐。"},
    {"en": "Cuisine", "zh": "料理(菜系)", "sent": "Italian cuisine is popular.", "sentZh": "義大利料理很受歡迎。"},
    {"en": "Tip", "zh": "小費", "sent": "Did you leave a tip?", "sentZh": "你有留小費嗎？"},
    {"en": "Bill / Check", "zh": "帳單", "sent": "Can we split the bill?", "sentZh": "我們可以分開結帳嗎？"},
    {"en": "Delicious", "zh": "美味", "sent": "This meal was delicious.", "sentZh": "這頓飯真美味。"}
]

def generate_day(day_num):
    filename = f"c:/Users/ian20/OneDrive/桌面/English/Food_Day{day_num}.html"
    title = f"Day {day_num} - Food & Dining"
    
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
