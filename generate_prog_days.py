import os
import json
import random

# Dark Theme Template with "Techno/IDE" feel
TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Programming English - {title}</title>
    <style>
        /* Dark Theme Variables */
        :root {{
            --bg-color: #0f172a; /* Deep Blue/Black */
            --card-bg: #1e293b;  /* Slate 800 */
            --text-main: #e2e8f0; /* Slate 200 */
            --text-sub: #94a3b8;  /* Slate 400 */
            --accent-primary: #38bdf8; /* Sky Blue (Cyan) */
            --accent-secondary: #818cf8; /* Indigo */
            --success: #4ade80;   /* Green */
            --error: #f87171;     /* Red */
            --tech-font: 'Consolas', 'Monaco', 'Courier New', monospace;
        }}

        body {{ 
            font-family: 'Segoe UI', sans-serif; 
            background-color: var(--bg-color); 
            /* Subtle Grid Pattern for "Texture" */
            background-image: linear-gradient(#1e293b 1px, transparent 1px), linear-gradient(90deg, #1e293b 1px, transparent 1px);
            background-size: 30px 30px;
            margin: 0; padding: 20px; 
            color: var(--text-main); 
        }}
        
        .container {{ 
            max-width: 800px; margin: 0 auto; 
            background: var(--card-bg); 
            padding: 30px; 
            border-radius: 16px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); 
            border: 1px solid #334155;
        }}

        h1 {{ 
            text-align: center; color: var(--accent-primary); 
            border-bottom: 2px solid var(--accent-secondary); 
            padding-bottom: 15px; 
            text-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
        }}
        
        /* Navigation Buttons */
        .nav {{ display: flex; justify-content: center; gap: 20px; margin-bottom: 30px; }}
        .btn {{ 
            padding: 10px 25px; border: none; border-radius: 8px; cursor: pointer; 
            font-size: 16px; transition: 0.3s; font-weight: bold; 
            font-family: var(--tech-font);
        }}
        .btn-learn {{ background-color: var(--accent-primary); color: #0f172a; }}
        .btn-quiz {{ background-color: var(--accent-secondary); color: white; }}
        .btn:hover {{ opacity: 0.9; transform: translateY(-2px); box-shadow: 0 0 15px rgba(56, 189, 248, 0.4); }}

        /* Learning Mode Cards */
        .word-card {{ 
            border-left: 5px solid var(--accent-primary); 
            background: #0f172a; /* Darker inner card */
            padding: 20px; margin-bottom: 20px; 
            border-radius: 8px; 
            border: 1px solid #334155;
        }}
        .word-header {{ display: flex; align-items: center; gap: 15px; margin-bottom: 10px; }}
        .english-word {{ 
            font-size: 24px; font-weight: bold; color: var(--accent-primary); 
            font-family: var(--tech-font);
        }}
        .speak-btn {{ 
            background: rgba(255,255,255,0.1); border: 1px solid #475569; 
            border-radius: 50%; width: 32px; height: 32px; color: var(--text-main);
            cursor: pointer; display: flex; align-items: center; justify-content: center; transition: 0.2s; 
        }}
        .speak-btn:hover {{ background: rgba(56, 189, 248, 0.2); border-color: var(--accent-primary); }}
        .meaning {{ color: var(--success); font-weight: bold; font-size: 20px; }}
        
        .sentence-box {{ margin-top: 10px; padding-top: 10px; border-top: 1px dashed #334155; }}
        .sentence {{ font-style: italic; color: #cbd5e1; font-size: 1.1em; margin-bottom: 4px; font-family: var(--tech-font); }}
        .sentence-zh {{ color: var(--text-sub); font-size: 0.95em; }}

        /* Quiz Mode */
        #quiz-section {{ display: none; text-align: center; }}
        .question-word {{ 
            font-size: 32px; font-weight: bold; margin-bottom: 30px; 
            color: var(--accent-primary); font-family: var(--tech-font);
        }}
        .options-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        .option-btn {{ 
            background: #1e293b; border: 2px solid #475569; color: var(--text-main);
            padding: 20px; border-radius: 12px; cursor: pointer; font-size: 18px; transition: 0.2s; 
        }}
        .option-btn:hover {{ background-color: #334155; border-color: var(--accent-primary); }}
        .option-btn:disabled {{ opacity: 0.6; cursor: not-allowed; }}
        
        .result-message {{ font-size: 22px; font-weight: bold; margin-top: 25px; padding: 15px; border-radius: 12px; }}
        .correct {{ color: #064e3b; background: var(--success); text-shadow: none; box-shadow: 0 0 10px var(--success); }}
        .wrong {{ color: #7f1d1d; background: var(--error); box-shadow: 0 0 10px var(--error); }}
        .score-board {{ font-size: 28px; color: var(--accent-primary); font-weight: bold; margin-top: 30px; }}
    </style>
</head>
<body>

<div class="container">
    <h1>{title}</h1>
    
    <div class="nav">
        <a href="index.html" class="btn btn-learn" style="text-decoration:none; display:inline-flex; align-items:center; justify-content:center;">🏠 主選單</a>
        <button class="btn btn-learn" onclick="showSection('learn')">📖 學習模式</button>
        <button class="btn btn-quiz" onclick="startQuiz()">📝 挑戰測驗</button>
    </div>

    <div id="learn-section"></div>

    <div id="quiz-section">
        <div id="quiz-container">
            <div class="question-word" id="q-word">Word</div>
            <div class="options-grid" id="options-area"></div>
            <div id="result-msg"></div>
        </div>
        <div id="final-score" style="display:none;" class="score-board"></div>
        <button id="restart-btn" class="btn btn-learn" style="display:none; margin-top:20px;" onclick="startQuiz()">🔄 重新挑戰</button>
    </div>
</div>

<script>
    const wordsDB = {json_data};

    function initLearn() {{
        const container = document.getElementById('learn-section');
        container.innerHTML = '';
        wordsDB.forEach(item => {{
            const card = document.createElement('div');
            card.className = 'word-card';
            card.innerHTML = `
                <div class="word-header">
                    <span class="english-word">${{item.en}}</span>
                    <button class="speak-btn" onclick="speak('${{item.en}}')" title="發音">🔊</button>
                    <span class="meaning">${{item.zh}}</span>
                </div>
                <div class="sentence-box">
                    <div class="sentence">"${{item.sent}}"</div>
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
            resultDiv.textContent = "✅ 正確 Correct!";
            resultDiv.className = "result-message correct";
        }} else {{
            resultDiv.textContent = `❌ 錯誤! 正解是: ${{correct}}`;
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
        let report = `測驗結束!<br>你的分數: ${{score}} / ${{wordsDB.length}}`;
        if (wrongAnswers.length > 0) {{
            report += '<div style="margin-top:20px; text-align:left; background:#24283b; padding:15px; border-radius:10px; border:1px solid #f87171;">';
            report += '<h3 style="color:#f87171; margin-top:0;">需複習單字 (Incorrect):</h3><ul style="padding-left:20px; color:#cbd5e1;">';
            wrongAnswers.forEach(w => {{
                report += `<li style="margin-bottom:5px;"><strong>${{w.en}}</strong>: <span style="color:#4ade80;">${{w.zh}}</span> <span style="color:#64748b; font-size:0.9em;">(你選了: ${{w.selected}})</span></li>`;
            }});
            report += '</ul></div>';
        }}
        scoreBoard.innerHTML = report;
        document.getElementById('restart-btn').style.display = 'inline-block';
    }}

    initLearn();
</script>
</body>
</html>"""

# DATA
DATA = {}
# Day 1: Basic Terms (Restored)
DATA[1] = ("Day 1 - 基礎術語 (Basics)", [
    {"en": "variable", "zh": "變數", "sent": "A variable stores a value.", "sentZh": "變數儲存一個數值。"},
    {"en": "function", "zh": "函式", "sent": "Call the function to execute code.", "sentZh": "呼叫函式來執行程式碼。"},
    {"en": "array", "zh": "陣列", "sent": "An array is a list of items.", "sentZh": "陣列是項目的列表。"},
    {"en": "integer", "zh": "整數", "sent": "5 is an integer.", "sentZh": "5 是一個整數。"},
    {"en": "string", "zh": "字串", "sent": "Strings are text data.", "sentZh": "字串是文字資料。"},
    {"en": "boolean", "zh": "布林值", "sent": "True or False.", "sentZh": "真或假。"},
    {"en": "loop", "zh": "迴圈", "sent": "Loops repeat actions.", "sentZh": "迴圈重複動作。"},
    {"en": "condition", "zh": "條件", "sent": "If-else is a condition.", "sentZh": "If-else 是一個條件。"},
    {"en": "syntax", "zh": "語法", "sent": "Check your syntax.", "sentZh": "檢查您的語法。"},
    {"en": "bug", "zh": "錯誤", "sent": "There is a bug in the code.", "sentZh": "程式碼中有一個錯誤。"},
    {"en": "debug", "zh": "除錯", "sent": "Use console to debug.", "sentZh": "使用控制台除錯。"},
    {"en": "compile", "zh": "編譯", "sent": "Compile the source code.", "sentZh": "編譯原始碼。"},
    {"en": "execute", "zh": "執行", "sent": "Execute the program.", "sentZh": "執行程式。"},
    {"en": "database", "zh": "資料庫", "sent": "Save to database.", "sentZh": "存入資料庫。"},
    {"en": "algorithm", "zh": "演算法", "sent": "Sorting algorithms are fast.", "sentZh": "排序演算法很快。"},
    {"en": "parameter", "zh": "參數", "sent": "Define function parameters.", "sentZh": "定義函式參數。"},
    {"en": "argument", "zh": "引數", "sent": "Pass arguments to function.", "sentZh": "傳遞引數給函式。"},
    {"en": "return", "zh": "回傳", "sent": "Return the result.", "sentZh": "回傳結果。"},
    {"en": "class", "zh": "類別", "sent": "Class defines objects.", "sentZh": "類別定義物件。"},
    {"en": "object", "zh": "物件", "sent": "Create a new object.", "sentZh": "建立一個新物件。"}
])

# Day 2: Frontend
DATA[2] = ("Day 2 - 前端開發 (Frontend)", [
    {"en": "element", "zh": "元素", "sent": "HTML elements structure the document.", "sentZh": "HTML 元素構建了文件結構。"},
    {"en": "attribute", "zh": "屬性", "sent": "The 'href' attribute specifies the link URL.", "sentZh": "'href' 屬性指定連結網址。"},
    {"en": "responsive", "zh": "響應式", "sent": "Responsive design works on mobile devices.", "sentZh": "響應式設計適用於行動裝置。"},
    {"en": "selector", "zh": "選擇器", "sent": "Use CSS selectors to style elements.", "sentZh": "使用 CSS 選擇器來設定元素樣式。"},
    {"en": "property", "zh": "屬性 (CSS)", "sent": "Color is a CSS property.", "sentZh": "顏色是一個 CSS 屬性。"},
    {"en": "framework", "zh": "框架", "sent": "Vue.js is a progressive framework.", "sentZh": "Vue.js 是一個漸進式框架。"},
    {"en": "library", "zh": "函式庫", "sent": "React is a UI library.", "sentZh": "React 是一個 UI 函式庫。"},
    {"en": "component", "zh": "組件", "sent": "Break the UI into small components.", "sentZh": "將 UI 拆分為小組件。"},
    {"en": "DOM", "zh": "文件物件模型", "sent": "The DOM represents the page structure.", "sentZh": "DOM 代表頁面結構。"},
    {"en": "event", "zh": "事件", "sent": "Button click is a common event.", "sentZh": "按鈕點擊是一個常見事件。"},
    {"en": "listener", "zh": "監聽器", "sent": "Add an event listener to the button.", "sentZh": "為按鈕新增事件監聽器。"},
    {"en": "callback", "zh": "回呼函式", "sent": "The callback runs after the request finishes.", "sentZh": "回呼函式在請求完成後執行。"},
    {"en": "async", "zh": "非同步", "sent": "Async code doesn't block execution.", "sentZh": "非同步程式碼不會阻塞執行。"},
    {"en": "promise", "zh": "承諾 (Promise)", "sent": "A Promise handles async operations.", "sentZh": "Promise 處理非同步操作。"},
    {"en": "fetch", "zh": "獲取", "sent": "Use fetch API to get data.", "sentZh": "使用 fetch API 獲取資料。"},
    {"en": "state", "zh": "狀態", "sent": "Manage application state carefully.", "sentZh": "小心管理應用程式狀態。"},
    {"en": "props", "zh": "屬性 (Props)", "sent": "Pass data to child components via props.", "sentZh": "透過 props 傳遞資料給子組件。"},
    {"en": "hook", "zh": "掛鉤 (Hook)", "sent": "React Hooks manage state logic.", "sentZh": "React Hooks 管理狀態邏輯。"},
    {"en": "render", "zh": "渲染", "sent": "The browser renders the HTML.", "sentZh": "瀏覽器渲染 HTML。"},
    {"en": "bundle", "zh": "打包", "sent": "Webpack bundles your assets.", "sentZh": "Webpack 打包您的資源。"}
])

# Day 3: Backend
DATA[3] = ("Day 3 - 後端與 API (Backend)", [
    {"en": "server", "zh": "伺服器", "sent": "The server handles requests.", "sentZh": "伺服器處理請求。"},
    {"en": "client", "zh": "客戶端", "sent": "The client displays the UI.", "sentZh": "客戶端顯示 UI。"},
    {"en": "request", "zh": "請求", "sent": "GET request retrieves data.", "sentZh": "GET 請求檢索資料。"},
    {"en": "response", "zh": "回應", "sent": "The server sent a 200 OK response.", "sentZh": "伺服器發送了 200 OK 回應。"},
    {"en": "endpoint", "zh": "端點", "sent": "The API user endpoint is /users.", "sentZh": "API 使用者端點是 /users。"},
    {"en": "status", "zh": "狀態", "sent": "Check the HTTP status code.", "sentZh": "檢查 HTTP 狀態碼。"},
    {"en": "header", "zh": "標頭", "sent": "Headers contain metadata.", "sentZh": "標頭包含元數據。"},
    {"en": "payload", "zh": "負載/資料包", "sent": "The payload contains the actual data.", "sentZh": "負載包含實際資料。"},
    {"en": "method", "zh": "方法", "sent": "HTTP methods include GET and POST.", "sentZh": "HTTP 方法包括 GET 和 POST。"},
    {"en": "authentication", "zh": "驗證", "sent": "Login requires authentication.", "sentZh": "登入需要驗證。"},
    {"en": "authorization", "zh": "授權", "sent": "Admin access requires authorization.", "sentZh": "管理員存取需要授權。"},
    {"en": "token", "zh": "代幣/憑證", "sent": "Use a JWT token for secure access.", "sentZh": "使用 JWT 憑證進行安全存取。"},
    {"en": "middleware", "zh": "中介軟體", "sent": "Middleware logs every request.", "sentZh": "中介軟體記錄每個請求。"},
    {"en": "router", "zh": "路由器", "sent": "The router directs traffic.", "sentZh": "路由器引導流量。"},
    {"en": "controller", "zh": "控制器", "sent": "The controller handles logic.", "sentZh": "控制器處理邏輯。"},
    {"en": "model", "zh": "模型", "sent": "The model represents data structure.", "sentZh": "模型代表資料結構。"},
    {"en": "service", "zh": "服務", "sent": "Business logic lives in the service layer.", "sentZh": "商業邏輯存在於服務層。"},
    {"en": "deploy", "zh": "部署", "sent": "Deploy to production server.", "sentZh": "部署到生產伺服器。"},
    {"en": "environment", "zh": "環境", "sent": "Set up the development environment.", "sentZh": "設定開發環境。"},
    {"en": "scalability", "zh": "可擴展性", "sent": "Microservices improve scalability.", "sentZh": "微服務提高可擴展性。"}
])

# Extensive pool of words for generation
POOL = [
    # General CS
    {"en": "algorithm", "zh": "演算法", "sent": "Binary search is an efficient algorithm.", "sentZh": "二分搜尋是一種高效的演算法。"},
    {"en": "structure", "zh": "結構", "sent": "Data structure organizes data.", "sentZh": "資料結構組織資料。"},
    {"en": "binary", "zh": "二進位", "sent": "Computers use binary logic.", "sentZh": "電腦使用二進位邏輯。"},
    {"en": "hexadecimal", "zh": "十六進位", "sent": "Colors are often in hexadecimal.", "sentZh": "顏色通常是十六進位的。"},
    {"en": "bit", "zh": "位元", "sent": "A bit is 0 or 1.", "sentZh": "位元是 0 或 1。"},
    {"en": "byte", "zh": "位元組", "sent": "8 bits make a byte.", "sentZh": "8 個位元組成一個位元組。"},
    # Data Structures
    {"en": "stack", "zh": "堆疊", "sent": "Stack follows LIFO principle.", "sentZh": "堆疊遵循 LIFO 原則。"},
    {"en": "queue", "zh": "佇列", "sent": "Queue follows FIFO principle.", "sentZh": "佇列遵循 FIFO 原則。"},
    {"en": "tree", "zh": "樹狀結構", "sent": "A binary tree has two children nodes.", "sentZh": "二元樹有兩個子節點。"},
    {"en": "graph", "zh": "圖形", "sent": "Graphs model network connections.", "sentZh": "圖形模擬網路連接。"},
    {"en": "node", "zh": "節點", "sent": "Each node contains data.", "sentZh": "每個節點包含資料。"},
    {"en": "edge", "zh": "邊", "sent": "Edges connect nodes in a graph.", "sentZh": "邊連接圖形中的節點。"},
    {"en": "hash", "zh": "雜湊", "sent": "Hash functions map data to keys.", "sentZh": "雜湊函式將資料對應到鍵值。"},
    {"en": "linked list", "zh": "連結串列", "sent": "Linked lists are dynamic.", "sentZh": "連結串列是動態的。"},
    # Security
    {"en": "encryption", "zh": "加密", "sent": "SSL uses encryption for security.", "sentZh": "SSL 使用加密來確保安全。"},
    {"en": "decryption", "zh": "解密", "sent": "Decryption requires a private key.", "sentZh": "解密需要私鑰。"},
    {"en": "firewall", "zh": "防火牆", "sent": "Configure the firewall rules.", "sentZh": "設定防火牆規則。"},
    {"en": "vulnerability", "zh": "漏洞", "sent": "Patch the security vulnerability.", "sentZh": "修補安全漏洞。"},
    {"en": "exploit", "zh": "利用(漏洞)", "sent": "Hackers exploit weaknesses.", "sentZh": "駭客利用弱點。"},
    # Networking
    {"en": "protocol", "zh": "協定", "sent": "TCP is a reliable protocol.", "sentZh": "TCP 是一個可靠的協定。"},
    {"en": "latency", "zh": "延遲", "sent": "Reduce network latency.", "sentZh": "減少網路延遲。"},
    {"en": "bandwidth", "zh": "頻寬", "sent": "High bandwidth is needed for video.", "sentZh": "影片需要高頻寬。"},
    {"en": "throughput", "zh": "吞吐量", "sent": "Increase the system throughput.", "sentZh": "增加系統吞吐量。"},
    {"en": "dns", "zh": "DNS", "sent": "DNS resolves domain names.", "sentZh": "DNS 解析網域名稱。"},
    # Cloud
    {"en": "cloud", "zh": "雲端", "sent": "AWS is a cloud provider.", "sentZh": "AWS 是一個雲端供應商。"},
    {"en": "virtualization", "zh": "虛擬化", "sent": "VMware provides virtualization.", "sentZh": "VMware 提供虛擬化。"},
    {"en": "container", "zh": "容器", "sent": "Docker containers are lightweight.", "sentZh": "Docker 容器是輕量級的。"},
    {"en": "orchestration", "zh": "編排", "sent": "Kubernetes handles orchestration.", "sentZh": "Kubernetes 處理編排。"},
    {"en": "serverless", "zh": "無伺服器", "sent": "Serverless functions scale auto.", "sentZh": "無伺服器函式自動擴展。"},
    # Agile
    {"en": "agile", "zh": "敏捷", "sent": "Agile methodology focuses on speed.", "sentZh": "敏捷方法論著重於速度。"},
    {"en": "scrum", "zh": "Scrum", "sent": "Daily scrum meetings keep us synced.", "sentZh": "每日 Scrum 會議讓我們保持同步。"},
    {"en": "sprint", "zh": "衝刺", "sent": "The sprint lasts two weeks.", "sentZh": "這個衝刺持續兩週。"},
    {"en": "backlog", "zh": "待辦清單", "sent": "Prioritize tasks in the backlog.", "sentZh": "優先處理待辦清單中的任務。"},
    {"en": "user story", "zh": "使用者故事", "sent": "Write user stories for features.", "sentZh": "為功能撰寫使用者故事。"},
    {"en": "kanban", "zh": "看板", "sent": "Use a Kanban board to track progress.", "sentZh": "使用看板來追蹤進度。"},
    # DevOps
    {"en": "integration", "zh": "整合", "sent": "Continuous integration (CI) is key.", "sentZh": "持續整合 (CI) 是關鍵。"},
    {"en": "delivery", "zh": "交付", "sent": "Continuous delivery updates software.", "sentZh": "持續交付更新軟體。"},
    {"en": "pipeline", "zh": "管線", "sent": "Build pipeline failed.", "sentZh": "建置管線失敗。"},
    {"en": "artifact", "zh": "產出物", "sent": "Store build artifacts.", "sentZh": "儲存建置產出物。"},
    # AI/ML
    {"en": "machine learning", "zh": "機器學習", "sent": "ML models learn from data.", "sentZh": "機器學習模型從資料中學習。"},
    {"en": "artificial intelligence", "zh": "人工智慧", "sent": "AI powers smart assistants.", "sentZh": "人工智慧驅動智慧助理。"},
    {"en": "neural network", "zh": "神經網路", "sent": "Deep learning uses neural networks.", "sentZh": "深度學習使用神經網路。"},
    {"en": "dataset", "zh": "資料集", "sent": "Clean the dataset before training.", "sentZh": "訓練前清理資料集。"},
    {"en": "training", "zh": "訓練", "sent": "Model training takes time.", "sentZh": "模型訓練需要時間。"},
    # Design
    {"en": "interface", "zh": "介面", "sent": "The UI should be intuitive.", "sentZh": "使用者介面應該直觀。"},
    {"en": "experience", "zh": "體驗", "sent": "UX focuses on user satisfaction.", "sentZh": "UX 著重於使用者滿意度。"},
    {"en": "accessibility", "zh": "無障礙", "sent": "Web accessibility is important.", "sentZh": "網頁無障礙性很重要。"},
    {"en": "wireframe", "zh": "線框圖", "sent": "Design a wireframe first.", "sentZh": "先設計線框圖。"},
    {"en": "prototype", "zh": "原型", "sent": "Test the interactive prototype.", "sentZh": "測試互動原型。"},
]

def generate_day(day_num):
    filename = f"c:/Users/ian20/OneDrive/桌面/English/Programming_Day{day_num}.html"
    
    # Determine Title and Content
    if day_num in DATA:
        title, words = DATA[day_num]
    else:
        title = f"Day {day_num} - 進階程式術語 (Advanced)"
        # Random pick 20
        words = random.sample(POOL, 20)

    # Ensure list is exactly 20
    while len(words) < 20: 
        words.append({"en": "Extra", "zh": "額外", "sent": "Bonus word.", "sentZh": "額外單字。"})
        
    html_content = TEMPLATE.format(title=title, json_data=json.dumps(words, ensure_ascii=False))
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated {filename}")

def main():
    # Update ALL days 1-30 to match the new Dark Theme
    for i in range(1, 31):
        generate_day(i)

if __name__ == "__main__":
    main()
