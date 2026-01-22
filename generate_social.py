import os
import json
import random

# Social Theme Template
TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Media - {title}</title>
    <style>
        /* Social Theme Variables (Instagram-like) */
        :root {{
            --bg-color: #fafafa;   /* Light Grey */
            --card-bg: #ffffff;    /* White */
            --text-main: #262626;  /* Dark */
            --text-sub: #8e8e8e;   /* Grey */
            --accent: #e1306c;     /* Instagram Pink/Purple */
            --accent-glow: #e1306c; 
            --secondary: #405de6;  /* Instagram Blue */
            --font-main: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
            --font-code: 'Consolas', 'Monaco', monospace;
        }}

        body {{ 
            font-family: var(--font-main); 
            background-color: var(--bg-color); 
            margin: 0; padding: 20px; 
            color: var(--text-main); 
            min-height: 100vh;
        }}
        
        .container {{ 
            max-width: 800px; margin: 0 auto; 
            background: var(--card-bg); 
            padding: 30px; 
            border-radius: 3px; 
            box-shadow: 0 1px 1px rgba(0,0,0,0.1); 
            border: 1px solid #dbdbdb;
        }}

        h1 {{ 
            text-align: center; 
            background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Segoe UI', cursive, sans-serif;
            font-size: 2.5em;
            margin-bottom: 30px;
        }}
        
        .nav {{ display: flex; justify-content: center; gap: 15px; margin-bottom: 30px; flex-wrap: wrap; }}
        .btn {{ 
            padding: 10px 25px; border: 1px solid #dbdbdb; background: transparent;
            color: var(--text-main); border-radius: 4px;
            cursor: pointer; font-size: 16px; transition: 0.3s; font-weight: 600; 
        }}
        
        .btn:hover, .btn-active {{ 
            background: #efefef; color: var(--text-main); 
        }}
        .btn-active {{ border-bottom: 2px solid var(--text-main); border-radius: 0; border-top: 0; border-left: 0; border-right: 0; }}

        /* Learning Mode Cards */
        .word-card {{ 
            border: 1px solid #dbdbdb; 
            background: #fff; 
            padding: 20px; margin-bottom: 20px; 
            border-radius: 3px;
        }}
        
        .word-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }}
        .avatar {{ 
            width: 40px; height: 40px; background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); 
            border-radius: 50%; padding: 2px;
        }}
        .avatar-inner {{ width: 100%; height: 100%; background: #fff; border-radius: 50%; }}
        
        .english-word {{ 
            font-size: 20px; font-weight: 600; color: var(--text-main); 
        }}
        .speak-btn {{ 
            background: transparent; border: none; font-size: 20px;
            cursor: pointer; display: flex; align-items: center; justify-content: center; transition: 0.2s; 
        }}
        .speak-btn:hover {{ transform: scale(1.1); }}
        .meaning {{ color: var(--secondary); font-weight: normal; font-size: 18px; margin-left: auto; }}
        
        .sentence-box {{ margin-top: 10px; }}
        .sentence {{ color: var(--text-main); font-size: 1em; margin-bottom: 4px; line-height: 1.5; }}
        .sentence-zh {{ color: var(--text-sub); font-size: 0.9em; margin-top: 5px; }}

        /* Quiz Mode */
        #quiz-section {{ display: none; text-align: center; }}
        .question-word {{ 
            font-size: 32px; font-weight: bold; margin-bottom: 30px; 
            color: var(--text-main);
        }}
        .options-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
        .option-btn {{ 
            background: #fff; border: 1px solid #dbdbdb; color: var(--text-main);
            padding: 15px; border-radius: 4px; cursor: pointer; font-size: 16px; transition: 0.2s; 
            font-weight: 600;
        }}
        .option-btn:hover {{ background-color: #fafafa; border-color: #8e8e8e; }}
        .option-btn:disabled {{ opacity: 0.6; cursor: not-allowed; }}
        
        .result-message {{ font-size: 20px; font-weight: bold; margin-top: 25px; padding: 15px; border-radius: 4px; }}
        .correct {{ color: var(--secondary); }}
        .wrong {{ color: #ed4956; }}
        .score-board {{ font-size: 28px; color: var(--text-main); margin-top: 30px; }}
    </style>
</head>
<body>

<div class="container">
    <h1>📱 {title}</h1>
    
    <div class="nav">
        <a href="index.html" class="btn">🏠 Feed</a>
        <button class="btn btn-active" onclick="showSection('learn')">♥️ Learn</button>
        <button class="btn" onclick="startQuiz()">💬 Quiz</button>
    </div>

    <div id="learn-section"></div>

    <div id="quiz-section">
        <div id="quiz-container">
            <div class="question-word" id="q-word">Word</div>
            <div class="options-grid" id="options-area"></div>
            <div id="result-msg"></div>
        </div>
        <div id="final-score" style="display:none;" class="score-board"></div>
        <button id="restart-btn" class="btn" style="display:none; margin-top:20px; width:100%; background:#0095f6; color:white; border:none;" onclick="startQuiz()">Refresh Feed</button>
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
                    <div class="avatar"><div class="avatar-inner"></div></div>
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
            resultDiv.textContent = "✅ Liked!";
            resultDiv.className = "result-message correct";
        }} else {{
            resultDiv.textContent = `❌ Unfollowed! Answer: ${{correct}}`;
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
        let report = `Story Views: ${{score}} / ${{wordsDB.length}}`;
        if (wrongAnswers.length > 0) {{
            report += '<div style="margin-top:20px; text-align:left; background:#fff; padding:15px; border-radius:4px; border:1px solid #dbdbdb;">';
            report += '<h3 style="color:#ed4956; margin-top:0;">Failed to Upload (Errors):</h3><ul style="padding-left:20px; color:#555;">';
            wrongAnswers.forEach(w => {{
                report += `<li style="margin-bottom:5px;"><strong>${{w.en}}</strong>: <span style="color:#0095f6;">${{w.zh}}</span> <span style="color:#999; font-size:0.9em;">(Input: ${{w.selected}})</span></li>`;
            }});
            report += '</ul></div>';
        }}
        scoreBoard.innerHTML = report;
        document.getElementById('restart-btn').style.display = 'inline-block';
    }}

    initLearn();
</script>

<div style="text-align: center; margin-top: 40px; margin-bottom: 20px;">
    <button onclick="markComplete()" style="padding: 15px 30px; background: #0095f6; color: white; border: none; border-radius: 4px; font-size: 18px; cursor: pointer; font-weight: 600; box-shadow: 0 4px 15px rgba(0, 149, 246, 0.3);">✅ Post to Profile (Complete)</button>
</div>

<script>
    function markComplete() {{
        const pageId = window.location.pathname.split('/').pop().replace('.html', '');
        localStorage.setItem('EnglishHub_Progress_' + pageId, 'true');
        alert('Posted! Progress saved.');
        location.href = 'index.html';
    }}
</script>
</body>
</html>"""

# Social Media Vocabulary Pool
POOL = [
    {"en": "Content", "zh": "內容", "sent": "Create engaging content.", "sentZh": "創作吸引人的內容。"},
    {"en": "Influencer", "zh": "網紅/影響者", "sent": "She is a beauty influencer.", "sentZh": "她是一位美妝網紅。"},
    {"en": "Algorithm", "zh": "演算法", "sent": "The algorithm changed again.", "sentZh": "演算法又變了。"},
    {"en": "Trending", "zh": "流行/趨勢", "sent": "This hashtag is trending.", "sentZh": "這個標籤正在流行。"},
    {"en": "Hashtag", "zh": "標籤(#)", "sent": "Use relevant hashtags.", "sentZh": "使用相關的標籤。"},
    {"en": "Viral", "zh": "爆紅", "sent": "The video went viral.", "sentZh": "那部影片爆紅了。"},
    {"en": "Follower", "zh": "追蹤者", "sent": "I gained 100 followers.", "sentZh": "我增加了 100 位追蹤者。"},
    {"en": "Subscriber", "zh": "訂閱者", "sent": "Like and subscribe!", "sentZh": "按讚並訂閱！"},
    {"en": "Engagement", "zh": "互動率", "sent": "High engagement is good.", "sentZh": "高互動率是好事。"},
    {"en": "Notification", "zh": "通知", "sent": "Turn on notifications.", "sentZh": "開啟通知。"},
    {"en": "DM (Direct Message)", "zh": "私訊", "sent": "Slide into the DMs.", "sentZh": "傳私訊 (搭訕)。"},
    {"en": "Profile", "zh": "個人檔案", "sent": "Link in bio / profile.", "sentZh": "連結在個人檔案。"},
    {"en": "Bio", "zh": "自我介紹", "sent": "Update your bio.", "sentZh": "更新你的自我介紹。"},
    {"en": "Feed", "zh": "動態牆", "sent": "Scroll through the feed.", "sentZh": "滑動態牆。"},
    {"en": "Story", "zh": "限時動態", "sent": "Post a story.", "sentZh": "發佈限時動態。"},
    {"en": "Reel / Short", "zh": "短影音", "sent": "Reels are very popular.", "sentZh": "短影音非常受歡迎。"},
    {"en": "Live Stream", "zh": "直播", "sent": "He is doing a live stream.", "sentZh": "他正在直播。"},
    {"en": "Meme", "zh": "迷因/梗圖", "sent": "Send me that meme.", "sentZh": "傳那張梗圖給我。"},
    {"en": "Troll", "zh": "酸民/引戰者", "sent": "Don't feed the trolls.", "sentZh": "別理會酸民。"},
    {"en": "Block", "zh": "封鎖", "sent": "I had to block him.", "sentZh": "我不得不封鎖他。"},
    {"en": "Filter", "zh": "濾鏡", "sent": "No filter needed.", "sentZh": "不需要濾鏡。"},
    {"en": "Tag", "zh": "標記", "sent": "Tag me in the photo.", "sentZh": "在照片裡標記我。"},
    {"en": "Caption", "zh": "貼文說明", "sent": "Write a funny caption.", "sentZh": "寫個有趣的貼文說明。"},
    {"en": "Platform", "zh": "平台", "sent": "Which platform do you use?", "sentZh": "你使用哪個平台？"},
    {"en": "Community", "zh": "社群", "sent": "Build a loyal community.", "sentZh": "建立忠實的社群。"}
]

def generate_day(day_num):
    filename = f"c:/Users/ian20/OneDrive/桌面/English/Social_Day{day_num}.html"
    title = f"Day {day_num} - Social Media"
    
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
