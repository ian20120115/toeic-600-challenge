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

def escape_text(text):
    return text.replace("'", "\\'")

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

# --- Unique Content Database ---

# Part 1: Photographs (Day 1-5)
# 3 questions per day = 15 scenarios
part1_db = {
    1: [
        {"desc": "A construction site", "opts": ["A) The man is wearing a helmet.", "B) The road is being paved.", "C) A truck is parking.", "D) Tools are scattered on the floor."], "ans": "A"},
        {"desc": "A library scene", "opts": ["A) Books are stacked on the floor.", "B) A woman is reading a magazine.", "C) The shelves are full of books.", "D) Someone is paying at the counter."], "ans": "C"},
        {"desc": "A business meeting", "opts": ["A) They are shaking hands.", "B) They are looking at a screen.", "C) They are eating lunch.", "D) They are walking outside."], "ans": "B"}
    ],
    2: [
        {"desc": "A busy restaurant kitchen", "opts": ["A) The chef is chopping vegetables.", "B) The waiter is dropping a plate.", "C) The stove is on fire.", "D) Customers are waiting outside."], "ans": "A"},
        {"desc": "A park with people", "opts": ["A) Children are playing soccer.", "B) A dog is sleeping on a bench.", "C) The trees are being cut down.", "D) Everyone is holding an umbrella."], "ans": "A"},
        {"desc": "An airport terminal", "opts": ["A) The plane is taking off.", "B) Passengers are waiting in line.", "C) Luggage is lost.", "D) The pilot is eating."], "ans": "B"}
    ],
    3: [
        {"desc": "A doctor examining a patient", "opts": ["A) The doctor is writing a prescription.", "B) The patient is sleeping.", "C) They are looking at an X-ray.", "D) The nurse is calling the phone."], "ans": "C"},
        {"desc": "A supermarket checkout", "opts": ["A) The cashier is scanning items.", "B) The cart is empty.", "C) Fruits are on the floor.", "D) The customer is paying with cash."], "ans": "A"},
        {"desc": "A mechanic fixing a car", "opts": ["A) The car is shiny and new.", "B) The hood is open.", "C) The tire is flat.", "D) He is driving away."], "ans": "B"}
    ],
    4: [
        {"desc": "A teacher in a classroom", "opts": ["A) She is writing on the whiteboard.", "B) Students are sleeping.", "C) The door is locked.", "D) Books are flying."], "ans": "A"},
        {"desc": "A scientist in a lab", "opts": ["A) He is looking through a microscope.", "B) The test tubes are broken.", "C) She is wearing a coat.", "D) The computer is off."], "ans": "A"},
        {"desc": "A street market", "opts": ["A) Vegetables are sold in boxes.", "B) Cars are racing.", "C) It is raining heavily.", "D) The street is empty."], "ans": "A"}
    ],
    5: [
        {"desc": "A reception desk", "opts": ["A) The phone is ringing.", "B) The receptionist is greeting a guest.", "C) The lobby is dark.", "D) Keys are on the floor."], "ans": "B"},
        {"desc": "A gym workout", "opts": ["A) He is lifting weights.", "B) She is swimming.", "C) The treadmill is broken.", "D) Everyone is sitting."], "ans": "A"},
        {"desc": "A bus stop", "opts": ["A) The bus is arriving.", "B) People are running away.", "C) tickets are free.", "D) The driver is sleeping."], "ans": "A"}
    ]
}

# Part 2: Q&A (Day 6-12)
# 5 questions per day
part2_db = {
    6: [
        {"q": "When does the meeting start?", "opts": ["A) In Room B.", "B) At 2 PM.", "C) Yes, I am."], "ans": "B"},
        {"q": "Who booked the flight?", "opts": ["A) To London.", "B) Mr. Smith did.", "C) Tomorrow morning."], "ans": "B"},
        {"q": "Where is the nearest bank?", "opts": ["A) Next to the post office.", "B) It is open.", "C) I have no money."], "ans": "A"},
        {"q": "Why is the office closed?", "opts": ["A) It's a holiday.", "B) Yes, close it.", "C) At 6 PM."], "ans": "A"},
        {"q": "How do I turn this on?", "opts": ["A) Press the red button.", "B) It is new.", "C) I don't know him."], "ans": "A"}
    ],
    7: [
        {"q": "Did you finish the report?", "opts": ["A) No, not yet.", "B) It is a long report.", "C) She is reporting."], "ans": "A"},
        {"q": "Whose bag is this?", "opts": ["A) It's huge.", "B) It's mine.", "C) Yes, please."], "ans": "B"},
        {"q": "Can you help me?", "opts": ["A) Certainly.", "B) I am fine.", "C) He is helping."], "ans": "A"},
        {"q": "What time is it?", "opts": ["A) It's 5 o'clock.", "B) I have time.", "C) Watch out."], "ans": "A"},
        {"q": "Are you coming to the party?", "opts": ["A) I'm afraid I can't.", "B) The party is fun.", "C) Yes, he is."], "ans": "A"}
    ],
    8: [
        {"q": "Which way to the station?", "opts": ["A) Turn left.", "B) By train.", "C) Station is big."], "ans": "A"},
        {"q": "Has the mail arrived?", "opts": ["A) Yes, on your desk.", "B) I will mail it.", "C) No, he left."], "ans": "A"},
        {"q": "Do you like coffee?", "opts": ["A) No, I prefer tea.", "B) It is hot.", "C) Coffee is black."], "ans": "A"},
        {"q": "When is the deadline?", "opts": ["A) Yesterday.", "B) It is dead.", "C) Line is long."], "ans": "A"},
        {"q": "Cost of the ticket?", "opts": ["A) 50 dollars.", "B) One ticket.", "C) To Paris."], "ans": "A"}
    ],
    9: [], # Fill with generic if empty or repeat with variation
    10: [],
    11: [],
    12: []
}

# Fill remaining Part 2 with generated variations
for d in range(9, 13):
    part2_db[d] = [
        {"q": f"Question {i} for Day {d}?", "opts": ["A) Correct Answer.", "B) Wrong Answer.", "C) Wrong Answer."], "ans": "A"} for i in range(1, 6)
    ]
    # Inject some variety
    part2_db[d][0] = {"q": "Should we take a taxi?", "opts": ["A) It's too expensive.", "B) Yes, take it.", "C) Taxi is yellow."], "ans": "A"}
    part2_db[d][1] = {"q": "Where did you buy that?", "opts": ["A) At the mall.", "B) It was cheap.", "C) I bought it."], "ans": "A"}


# Part 3: Conversations (Day 13-20)
# 2 conversations per day
part3_db = {
    13: [
        ("W: Did you see the new schedule? M: Yes, they changed the meeting time. W: Oh no, I have a dentist appointment then.",
         [("What are they discussing?", ["Schedulue", "Food", "Weather", "Traffic"], "A"), ("What is the woman's problem?", ["She is sick", "She has conflict", "She is late", "She lost key"], "B")]),
        ("M: I'd like to book a room. W: For how many nights? M: Just two nights. W: Okay, that will be $200.",
         [("Where does this take place?", ["Hotel", "Bank", "School", "Park"], "A"), ("How long is the stay?", ["1 night", "2 nights", "3 nights", "1 week"], "B")])
    ]
}
# Generate generic for rest for now to ensure structure exists
for d in range(14, 21):
    part3_db[d] = [
        (f"M: Use conversation {i}. W: Okay day {d}.", [("Q1", ["A","B","C","D"], "A"), ("Q2", ["A","B","C","D"], "A")]) for i in range(2)
    ]

# Part 4: Talks (Day 21-30)
# 2 talks per day
part4_db = {
    21: [
        ("Attention please. The library will close in 15 minutes. Please check out your books now.",
         [("Where is this?", ["Library", "School", "Store", "Bank"], "A"), ("When closing?", ["15m", "1 hour", "Now", "Never"], "A")]),
        ("Welcome to the zoo. Do not feed the animals. Tours start at 10 AM.", 
         [("What is forbidden?", ["Feeding", "Walking", "Talking", "Sleeping"], "A"), ("Tour time?", ["9", "10", "11", "12"], "B")])
    ]
}
for d in range(22, 31):
    part4_db[d] = [
        (f"This is talk {i} for day {d}. Please listen.", [("Q1", ["A","B","C","D"], "A"), ("Q2", ["A","B","C","D"], "A")]) for i in range(2)
    ]

def gen_part1_content(idx, sc):
    # Map descriptions to images if available
    img_map = {
        "A business meeting": "images/toeic_meeting.png",
        "A construction site": "images/toeic_construction.png",
        "A library scene": "images/toeic_library.png",
        "A busy restaurant kitchen": "images/toeic_kitchen.png",
        "A park with people": "images/toeic_park.png",
        "An airport terminal": "images/toeic_airport.png",
        "A doctor examining a patient": "images/toeic_doctor.png",
        "A supermarket checkout": "images/toeic_supermarket.png",
        "A mechanic fixing a car": "images/toeic_mechanic.png",
        "A teacher in a classroom": "images/toeic_classroom.png",
        "A scientist in a lab": "images/toeic_lab.png",
        "A street market": "images/toeic_market.png",
        "A reception desk": "images/toeic_reception.png",
        "A gym workout": "images/toeic_gym.png",
        "A bus stop": "images/toeic_bus.png"
    }
    
    img_src = img_map.get(sc['desc'])
    
    if img_src:
        img_html = f'<img src="{img_src}" style="max-width:100%; max-height:100%; object-fit:contain; border-radius:8px;">'
        bg_style = ""
    else:
        encoded_desc = sc['desc'].replace(" ", "+")
        img_html = f'<img src="https://placehold.co/600x400?text={encoded_desc}" style="max-width:100%; max-height:100%; object-fit:contain; border-radius:8px;">'
        bg_style = "background: #eee;"

    return f"""
    <div class="question-card">
        <span class="part-label">Part 1: Photographs</span>
        <div class="photo-placeholder" style="{bg_style}">
            {img_html}
        </div>
        <p>Listen to the four statements and select the one that best describes the picture.</p>
        <button class="audio-btn" onclick="playAudio('{escape_text(sc['opts'][0])}. {escape_text(sc['opts'][1])}. {escape_text(sc['opts'][2])}. {escape_text(sc['opts'][3])}.')">▶️ Play Audio Options</button>
        
        <div class="options-grid">
            <label class="option-label"><input type="radio" name="q{idx}" value="A" onclick="checkAnswer({idx}, '{sc['ans']}')"> (A)</label>
            <label class="option-label"><input type="radio" name="q{idx}" value="B" onclick="checkAnswer({idx}, '{sc['ans']}')"> (B)</label>
            <label class="option-label"><input type="radio" name="q{idx}" value="C" onclick="checkAnswer({idx}, '{sc['ans']}')"> (C)</label>
            <label class="option-label"><input type="radio" name="q{idx}" value="D" onclick="checkAnswer({idx}, '{sc['ans']}')"> (D)</label>
        </div>
        <div id="fb-{idx}" class="feedback"></div>
    </div>
    """

def gen_part2_content(idx, sc):
    return f"""
    <div class="question-card">
        <span class="part-label">Part 2: Question-Response</span>
        <p>Listen to the question and three responses. Select the best response.</p>
        <button class="audio-btn" onclick="playAudio('Question: {escape_text(sc['q'])} ... {escape_text(sc['opts'][0])} ... {escape_text(sc['opts'][1])} ... {escape_text(sc['opts'][2])}')">▶️ Play Audio</button>
        
        <div class="options-grid">
            <label class="option-label"><input type="radio" name="q{idx}" value="A" onclick="checkAnswer({idx}, '{sc['ans']}')"> (A)</label>
            <label class="option-label"><input type="radio" name="q{idx}" value="B" onclick="checkAnswer({idx}, '{sc['ans']}')"> (B)</label>
            <label class="option-label"><input type="radio" name="q{idx}" value="C" onclick="checkAnswer({idx}, '{sc['ans']}')"> (C)</label>
        </div>
        <div id="fb-{idx}" class="feedback"></div>
    </div>
    """

def gen_part3_content(idx, conv, q1, q2):
    return f"""
    <div class="question-card">
        <span class="part-label">Part 3: Short Conversations</span>
        <p>Listen to the dialogue and answer the questions.</p>
        <button class="audio-btn" onclick="playAudio('{escape_text(conv)}')">▶️ Play Conversation</button>
        <hr style="border:0; border-top:1px solid #eee; margin:15px 0;">
        
        <p><strong>1. {q1[0]}</strong></p>
        <div class="options-grid">
            <label class="option-label"><input type="radio" name="q{idx}_1" value="A" onclick="checkAnswer('{idx}_1', '{q1[2]}')"> {q1[1][0]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_1" value="B" onclick="checkAnswer('{idx}_1', '{q1[2]}')"> {q1[1][1]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_1" value="C" onclick="checkAnswer('{idx}_1', '{q1[2]}')"> {q1[1][2]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_1" value="D" onclick="checkAnswer('{idx}_1', '{q1[2]}')"> {q1[1][3]}</label>
        </div>
        <div id="fb-{idx}_1" class="feedback"></div>

        <p><strong>2. {q2[0]}</strong></p>
        <div class="options-grid">
            <label class="option-label"><input type="radio" name="q{idx}_2" value="A" onclick="checkAnswer('{idx}_2', '{q2[2]}')"> {q2[1][0]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_2" value="B" onclick="checkAnswer('{idx}_2', '{q2[2]}')"> {q2[1][1]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_2" value="C" onclick="checkAnswer('{idx}_2', '{q2[2]}')"> {q2[1][2]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_2" value="D" onclick="checkAnswer('{idx}_2', '{q2[2]}')"> {q2[1][3]}</label>
        </div>
        <div id="fb-{idx}_2" class="feedback"></div>
    </div>
    """

# Reuse part3 template for part4 basically
def gen_part4_content(idx, talk, q1, q2):
    return f"""
    <div class="question-card">
        <span class="part-label">Part 4: Short Talks</span>
        <p>Listen to the announcement and answer the questions.</p>
        <button class="audio-btn" onclick="playAudio('{escape_text(talk)}')">▶️ Play Announcement</button>
        <hr style="border:0; border-top:1px solid #eee; margin:15px 0;">
        
        <p><strong>1. {q1[0]}</strong></p>
        <div class="options-grid">
            <label class="option-label"><input type="radio" name="q{idx}_1" value="A" onclick="checkAnswer('{idx}_1', '{q1[2]}')"> {q1[1][0]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_1" value="B" onclick="checkAnswer('{idx}_1', '{q1[2]}')"> {q1[1][1]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_1" value="C" onclick="checkAnswer('{idx}_1', '{q1[2]}')"> {q1[1][2]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_1" value="D" onclick="checkAnswer('{idx}_1', '{q1[2]}')"> {q1[1][3]}</label>
        </div>
        <div id="fb-{idx}_1" class="feedback"></div>

        <p><strong>2. {q2[0]}</strong></p>
        <div class="options-grid">
            <label class="option-label"><input type="radio" name="q{idx}_2" value="A" onclick="checkAnswer('{idx}_2', '{q2[2]}')"> {q2[1][0]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_2" value="B" onclick="checkAnswer('{idx}_2', '{q2[2]}')"> {q2[1][1]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_2" value="C" onclick="checkAnswer('{idx}_2', '{q2[2]}')"> {q2[1][2]}</label>
            <label class="option-label"><input type="radio" name="q{idx}_2" value="D" onclick="checkAnswer('{idx}_2', '{q2[2]}')"> {q2[1][3]}</label>
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
            questions = part1_db.get(i, part1_db[1]) # Fallback to Day 1 only if error
            for idx, sc in enumerate(questions):
                content += gen_part1_content(idx + i*10, sc)
                
        elif i <= 12:
            part_name = "Part 2 (Q&A)"
            questions = part2_db.get(i, part2_db[6])
            for idx, sc in enumerate(questions):
                content += gen_part2_content(idx + i*10, sc)
                
        elif i <= 20:
            part_name = "Part 3 (Conversations)"
            items = part3_db.get(i, part3_db[13])
            for idx, (conv, qs) in enumerate(items):
                content += gen_part3_content(idx + i*10, conv, qs[0], qs[1])
                
        else:
            part_name = "Part 4 (Talks)"
            items = part4_db.get(i, part4_db[21])
            for idx, (talk, qs) in enumerate(items):
                content += gen_part4_content(idx + i*10, talk, qs[0], qs[1])
            
        full_html = get_header(i, part_name) + content + get_footer(i)
        
        filename = f"Listening_Day{i}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"Generated {filename}")

if __name__ == "__main__":
    main()
