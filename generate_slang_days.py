import os
import json
import random

# Slang Theme Template (Caution / Street Style)
TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Slang & Expressive - {title}</title>
    <style>
        /* Slang Theme Variables */
        :root {{
            --bg-color: #111;      /* Asphalt Black */
            --card-bg: #222;       /* Dark Grey */
            --text-main: #fff;
            --text-sub: #aaa;
            --accent: #f1c40f;     /* Warning Yellow */
            --accent-hot: #c0392b; /* Danger Red */
            --spray: #e67e22;      /* Spray Paint Orange */
            --font-main: 'Segoe UI', sans-serif;
            --font-street: 'Impact', 'Arial Black', sans-serif;
        }}

        body {{ 
            font-family: var(--font-main); 
            background-color: var(--bg-color); 
            /* Urban texture */
            background-image: repeating-linear-gradient(45deg, #181818 20px, #111 20px, #111 40px);
            margin: 0; padding: 20px; 
            color: var(--text-main); 
            min-height: 100vh;
        }}
        
        .container {{ 
            max-width: 800px; margin: 0 auto; 
            background: var(--card-bg); 
            padding: 30px; 
            border-radius: 0px; 
            box-shadow: 10px 10px 0px var(--accent); 
            border: 4px solid var(--text-main);
            position: relative;
        }}
        
        /* Caution Tape Effect at top */
        .container::before {{
            content: ''; position: absolute; top: -20px; left: 20px; right: 20px; height: 10px;
            background: repeating-linear-gradient(45deg, var(--accent) 0, var(--accent) 10px, #000 10px, #000 20px);
            transform: rotate(-1deg);
            box-shadow: 0 5px 10px rgba(0,0,0,0.5);
        }}

        h1 {{ 
            text-align: center; color: var(--accent); 
            font-family: var(--font-street);
            text-transform: uppercase;
            letter-spacing: -1px;
            font-size: 2.5em;
            transform: rotate(-2deg);
            margin-bottom: 30px;
            text-shadow: 4px 4px 0px #000;
        }}
        
        .nav {{ display: flex; justify-content: center; gap: 15px; margin-bottom: 30px; flex-wrap: wrap; }}
        .btn {{ 
            padding: 10px 25px; border: 3px solid var(--text-main); background: #000;
            color: var(--text-main); font-weight: bold;
            cursor: pointer; font-size: 16px; transition: 0.1s;
            text-transform: uppercase;
            box-shadow: 5px 5px 0px var(--text-main);
        }}
        
        .btn:hover {{ 
            background: var(--accent); color: #000; 
            transform: translate(-3px, -3px);
            box-shadow: 8px 8px 0px var(--text-main);
        }}
        
        .btn-active {{ background: var(--accent); color: #000; }}

        /* Learning Mode Cards */
        .word-card {{ 
            border: 2px solid #444; 
            background: #2a2a2a; 
            padding: 20px; margin-bottom: 20px; 
            box-shadow: 5px 5px 0px #000;
        }}
        .word-header {{ display: flex; align-items: center; gap: 15px; margin-bottom: 10px; }}
        .english-word {{ 
            font-size: 28px; font-weight: bold; color: var(--accent); 
            font-family: var(--font-street);
            letter-spacing: -1px;
            background: #000; padding: 2px 8px; transform: rotate(-1deg);
        }}
        .speak-btn {{ 
            background: #444; border: none; 
            border-radius: 0; width: 36px; height: 36px; color: #fff;
            cursor: pointer; display: flex; align-items: center; justify-content: center; transition: 0.2s; 
        }}
        .speak-btn:hover {{ background: var(--accent); color: #000; }}
        .meaning {{ color: var(--text-main); font-weight: bold; font-size: 20px; margin-left: auto; }}
        .tag {{ 
            font-size: 0.7em; background: var(--accent-hot); color: white; 
            padding: 2px 6px; border-radius: 3px; font-weight: bold; margin-left: 10px;
        }}

        
        .sentence-box {{ margin-top: 15px; padding: 15px; background: #000; border-left: 4px solid var(--spray); }}
        .sentence {{ font-style: italic; color: #fff; font-size: 1.1em; margin-bottom: 5px; }}
        .sentence-zh {{ color: #888; font-size: 0.95em; }}

        /* Quiz Mode */
        #quiz-section {{ display: none; text-align: center; }}
        .question-word {{ 
            font-size: 36px; font-weight: bold; margin-bottom: 30px; 
            color: var(--accent); font-family: var(--font-street);
            text-decoration: underline wavy var(--accent-hot);
        }}
        .options-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        .option-btn {{ 
            background: #333; border: 2px solid #555; color: white;
            padding: 15px; cursor: pointer; font-size: 18px; transition: 0.1s; 
            font-weight: bold; font-family: var(--font-street);
        }}
        .option-btn:hover {{ background: var(--accent); color: #000; border-color: #000; }}
        .option-btn:disabled {{ opacity: 0.6; cursor: not-allowed; }}
        
        .result-message {{ font-size: 22px; font-weight: bold; margin-top: 25px; padding: 15px; background: #000; border: 2px solid white; }}
        .correct {{ color: var(--accent); border-color: var(--accent); }}
        .wrong {{ color: var(--accent-hot); border-color: var(--accent-hot); }}
        .score-board {{ font-size: 40px; color: var(--accent); margin-top: 30px; font-family: var(--font-street); }}
    </style>
</head>
<body>

<div class="container">
    <h1>🤬 {title}</h1>
    
    <div class="nav">
        <a href="index.html" class="btn">🏠 Safe Zone</a>
        <button class="btn btn-active" onclick="showSection('learn')">🗣️ Street Talk</button>
        <button class="btn" onclick="startQuiz()">🔥 Rap Battle</button>
    </div>

    <div id="learn-section"></div>

    <div id="quiz-section">
        <div id="quiz-container">
            <div class="question-word" id="q-word">Word</div>
            <div class="options-grid" id="options-area"></div>
            <div id="result-msg"></div>
        </div>
        <div id="final-score" style="display:none;" class="score-board"></div>
        <button id="restart-btn" class="btn" style="display:none; margin-top:20px;" onclick="startQuiz()">🔄 Run It Back</button>
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
            let tagHTML = '';
            if (item.tag) tagHTML = `<span class="tag">${{item.tag}}</span>`;
            
            card.innerHTML = `
                <div class="word-header">
                    <span class="english-word">${{item.en}}</span>
                    ${{tagHTML}}
                    <span class="meaning">${{item.zh}}</span>
                    <button class="speak-btn" onclick="speak('${{item.en}}')" title="Listen">🔊</button>
                </div>
                <div class="sentence-box">
                    <div class="sentence">"${{item.sent}}"
                        <button class="speak-btn" style="width:24px; height:24px; font-size:12px; display:inline-flex; vertical-align:middle; margin-left:5px;" onclick="speak(wordsDB[${{index}}].sent)" title="Listen to Sentence">🔊</button>
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
            resultDiv.textContent = "✅ Nailed it!";
            resultDiv.className = "result-message correct";
        }} else {{
            resultDiv.textContent = `❌ Wasted! Answer: ${{correct}}`;
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
        let report = `Respect!<br>Score: ${{score}} / ${{wordsDB.length}}`;
        if (wrongAnswers.length > 0) {{
            report += '<div style="margin-top:20px; text-align:left; background:#222; padding:15px; border:1px solid #555;">';
            report += '<h3 style="color:#f1c40f; margin-top:0;">You messed up these:</h3><ul style="padding-left:20px; color:#ccc;">';
            wrongAnswers.forEach(w => {{
                report += `<li style="margin-bottom:5px;"><strong>${{w.en}}</strong>: <span style="color:#eee;">${{w.zh}}</span> <span style="color:#666; font-size:0.9em;">(Your guess: ${{w.selected}})</span></li>`;
            }});
            report += '</ul></div>';
        }}
        scoreBoard.innerHTML = report;
        document.getElementById('restart-btn').style.display = 'inline-block';
    }}

    initLearn();
</script>
    <div style="text-align: center; margin-top: 40px; margin-bottom: 20px;">
        <button onclick="markComplete()" style="padding: 15px 30px; background: #27ae60; color: white; border: none; border-radius: 50px; font-size: 18px; cursor: pointer; font-weight: bold; box-shadow: 0 4px 15px rgba(39,174,96,0.3);">✅ 完成今日學習 (Mark Complete)</button>
    </div>

<script>
    function markComplete() {{
        const pageId = window.location.pathname.split('/').pop().replace('.html', '');
        localStorage.setItem('EnglishHub_Progress_' + pageId, 'true');
        alert('Nailed it! 今日學習進度已保存。');
        location.href = 'index.html';
    }}
</script>
</body>
</html>"""

# Slang & Curse Vocab Pool (Educational Context)
POOL = [
    # Mild / Common
    {"en": "Whatever", "zh": "隨便啦", "sent": "Whatever, I don't care.", "sentZh": "隨便啦，我不在乎。", "tag": "Mild"},
    {"en": "My bad", "zh": "我的錯", "sent": "Oops, my bad.", "sentZh": "噢，我的錯。", "tag": "Mild"},
    {"en": "No worries", "zh": "沒事/不客氣", "sent": "No worries, it's fine.", "sentZh": "沒事，沒關係。", "tag": "Mild"},
    {"en": "Dude", "zh": "老兄", "sent": "Dude, that's cool.", "sentZh": "老兄，那太酷了。", "tag": "Mild"},
    {"en": "Bro", "zh": "兄弟", "sent": "Chill out, bro.", "sentZh": "冷靜點，兄弟。", "tag": "Mild"},
    {"en": "Lame", "zh": "遜/無聊", "sent": "That joke was lame.", "sentZh": "那個笑話很遜。", "tag": "Mild"},
    {"en": "Sketchy", "zh": "可疑的/怪怪的", "sent": "This alley looks sketchy.", "sentZh": "這條巷子看起來怪怪的。", "tag": "Mild"},
    {"en": "Awesome", "zh": "棒極了", "sent": "The movie was awesome.", "sentZh": "這部電影棒極了。", "tag": "Mild"},
    
    # Modern / Internet Slang
    {"en": "Ghosting", "zh": "神隱(搞消失)", "sent": "He is ghosting me.", "sentZh": "他對我搞消失(已讀不回)。", "tag": "Slang"},
    {"en": "Flex", "zh": "炫耀", "sent": "He likes to flex his money.", "sentZh": "他喜歡炫耀他的錢。", "tag": "Slang"},
    {"en": "Salty", "zh": "惱羞/酸", "sent": "Don't be salty just because you lost.", "sentZh": "別因為輸了就惱羞。", "tag": "Slang"},
    {"en": "Lit", "zh": "超讚/嗨", "sent": "The party was lit.", "sentZh": "派對超嗨。", "tag": "Slang"},
    {"en": "Simp", "zh": "火山孝子/舔狗", "sent": "Stop being a simp.", "sentZh": "別當個舔狗。", "tag": "Slang"},
    {"en": "Cap / No Cap", "zh": "謊話/不騙你", "sent": "That's cap. / No cap.", "sentZh": "那是騙人的。/ 我不騙你。", "tag": "Slang"},
    {"en": "Boomer", "zh": "老古板", "sent": "Ok, boomer.", "sentZh": "好喔，老古板。", "tag": "Slang"},
    {"en": "Karen", "zh": "奧客大媽(Karen)", "sent": "She is acting like a Karen.", "sentZh": "她表現得像個奧客大媽。", "tag": "Slang"},
    {"en": "Sus", "zh": "可疑的(Among Us梗)", "sent": "You are acting sus.", "sentZh": "你行為很可疑。", "tag": "Slang"},
    {"en": "Cringe", "zh": "尷尬癌發作", "sent": "That video is so cringe.", "sentZh": "那影片超尷尬。", "tag": "Slang"},

    # Expressive / Stronger (Educational Purpose)
    {"en": "Damn", "zh": "該死/可惡", "sent": "Damn, I forgot my keys.", "sentZh": "該死，我忘帶鑰匙了。", "tag": "Caution"},
    {"en": "Hell", "zh": "地獄/見鬼", "sent": "What the hell?", "sentZh": "搞什麼鬼？", "tag": "Caution"},
    {"en": "Pissed off", "zh": "超不爽", "sent": "I am so pissed off.", "sentZh": "我超不爽。", "tag": "Caution"},
    {"en": "Screw up", "zh": "搞砸了", "sent": "I screwed up big time.", "sentZh": "我搞砸得一塌糊塗。", "tag": "Caution"},
    {"en": "Sucks", "zh": "爛透了", "sent": "This internet sucks.", "sentZh": "這網路爛透了。", "tag": "Caution"},
    {"en": "Shut up", "zh": "閉嘴", "sent": "Shut up and listen.", "sentZh": "閉嘴聽我說。", "tag": "Caution"},
    {"en": "Nerd", "zh": "書呆子", "sent": "He is a computer nerd.", "sentZh": "他是個電腦書呆子。", "tag": "Common"},
    {"en": "Geek", "zh": "狂熱者/怪咖", "sent": "I'm a tech geek.", "sentZh": "我是個科技狂熱者。", "tag": "Common"},
    {"en": "Freak", "zh": "怪胎", "sent": "Don't be a freak.", "sentZh": "別當個怪胎。", "tag": "Common"},
    {"en": "Idiot", "zh": "白痴", "sent": "Don't be an idiot.", "sentZh": "別當個白痴。", "tag": "Insult"},
    {"en": "Jerk", "zh": "渾蛋", "sent": "He is such a jerk.", "sentZh": "他真是個渾蛋。", "tag": "Insult"},
    {"en": "Moron", "zh": "智障", "sent": "What a moron.", "sentZh": "真是個智障。", "tag": "Insult"},
    
    # Strong Language (Filtered to common safe-for-work variants or explicit markings)
    {"en": "WTF", "zh": "搞什麼(縮寫)", "sent": "WTF is happening?", "sentZh": "現在是搞什麼？", "tag": "Explicit"},
    {"en": "BS (Bullsh*t)", "zh": "胡扯/廢話", "sent": "That is total BS.", "sentZh": "那完全是鬼扯。", "tag": "Explicit"},
    {"en": "Ass", "zh": "屁股/笨蛋", "sent": "Don't be a smart ass.", "sentZh": "別自作聰明。", "tag": "Caution"},
    {"en": "Badass", "zh": "超猛/硬漢", "sent": "He is a badass.", "sentZh": "他超猛的。", "tag": "Slang"},
    {"en": "Kick ass", "zh": "很厲害/教訓", "sent": "This game kicks ass.", "sentZh": "這遊戲太讚了。", "tag": "Slang"}
]

def generate_day(day_num):
    filename = f"c:/Users/ian20/OneDrive/桌面/English/Slang_Day{day_num}.html"
    title = f"Day {day_num} - Slang & Expressive"
    words = random.sample(POOL, 20)
    
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
