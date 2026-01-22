import os
import random

def get_header(day, part_name):
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TOEIC Listening - Day {day} - {part_name}</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background-color: #f3e5f5; margin: 0; padding: 20px; color: #333; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        h1 {{ text-align: center; color: #8e44ad; border-bottom: 2px solid #9b59b6; padding-bottom: 15px; }}
        .nav {{ display: flex; justify-content: center; gap: 15px; margin-bottom: 30px; }}
        .btn {{ padding: 10px 25px; border: none; border-radius: 50px; cursor: pointer; font-size: 16px; transition: 0.3s; font-weight: bold; background: #8e44ad; color: white; text-decoration: none; }}
        .btn:hover {{ transform: translateY(-2px); box-shadow: 0 4px 10px rgba(142, 68, 173, 0.3); }}
        
        .question-card {{ background: #fff; border: 1px solid #ddd; padding: 20px; margin-bottom: 25px; border-radius: 10px; }}
        .audio-btn {{ background: #333; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; font-size: 14px; display: inline-flex; align-items: center; gap: 5px; }}
        .audio-btn:hover {{ background: #555; }}
        
        .options-grid {{ display: grid; gap: 10px; margin-top: 15px; }}
        .option-label {{ display: flex; align-items: center; padding: 10px; border: 2px solid #eee; border-radius: 8px; cursor: pointer; transition: 0.2s; }}
        .option-label:hover {{ background: #f9f9f9; border-color: #8e44ad; }}
        .option-label input {{ margin-right: 15px; transform: scale(1.2); }}
        
        .part-label {{ display: inline-block; background: #9b59b6; color: white; padding: 5px 10px; border-radius: 5px; font-size: 0.8em; margin-bottom: 10px; }}
        
        .feedback {{ margin-top: 10px; font-weight: bold; display: none; padding: 10px; border-radius: 5px; }}
        .correct {{ background: #d4edda; color: #155724; }}
        .incorrect {{ background: #f8d7da; color: #721c24; }}

        /* Part specific styles */
        .photo-placeholder {{ width: 100%; height: 300px; background: #eee; display: flex; align-items: center; justify-content: center; color: #888; font-size: 1.2em; border-radius: 8px; margin-bottom: 15px; }}
    </style>
</head>
<body>
<div class="container">
    <h1>🎧 Day {day} - {part_name}</h1>
    <div class="nav">
        <a href="index.html" class="btn">🏠 Home</a>
    </div>
"""

def get_footer(day):
    return f"""
    <div style="text-align: center; margin-top: 40px; margin-bottom: 20px;">
        <button onclick="markComplete()" style="padding: 15px 30px; background: #27ae60; color: white; border: none; border-radius: 50px; font-size: 18px; cursor: pointer; font-weight: bold; box-shadow: 0 4px 15px rgba(39,174,96,0.3);">✅ Mark Complete</button>
    </div>
</div>
<script>
    function playAudio(text) {{
        window.speechSynthesis.cancel();
        const utt = new SpeechSynthesisUtterance(text);
        utt.lang = 'en-US';
        utt.rate = 0.9;
        window.speechSynthesis.speak(utt);
    }}

    function checkAnswer(qId, correctVal) {{
        const selected = document.querySelector(`input[name="q${{qId}}"]:checked`);
        const feedback = document.getElementById(`fb-${{qId}}`);
        if (!selected) return;
        
        feedback.style.display = 'block';
        if (selected.value === correctVal) {{
            feedback.textContent = "✅ Correct!";
            feedback.className = "feedback correct";
        }} else {{
            feedback.textContent = "❌ Incorrect. The correct answer is " + correctVal;
            feedback.className = "feedback incorrect";
        }}
    }}

    function markComplete() {{
        const pageId = 'Listening_Day{day}';
        localStorage.setItem('EnglishHub_Progress_' + pageId, 'true');
        alert('Progress Saved!');
        location.href = 'index.html';
    }}
</script>
</body>
</html>
"""

# --- Content Generators ---

def gen_part1(idx):
    # Photographs
    # 4 audio descriptions, user picks mostly hidden correct one or simply A/B/C/D
    scenarios = [
        {"desc": "A business meeting", "opts": ["A) They are shaking hands.", "B) They are looking at a screen.", "C) They are eating lunch.", "D) They are walking outside."], "ans": "B"},
        {"desc": "A construction site", "opts": ["A) The man is wearing a helmet.", "B) The road is being paved.", "C) A truck is parking.", "D) Tools are scattered on the floor."], "ans": "A"},
        {"desc": "A library scene", "opts": ["A) Books are stacked on the floor.", "B) A woman is reading a magazine.", "C) The shelves are full of books.", "D) Someone is paying at the counter."], "ans": "C"},
    ]
    # Map descriptions to images if available
    sc = scenarios[idx % len(scenarios)]

    img_map = {
        "A business meeting": "images/toeic_meeting.png",
        "A construction site": "images/toeic_construction.png",
        "A library scene": "images/toeic_library.png"
    }
    
    img_src = img_map.get(sc['desc'])
    
    if img_src:
        img_html = f'<img src="{img_src}" style="max-width:100%; max-height:100%; object-fit:contain; border-radius:8px;">'
        bg_style = ""
    else:
        # Fallback to placeholder service if local image missing
        encoded_desc = sc['desc'].replace(" ", "+")
        img_html = f'<img src="https://placehold.co/600x400?text={encoded_desc}" style="max-width:100%; max-height:100%; object-fit:contain; border-radius:8px;">'
        bg_style = "background: #eee;"

    html = f"""
    <div class="question-card">
        <span class="part-label">Part 1: Photographs</span>
        <div class="photo-placeholder" style="{bg_style}">
            {img_html}
        </div>
        <p>Listen to the four statements and select the one that best describes the picture.</p>
        <button class="audio-btn" onclick="playAudio('A. {sc['opts'][0]}. B. {sc['opts'][1]}. C. {sc['opts'][2]}. D. {sc['opts'][3]}.')">▶️ Play Audio Options</button>
        
        <div class="options-grid">
            <label class="option-label"><input type="radio" name="q{idx}" value="A" onclick="checkAnswer({idx}, '{sc['ans']}')"> (A)</label>
            <label class="option-label"><input type="radio" name="q{idx}" value="B" onclick="checkAnswer({idx}, '{sc['ans']}')"> (B)</label>
            <label class="option-label"><input type="radio" name="q{idx}" value="C" onclick="checkAnswer({idx}, '{sc['ans']}')"> (C)</label>
            <label class="option-label"><input type="radio" name="q{idx}" value="D" onclick="checkAnswer({idx}, '{sc['ans']}')"> (D)</label>
        </div>
        <div id="fb-{idx}" class="feedback"></div>
    </div>
    """
    return html

def gen_part2(idx):
    # Q & A (3 options)
    scenarios = [
        {"q": "When does the meeting start?", "opts": ["A) In conference room B.", "B) At 2 PM sharp.", "C) Yes, I am going."], "ans": "B"},
        {"q": "Who is responsible for the budget?", "opts": ["A) It's about 500 dollars.", "B) Mr. Henderson is.", "C) I bought it yesterday."], "ans": "B"},
        {"q": "Where did you put the file?", "opts": ["A) On your desk.", "B) It's a large file.", "C) No, I didn't."], "ans": "A"},
    ]
    sc = scenarios[idx % len(scenarios)]
    return f"""
    <div class="question-card">
        <span class="part-label">Part 2: Question-Response</span>
        <p>Listen to the question and three responses. Select the best response.</p>
        <button class="audio-btn" onclick="playAudio('Question: {sc['q']} ... Response A: {sc['opts'][0]} ... Response B: {sc['opts'][1]} ... Response C: {sc['opts'][2]}')">▶️ Play Audio</button>
        
        <div class="options-grid">
            <label class="option-label"><input type="radio" name="q{idx}" value="A" onclick="checkAnswer({idx}, '{sc['ans']}')"> (A)</label>
            <label class="option-label"><input type="radio" name="q{idx}" value="B" onclick="checkAnswer({idx}, '{sc['ans']}')"> (B)</label>
            <label class="option-label"><input type="radio" name="q{idx}" value="C" onclick="checkAnswer({idx}, '{sc['ans']}')"> (C)</label>
        </div>
        <div id="fb-{idx}" class="feedback"></div>
    </div>
    """

def gen_part3(idx):
    # Short Conversation
    conv = "Woman: Did you finish the monthly report? Man: No, I am still waiting for the sales data from the marketing team. Woman: You should call them correctly. We need it by noon."
    q1 = {"q": "What use the man waiting for?", "opts": ["A) A phone call", "B) Sales data", "C) A meeting", "D) Lunch"], "ans": "B"}
    q2 = {"q": "What is the deadline?", "opts": ["A) Noon", "B) Tomorrow", "C) 5 PM", "D) Next week"], "ans": "A"}
    q3 = {"q": "What does the woman suggest?", "opts": ["A) Waiting longer", "B) Calling the team", "C) Leaving early", "D) Writing an email"], "ans": "B"}
    
    return f"""
    <div class="question-card">
        <span class="part-label">Part 3: Short Conversations</span>
        <p>Listen to the dialogue and answer the questions.</p>
        <button class="audio-btn" onclick="playAudio('{conv.replace("'", "")}')">▶️ Play Conversation</button>
        <hr style="border:0; border-top:1px solid #eee; margin:15px 0;">
        
        <!-- Q1 -->
        <p><strong>1. {q1['q']}</strong></p>
        <div class="options-grid">
            <label class="option-label"><input type="radio" name="q{idx}_1" value="A" onclick="checkAnswer('{idx}_1', '{q1['ans']}')"> {q1['opts'][0]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_1" value="B" onclick="checkAnswer('{idx}_1', '{q1['ans']}')"> {q1['opts'][1]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_1" value="C" onclick="checkAnswer('{idx}_1', '{q1['ans']}')"> {q1['opts'][2]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_1" value="D" onclick="checkAnswer('{idx}_1', '{q1['ans']}')"> {q1['opts'][3]}</label>
        </div>
        <div id="fb-{idx}_1" class="feedback"></div>

        <!-- Q2 -->
        <p><strong>2. {q2['q']}</strong></p>
        <div class="options-grid">
            <label class="option-label"><input type="radio" name="q{idx}_2" value="A" onclick="checkAnswer('{idx}_2', '{q2['ans']}')"> {q2['opts'][0]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_2" value="B" onclick="checkAnswer('{idx}_2', '{q2['ans']}')"> {q2['opts'][1]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_2" value="C" onclick="checkAnswer('{idx}_2', '{q2['ans']}')"> {q2['opts'][2]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_2" value="D" onclick="checkAnswer('{idx}_2', '{q2['ans']}')"> {q2['opts'][3]}</label>
        </div>
        <div id="fb-{idx}_2" class="feedback"></div>
    </div>
    """

def gen_part4(idx):
    # Short Talks (Monologue)
    talk = "Attention passengers. Flight 84 to Tokyo has been delayed due to heavy snow. The new departure time is 8 PM. Please check the monitors for gate changes."
    q1 = {"q": "Where is the flight going?", "opts": ["A) London", "B) Tokyo", "C) New York", "D) Paris"], "ans": "B"}
    q2 = {"q": "Why is it delayed?", "opts": ["A) Technical issue", "B) Heavy snow", "C) Late crew", "D) Security check"], "ans": "B"}
    
    return f"""
    <div class="question-card">
        <span class="part-label">Part 4: Short Talks</span>
        <p>Listen to the announcement and answer the questions.</p>
        <button class="audio-btn" onclick="playAudio('{talk.replace("'", "")}')">▶️ Play Announcement</button>
        <hr style="border:0; border-top:1px solid #eee; margin:15px 0;">
        
        <!-- Q1 -->
        <p><strong>1. {q1['q']}</strong></p>
        <div class="options-grid">
            <label class="option-label"><input type="radio" name="q{idx}_1" value="A" onclick="checkAnswer('{idx}_1', '{q1['ans']}')"> {q1['opts'][0]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_1" value="B" onclick="checkAnswer('{idx}_1', '{q1['ans']}')"> {q1['opts'][1]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_1" value="C" onclick="checkAnswer('{idx}_1', '{q1['ans']}')"> {q1['opts'][2]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_1" value="D" onclick="checkAnswer('{idx}_1', '{q1['ans']}')"> {q1['opts'][3]}</label>
        </div>
        <div id="fb-{idx}_1" class="feedback"></div>

        <!-- Q2 -->
        <p><strong>2. {q2['q']}</strong></p>
        <div class="options-grid">
            <label class="option-label"><input type="radio" name="q{idx}_2" value="A" onclick="checkAnswer('{idx}_2', '{q2['ans']}')"> {q2['opts'][0]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_2" value="B" onclick="checkAnswer('{idx}_2', '{q2['ans']}')"> {q2['opts'][1]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_2" value="C" onclick="checkAnswer('{idx}_2', '{q2['ans']}')"> {q2['opts'][2]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_2" value="D" onclick="checkAnswer('{idx}_2', '{q2['ans']}')"> {q2['opts'][3]}</label>
        </div>
        <div id="fb-{idx}_2" class="feedback"></div>
    </div>
    """

def main():
    for i in range(1, 31):
        content = ""
        part_name = ""
        
        if i <= 5:
            part_name = "Part 1 (Photographs)"
            for q in range(3): content += gen_part1(q + i*10)
        elif i <= 12:
            part_name = "Part 2 (Q&A)"
            for q in range(5): content += gen_part2(q + i*10)
        elif i <= 20:
            part_name = "Part 3 (Conversations)"
            for q in range(2): content += gen_part3(q + i*10)
        else:
            part_name = "Part 4 (Talks)"
            for q in range(2): content += gen_part4(q + i*10)
            
        full_html = get_header(i, part_name) + content + get_footer(i)
        
        filename = f"Listening_Day{i}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"Generated {filename}")

if __name__ == "__main__":
    main()
