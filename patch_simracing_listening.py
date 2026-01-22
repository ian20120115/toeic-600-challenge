import os
import glob

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if "startListening()" in content:
        print(f"Skipping {filepath} - already patched.")
        return

    # 1. Inject Nav Button
    # Find the quiz button and add listening button after it
    # Pattern: <button class="btn btn-quiz" onclick="startQuiz()"><span>🏁 開始比賽</span></button>
    if 'onclick="startQuiz()">' in content:
        nav_injection = """
        <button class="btn btn-quiz" onclick="startListening()" style="background-color: #f1c40f; color: #000;"><span>👂 聽力測驗</span></button>"""
        # Insert before the closing div of nav if possible, or after startQuiz button
        # SimRacing uses: <div class="nav"> ... <button ... startQuiz ...> ... </div>
        # Let's simple replace the closing </div> of nav
        # But wait, finding the exact location is safer with replace on the button line.
        
        # SimRacing specific target
        target_btn = 'onclick="startQuiz()"><span>🏁 開始比賽</span></button>'
        replacement_btn = target_btn + nav_injection
        content = content.replace(target_btn, replacement_btn)
    else:
        print(f"Warning: Could not find nav button in {filepath}")

    # 2. Inject HTML Section
    # Insert after quiz-section div
    # Pattern: <div id="quiz-section">...</div> (This might be multiline)
    # Strategy: Find <div id="quiz-section"> and find the matching closing div? Hard with regex.
    # Alternative: Find the line `    <div id="quiz-section">` ...
    # Easier: Find where `.container` ends?
    # SimRacing has `    <div id="quiz-section">` ... `    </div>` then `</div>` (closing container).
    
    # Let's search for `<div id="quiz-section">` and find the next `<div id="final-score"` inside it to locate context,
    # OR better: Insert before `</div>` (closing container) if we know the structure.
    # Structure:
    # <div class="container">
    #    ...
    #    <div id="quiz-section">...</div>
    # </div>
    
    # We can look for `    <div id="quiz-section">` and insert our new section BEFORE it? No, maybe after.
    # Actually, inserting before the closing `</div>` of container is risky if there are nested divs.
    # Let's insert BEFORE `<script>` tag that starts `const wordsDB`.
    
    listen_html = """
    <div id="listen-section" style="display: none; text-align: center;">
        <div id="listen-container">
            <div class="question-word" style="font-size: 80px; margin-bottom: 20px;">🔊</div>
            <button class="btn" onclick="playCurrentAudio()" style="margin-bottom: 30px; background: #fff; color: #333;">▶️ Replay Audio</button>
            <div class="options-grid" id="listen-options-area"></div>
            <div id="listen-result-msg"></div>
        </div>
        <div id="listen-final-score" style="display:none;" class="score-board"></div>
        <button id="listen-restart-btn" class="btn btn-learn" style="display:none; margin-top:20px;" onclick="startListening()"><span>🔄 再測一次</span></button>
    </div>
    """
    
    if '<script>' in content:
        # Insert before the FIRST <script> tag that defines wordsDB?
        # Usually there's only one main script block at the bottom (excluding simple ones).
        # We can insert before `<script>`
        content = content.replace('<script>', listen_html + '\n<script>', 1)
    
    # 3. Inject JS Logic
    # We need to insert functions: startListening, loadListeningQuestion, checkListeningAnswer...
    # We can insert them at the end of the script, before `initLearn();`.
    
    js_logic = """
    // --- Listening Mode Logic ---
    let listenQ = 0;
    let listenScore = 0;
    let listenList = [];
    
    function startListening() {
        showSection('listen');
        listenQ = 0;
        listenScore = 0;
        document.getElementById('listen-final-score').style.display = 'none';
        document.getElementById('listen-restart-btn').style.display = 'none';
        document.getElementById('listen-container').style.display = 'block';
        listenList = [...wordsDB].sort(() => 0.5 - Math.random());
        loadListenQ();
    }

    function loadListenQ() {
        if (listenQ >= listenList.length) {
            endListening();
            return;
        }
        const current = listenList[listenQ];
        document.getElementById('listen-result-msg').className = '';
        document.getElementById('listen-result-msg').innerHTML = '';
        
        // Auto play audio
        setTimeout(() => speak(current.en), 300);

        let options = [current.zh];
        while (options.length < 4) {
            const r = wordsDB[Math.floor(Math.random() * wordsDB.length)];
            if (!options.includes(r.zh)) options.push(r.zh);
        }
        options.sort(() => 0.5 - Math.random());

        const area = document.getElementById('listen-options-area');
        area.innerHTML = '';
        options.forEach(opt => {
            const btn = document.createElement('button');
            btn.className = 'option-btn';
            btn.textContent = opt;
            btn.onclick = () => checkListenAns(opt, current.zh);
            area.appendChild(btn);
        });
    }

    function playCurrentAudio() {
        if (listenQ < listenList.length) {
            speak(listenList[listenQ].en);
        }
    }

    function checkListenAns(selected, correct) {
        const resDiv = document.getElementById('listen-result-msg');
        document.querySelectorAll('#listen-options-area .option-btn').forEach(b => b.disabled = true);
        if (selected === correct) {
            listenScore++;
            resDiv.textContent = "✅ Correct!";
            resDiv.className = "result-message correct";
        } else {
            resDiv.textContent = `❌ Wrong! It was: ${correct}`;
            resDiv.className = "result-message wrong";
        }
        setTimeout(() => {
            listenQ++;
            loadListenQ();
        }, 1200);
    }

    function endListening() {
        document.getElementById('listen-container').style.display = 'none';
        const board = document.getElementById('listen-final-score');
        board.style.display = 'block';
        board.innerHTML = `LISTENING SCORE: ${listenScore} / ${wordsDB.length}`;
        document.getElementById('listen-restart-btn').style.display = 'inline-block';
    }
    """
    
    if 'initLearn();' in content:
        content = content.replace('initLearn();', js_logic + '\n    initLearn();')
        
    # 4. Update showSection
    # We need to update showSection to handle 'listen' case
    # Current: document.getElementById('learn-section').style.display = section === 'learn' ? 'block' : 'none';
    #          document.getElementById('quiz-section').style.display = section === 'quiz' ? 'block' : 'none';
    
    new_show_section = """
    function showSection(section) {
        document.getElementById('learn-section').style.display = section === 'learn' ? 'block' : 'none';
        document.getElementById('quiz-section').style.display = section === 'quiz' ? 'block' : 'none';
        document.getElementById('listen-section').style.display = section === 'listen' ? 'block' : 'none';
    }
    """
    
    # We can use regex or simple string replacement to replace the old function
    old_show_patt_start = "function showSection(section) {"
    # Since exact content varies, let's just REPLACE the function entirely if we can identify it unique enough.
    # The generated file likely has exact spacing.
    
    # Let's try to match the body lines
    # document.getElementById('learn-section').style.display = section === 'learn' ? 'block' : 'none';
    target_line = "document.getElementById('learn-section').style.display = section === 'learn' ? 'block' : 'none';"
    if target_line in content:
        # We replace the whole function logic or just append the third line
        replacement_line = target_line + "\n        document.getElementById('listen-section').style.display = section === 'listen' ? 'block' : 'none';"
        content = content.replace(target_line, replacement_line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")

def main():
    files = glob.glob("c:/Users/ian20/OneDrive/桌面/English/SimRacing_Day*.html")
    for f in files:
        patch_file(f)

if __name__ == "__main__":
    main()
