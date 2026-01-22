import os
import glob
import re

def patch_file(filepath):
    # Skip SimRacing content as it's already patched
    if "SimRacing_" in filepath:
        # Check if we need to skip or confirm. 
        # The user said "in OTHER categories". 
        # But if I re-patch SimRacing, it might be safer to just check "startListening()" presence.
        pass

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)

    if "startListening()" in content and "SimRacing" not in filepath:
        print(f"Skipping {filename} - already patched.")
        return
    elif "startListening()" in content and "SimRacing" in filepath:
        # SimRacing already done, skip silently
        return

    # --- 1. Identify Button Color ---
    # Different themes have different button styles.
    # Default: Yellow (#f1c40f) or something fitting.
    # TOEIC uses .btn-quiz (red). 
    # Let's use a distinct color like Yellow/Orange for Listening.
    listening_btn_color = "background-color: #f1c40f; color: #000;"

    nav_injection = f"""
        <button class="btn btn-quiz" onclick="startListening()" style="{listening_btn_color}"><span>👂 Listening</span></button>"""
    
    # --- 2. Inject Nav Button ---
    # Find startQuiz button
    # Pattern 1: onclick="startQuiz()">... (standard)
    # Pattern 2: onclick="startQuiz()">📝 開始測驗</button> (TOEIC)
    # Pattern 3: onclick="startQuiz()"><span>🏁 開始比賽</span></button> (SimRacing)
    
    # Regex to find the startQuiz button tag
    # <button ... onclick="startQuiz()" ...> ... </button>
    # We want to append our button AFTER this button.
    
    # Simplest approach: Replace the CLOSE tag of the startQuiz button.
    # But finding the correct close tag is tricky.
    
    # Safer approach: Look for `onclick="startQuiz()"` line and append to it if it fits on one line?
    # Most generated files have one button per line or standard formatting.
    
    if 'onclick="startQuiz()"' in content:
        # We need to find the specific string that closes this button.
        # Most of them end with `</button>`
        # Let's try to match the whole tag using regex?
        # Or just find the substring `onclick="startQuiz()"` and find the next `</button>`
        
        idx = content.find('onclick="startQuiz()"')
        if idx != -1:
            close_btn_idx = content.find('</button>', idx)
            if close_btn_idx != -1:
                # Insert after </button>
                insertion_point = close_btn_idx + 9 # len('</button>')
                content = content[:insertion_point] + nav_injection + content[insertion_point:]
            else:
                print(f"Warn: No closing button tag found for {filename}")
                return
    else:
        print(f"Warn: No startQuiz button found for {filename}")
        return

    # --- 3. Inject HTML Section ---
    # Insert before <script> tag (or before initLearn calls if script is huge, but usually before script is safe)
    # We used "before <script>" in SimRacing. Let's stick to that.
    # NOTE: Some files might have multiple scripts. We want the one defining wordsDB.
    # Usually it's the last big script block.
    
    listen_html = """
    <div id="listen-section" style="display: none; text-align: center;">
        <div id="listen-container">
            <div class="question-word" style="font-size: 80px; margin-bottom: 20px;">🔊</div>
            <button class="btn" onclick="playCurrentAudio()" style="margin-bottom: 30px; background: #fff; color: #333; border: 1px solid #ccc;">▶️ Replay</button>
            <div class="options-grid" id="listen-options-area"></div>
            <div id="listen-result-msg"></div>
        </div>
        <div id="listen-final-score" style="display:none;" class="score-board"></div>
        <button id="listen-restart-btn" class="btn btn-learn" style="display:none; margin-top:20px;" onclick="startListening()"><span>🔄 Retry</span></button>
    </div>
    """
    
    # Insert before the script that contains wordsDB
    if 'const wordsDB =' in content or 'let wordsDB =' in content:
        # Find the <script that contains this
        # Easier: just insert before the LAST <div style="text-align: center; margin-top: 40px... "> (Mark Complete button)
        # OR just insert before the <script> tag that follows </div> of main container.
        # In standardized files: ... </div> ... <script>
        
        # Let's try identifying <script> lines.
        # We want to insert BEFORE the script that has wordsDB.
        
        # Method: Replace `const wordsDB =` with `listen_html + <script>... const wordsDB =`?
        # No, that breaks the script tag.
        
        # Method: Find where the main container ends? `</div>` followed by `<script>`.
        patt = r'(</div>\s*<script>\s*const wordsDB)'
        match = re.search(patt, content, re.DOTALL)
        if match:
            # We found the transition. Insert html in between.
            # match.group(1) is `</div>\n<script>\nconst wordsDB`
            # We want `</div>` + listen_html + `<script>...`
            # Wait, regex is tricky.
            
            # Simple string replace:
            # most files have:
            # </div>
            #
            # <script>
            #     const wordsDB ...
            
            # Let's search for `<script>` and check if `wordsDB` follows shortly.
            pass
        
        # Let's fallback to "Before the last <script>" or "Before the script containing wordsDB"
        # We can scan the file line by line?
        pass
    
    # Robust placement: Find `<div id="quiz-section">` ... `</div>` (closing quiz) ... `</div>` (closing container).
    # Then insert.
    # Or just insert before `<script>` tag.
    
    # Let's use `.replace('<script>', ...)` but only the one that starts the logic.
    # There are usually 3 scripts:
    # 1. (Optional) Top
    # 2. Main logic
    # 3. Mark Complete logic (bottom)
    
    # We want the Main Logic one.
    # It usually starts with `const wordsDB` or `var wordsDB`.
    
    # Strategy: Find `<script>` index, check if `wordsDB` is in the next 500 chars.
    script_indices = [m.start() for m in re.finditer(r'<script>', content)]
    target_script_idx = -1
    for idx in script_indices:
        chunk = content[idx:idx+500]
        if 'wordsDB' in chunk:
            target_script_idx = idx
            break
            
    if target_script_idx != -1:
        # Insert HTML before this script tag
        content = content[:target_script_idx] + listen_html + '\n' + content[target_script_idx:]
    else:
        print(f"Warn: Could not locate main script in {filename}")
        return

    # --- 4. Inject JS Logic ---
    # Need to properly detect where to insert the JS functions.
    # Before `initLearn();` is a good spot.
    
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
    else:
        print(f"Warn: initLearn() not found in {filename}")
        return

    # --- 5. Update showSection ---
    # We replace the closing brace `}` of showSection with the newLine?
    # Or replace the whole line if we can match it.
    
    # Generic matcher:
    # function showSection(section) {
    #    ...
    # }
    
    if 'function showSection(section)' in content:
        # We need to inject the `listen` toggle.
        # Find the function body start
        start_idx = content.find('function showSection(section)')
        # Find the closing brace? Checking syntax is hard.
        # Simpler: find the line `document.getElementById('quiz-section').style.display =` ...
        # And append the listen line after it.
        
        quiz_display_matcher = r"document\.getElementById\('quiz-section'\)\.style\.display\s*=\s*section\s*===\s*'quiz'\s*\?\s*'block'\s*:\s*'none';"
        match = re.search(quiz_display_matcher, content)
        if match:
             # Found the quiz line. Append listen line.
            param = "'listen'"
            block = "'block'"
            none = "'none'"
            # Use raw string for injection to avoid escaping issues
            injection = f"\n        document.getElementById('listen-section').style.display = section === 'listen' ? 'block' : 'none';"
            
            # Replace the match with match + injection
            content = content[:match.end()] + injection + content[match.end():]
        else:
             print(f"Warn: Could not match showSection logic in {filename}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filename}")

def main():
    # Target all Day HTML files
    files = glob.glob("c:/Users/ian20/OneDrive/桌面/English/*_Day*.html")
    print(f"Found {len(files)} files.")
    for f in files:
        patch_file(f)

if __name__ == "__main__":
    main()
