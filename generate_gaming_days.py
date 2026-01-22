import os
import json
import random

# Gaming Theme Template
TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gaming & Streaming - {title}</title>
    <style>
        /* Gaming Theme Variables */
        :root {{
            --bg-color: #0f0f13;   /* Darkest Void */
            --card-bg: #1a1a24;    /* Gaming Panel */
            --text-main: #ffffff;
            --text-sub: #aab2bd;
            --accent: #9146ff;     /* Twitch Purple */
            --accent-sec: #00f2ff; /* Cyan Neon */
            --accent-hot: #ff0055; /* Magenta Neon */
            --font-main: 'Segoe UI', sans-serif;
            --font-game: 'Impact', sans-serif;
        }}

        body {{ 
            font-family: var(--font-main); 
            background-color: var(--bg-color); 
            background: linear-gradient(135deg, #0f0f13 0%, #1a1a24 100%);
            margin: 0; padding: 20px; 
            color: var(--text-main); 
            min-height: 100vh;
        }}
        
        .container {{ 
            max-width: 800px; margin: 0 auto; 
            background: rgba(26, 26, 36, 0.95); 
            padding: 30px; 
            border-radius: 15px; 
            box-shadow: 0 0 20px var(--accent); 
            border: 2px solid transparent;
            background-clip: padding-box;
            position: relative;
        }}
        
        /* RGB Border Effect */
        .container::after {{
            content: ''; position: absolute; top: -2px; left: -2px; right: -2px; bottom: -2px;
            background: linear-gradient(45deg, var(--accent-hot), var(--accent), var(--accent-sec));
            z-index: -1; border-radius: 16px;
        }}

        h1 {{ 
            text-align: center; color: white; 
            font-family: var(--font-game);
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 3px 3px 0px var(--accent);
            margin-bottom: 30px;
        }}
        
        .nav {{ display: flex; justify-content: center; gap: 15px; margin-bottom: 30px; flex-wrap: wrap; }}
        .btn {{ 
            padding: 10px 25px; border: none; border-radius: 5px;
            background: linear-gradient(90deg, var(--accent), #7a2add);
            color: white; font-weight: bold;
            cursor: pointer; font-size: 16px; transition: 0.2s;
            text-transform: uppercase;
        }}
        
        .btn:hover {{ 
            transform: scale(1.1); 
            box-shadow: 0 0 15px var(--accent);
        }}

        /* Learning Mode Cards */
        .word-card {{ 
            border-left: 5px solid var(--accent-sec); 
            background: #252533; 
            padding: 20px; margin-bottom: 20px; 
            border-radius: 8px;
        }}
        .word-header {{ display: flex; align-items: center; gap: 15px; margin-bottom: 10px; }}
        .english-word {{ 
            font-size: 26px; font-weight: bold; color: var(--accent-sec); 
            text-shadow: 0 0 5px rgba(0, 242, 255, 0.5);
        }}
        .speak-btn {{ 
            background: #333; border: none; 
            border-radius: 50%; width: 32px; height: 32px; color: #fff;
            cursor: pointer; display: flex; align-items: center; justify-content: center; transition: 0.2s; 
        }}
        .speak-btn:hover {{ background: var(--accent-hot); }}
        .meaning {{ color: white; font-weight: bold; font-size: 20px; }}
        
        .sentence-box {{ margin-top: 10px; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 5px; }}
        .sentence {{ font-style: italic; color: #ddd; font-size: 1.1em; margin-bottom: 4px; }}
        .sentence-zh {{ color: var(--text-sub); font-size: 0.95em; }}

        /* Quiz Mode */
        #quiz-section {{ display: none; text-align: center; }}
        .question-word {{ 
            font-size: 32px; font-weight: bold; margin-bottom: 30px; 
            color: var(--accent-hot); text-shadow: 0 0 10px var(--accent-hot);
        }}
        .options-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
        .option-btn {{ 
            background: #252533; border: 2px solid transparent; color: white;
            padding: 15px; border-radius: 8px; cursor: pointer; font-size: 16px; transition: 0.2s; 
            font-weight: bold;
        }}
        .option-btn:hover {{ border-color: var(--accent-sec); box-shadow: 0 0 10px var(--accent-sec); }}
        .option-btn:disabled {{ opacity: 0.6; cursor: not-allowed; }}
        
        .result-message {{ font-size: 22px; font-weight: bold; margin-top: 25px; padding: 15px; border-radius: 8px; }}
        .correct {{ color: #0f0; background: rgba(0, 255, 0, 0.1); border: 1px solid #0f0; }}
        .wrong {{ color: #f00; background: rgba(255, 0, 0, 0.1); border: 1px solid #f00; }}
        .score-board {{ font-size: 36px; color: var(--accent-sec); margin-top: 30px; font-family: var(--font-game); }}
    </style>
</head>
<body>

<div class="container">
    <h1>👾 {title}</h1>
    
    <div class="nav">
        <a href="index.html" class="btn">🏠 Lobby</a>
        <button class="btn" onclick="showSection('learn')">🗡️ Quest</button>
        <button class="btn" onclick="startQuiz()">⚔️ Boss Fight</button>
    </div>

    <div id="learn-section"></div>

    <div id="quiz-section">
        <div id="quiz-container">
            <div class="question-word" id="q-word">Word</div>
            <div class="options-grid" id="options-area"></div>
            <div id="result-msg"></div>
        </div>
        <div id="final-score" style="display:none;" class="score-board"></div>
        <button id="restart-btn" class="btn" style="display:none; margin-top:20px;" onclick="startQuiz()">🔄 Respawn</button>
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
                    <button class="speak-btn" onclick="speak('${{item.en}}')" title="Voice Chat">🔊</button>
                    <span class="meaning">${{item.zh}}</span>
                </div>
                <div class="sentence-box">
                    <div class="sentence">"${{item.sent}}"
                        <button class="speak-btn" style="width:24px; height:24px; font-size:12px; display:inline-flex; vertical-align:middle; margin-left:5px;" onclick="speak(wordsDB[${{index}}].sent)" title="Play Voice Line">🔊</button>
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
            resultDiv.textContent = "✅ Headshot (Critical Hit)!";
            resultDiv.className = "result-message correct";
        }} else {{
            resultDiv.textContent = `❌ You Died! Answer: ${{correct}}`;
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
        let report = `Game Over<br>High Score: ${{score}} / ${{wordsDB.length}}`;
        if (wrongAnswers.length > 0) {{
            report += '<div style="margin-top:20px; text-align:left; background:#222; padding:15px; border-radius:8px; border:1px solid #555;">';
            report += '<h3 style="color:#ff5555; margin-top:0;">Failed Quests (Review):</h3><ul style="padding-left:20px; color:#ccc;">';
            wrongAnswers.forEach(w => {{
                report += `<li style="margin-bottom:5px;"><strong>${{w.en}}</strong>: <span style="color:#0f0;">${{w.zh}}</span> <span style="color:#888; font-size:0.9em;">(Pick: ${{w.selected}})</span></li>`;
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
        alert('GG! 今日學習進度已保存。');
        location.href = 'index.html';
    }}
</script>
</body>
</html>"""

# Gaming & Streaming Vocab Pool
POOL = [
    # Gameplay
    {"en": "Lag", "zh": "延遲/卡頓", "sent": "The lag is terrible.", "sentZh": "這延遲太糟糕了。"},
    {"en": "Buff", "zh": "增強", "sent": "They buffed this weapon.", "sentZh": "他們增強了這把武器。"},
    {"en": "Nerf", "zh": "削弱", "sent": "The hero got nerfed.", "sentZh": "這英雄被削弱了。"},
    {"en": "Grind", "zh": "農怪/苦練", "sent": "I have to grind for XP.", "sentZh": "我必須農經驗值。"},
    {"en": "Loot", "zh": "戰利品", "sent": "Pick up the loot.", "sentZh": "撿起戰利品。"},
    {"en": "Spawn", "zh": "重生/生成", "sent": "Enemy spawned behind you.", "sentZh": "敵人在你後面重生了。"},
    {"en": "Camp", "zh": "龜點/蹲點", "sent": "Stop camping in the corner!", "sentZh": "別再龜在角落了！"},
    {"en": "Noob", "zh": "新手/菜鳥", "sent": "Don't be a noob.", "sentZh": "別當個菜鳥。"},
    {"en": "Smurf", "zh": "炸魚(開小號)", "sent": "He is smurfing in low rank.", "sentZh": "他在低排位炸魚。"},
    {"en": "Carry", "zh": "凱瑞(帶飛)", "sent": "Please carry me.", "sentZh": "拜託凱瑞我。"},
    {"en": "Tank", "zh": "坦克(肉盾)", "sent": "We need a tank.", "sentZh": "我們需要一個坦克。"},
    {"en": "DPS", "zh": "輸出(每秒傷害)", "sent": "Low DPS output.", "sentZh": "低傷害輸出。"},
    {"en": "Healer", "zh": "補師", "sent": "Protect the healer.", "sentZh": "保護補師。"},
    {"en": "Meta", "zh": "主流戰術", "sent": "This is the current meta.", "sentZh": "這是目前的主流玩法。"},
    {"en": "Gank", "zh": "偷襲", "sent": "Jungler is coming to gank.", "sentZh": "打野要來偷襲了。"},
    {"en": "Aggro", "zh": "仇恨值", "sent": "Don't pull aggro.", "sentZh": "別拉到仇恨。"},
    {"en": "NPC", "zh": "非玩家角色", "sent": "Talk to the NPC.", "sentZh": "跟 NPC 對話。"},
    {"en": "Quest", "zh": "任務", "sent": "Complete the quest.", "sentZh": "完成任務。"},
    {"en": "Boss", "zh": "魔王", "sent": "Defeat the final boss.", "sentZh": "打敗最終魔王。"},
    {"en": "HP (Health Points)", "zh": "生命值", "sent": "My HP is low.", "sentZh": "我血量很低。"},
    {"en": "MP (Mana Points)", "zh": "魔力值", "sent": "Out of MP.", "sentZh": "沒魔了。"},
    {"en": "XP (Experience)", "zh": "經驗值", "sent": "Gain XP to level up.", "sentZh": "獲得經驗值升級。"},
    {"en": "Cooldown", "zh": "冷卻時間", "sent": "Skill is on cooldown.", "sentZh": "技能冷卻中。"},
    {"en": "Ult / Ultimate", "zh": "大招/終極技能", "sent": "My ult is ready.", "sentZh": "我的大招好了。"},
    {"en": "GG (Good Game)", "zh": "好局(結束了)", "sent": "GG WP (Well Played).", "sentZh": "好局，打得好。"},
    {"en": "AFK", "zh": "掛網(不在電腦前)", "sent": "He went AFK.", "sentZh": "他掛網了。"},
    {"en": "Toxic", "zh": "嘴臭/惡質", "sent": "The community is toxic.", "sentZh": "這社群很惡質。"},
    {"en": "Salty", "zh": "惱羞", "sent": "Why are you so salty?", "sentZh": "你幹嘛這麼惱羞？"},
    {"en": "Tilt", "zh": "心態崩越打越爛", "sent": "I'm on full tilt.", "sentZh": "我心態全崩了。"},
    {"en": "Clutch", "zh": "關鍵時刻逆轉", "sent": "That was a clutch play!", "sentZh": "那操作太關鍵了！"},
    {"en": "Op (Overpowered)", "zh": "過強(做壞了)", "sent": "That gun is OP.", "sentZh": "那把槍太 OP 了。"},
    # Streaming
    {"en": "Streamer", "zh": "實況主", "sent": "My favorite streamer is live.", "sentZh": "我最愛的實況主開台了。"},
    {"en": "Subscribe", "zh": "訂閱", "sent": "Don't forget to subscribe.", "sentZh": "別忘了訂閱。"},
    {"en": "Follow", "zh": "追隨", "sent": "Thanks for the follow.", "sentZh": "謝謝追隨。"},
    {"en": "Donation / Dono", "zh": "贊助(斗內)", "sent": "Huge donation!", "sentZh": "巨額贊助！"},
    {"en": "Chat", "zh": "聊天室", "sent": "Read the chat.", "sentZh": "看聊天室。"},
    {"en": "Mod (Moderator)", "zh": "板手(管理員)", "sent": "Mods, ban him.", "sentZh": "管理員，Ban 掉他。"},
    {"en": "Ban", "zh": "封鎖", "sent": "You are permanently banned.", "sentZh": "你被永久封鎖了。"},
    {"en": "Emote", "zh": "表情符號", "sent": "Spam emotes in chat.", "sentZh": "在聊天室狂刷表情。"},
    {"en": "Raid", "zh": "揪團(導流)", "sent": "We are raiding Ian's channel.", "sentZh": "我們要去揪團 Ian 的頻道。"},
    {"en": "Overlay", "zh": "介面層", "sent": "New stream overlay.", "sentZh": "新的實況介面。"},
    {"en": "Alert", "zh": "通知(跳通知)", "sent": "The sub alert didn't trigger.", "sentZh": "訂閱通知沒跳出來。"},
    {"en": "Bitrate", "zh": "位元率", "sent": "Increase the streaming bitrate.", "sentZh": "提高串流位元率。"},
    {"en": "Facecam", "zh": "視訊鏡頭", "sent": "Turn on the facecam.", "sentZh": "開啟視訊鏡頭。"},
    {"en": "Highlights", "zh": "精華片段", "sent": "Watch the stream highlights.", "sentZh": "觀看實況精華。"},
    {"en": "VOD", "zh": "存檔影片", "sent": "Check the VOD later.", "sentZh": "晚點看 VOD (回放)。"}
]

def generate_day(day_num):
    filename = f"c:/Users/ian20/OneDrive/桌面/English/Gaming_Day{day_num}.html"
    title = f"Day {day_num} - Gaming & Streaming"
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
