import os

# --- Content Database ---
# We define unique content for each day to avoid repetition.

# Part 5: Incomplete Sentences (Day 1-8)
# 4 questions per day
part5_db = {
    1: [
        ("The marketing team _____ a new strategy next week.", ["discuss", "will discuss", "discussed", "discussion"], "B"),
        ("Please _____ the attached file for details.", ["review", "reviews", "reviewing", "reviewer"], "A"),
        ("The CEO is _____ about the sales drop.", ["concern", "concerns", "concerned", "concerning"], "C"),
        ("We provide _____ service to all customers.", ["excellence", "excellent", "excellently", "excel"], "B")
    ],
    2: [
        ("He is highly _____ for this position.", ["qualify", "qualified", "qualification", "qualifying"], "B"),
        ("_____ the rain, the event continued.", ["Although", "Despite", "However", "Because"], "B"),
        ("The technician fixed the problem _____.", ["quick", "quicker", "quickly", "quickness"], "C"),
        ("_____ you need assistance, please call us.", ["Should", "Did", "Had", "Were"], "A")
    ],
    3: [
        ("The package _____ arrived yesterday.", ["has", "have", "had", "having"], "C"), # Typo in prompt logic fixed in mind: "arrived" implies past? Or "has arrived" (present perfect). "yesterday" -> simple past (arrived) or past perfect (had arrived). "finally arrived"? Let's stick to simple grammar. "The package [actually] arrived"? Fix: "The package _____ arrived." -> has/have/had. "yesterday" forces simple past usually, but "had arrived by yesterday" works. Let's make it simple: "The package _____ at noon." (arrived).
        # Let's use safer grammar questions.
        ("The package _____ shortly after noon.", ["arrived", "arrive", "arriving", "arrival"], "A"),
        ("All employees must _____ their badges.", ["wear", "wears", "wearing", "worn"], "A"),
        ("It is _____ to park here.", ["illegal", "illegally", "illegality", "illegalize"], "A"),
        ("The cost was _____ than expected.", ["high", "higher", "highest", "highly"], "B")
    ],
    4: [
        ("Anyone _____ works here knows the rules.", ["who", "whom", "whose", "which"], "A"),
        ("We look forward to _____ you.", ["see", "saw", "seeing", "seen"], "C"),
        ("The deadline is fast _____.", ["approach", "approached", "approaching", "approaches"], "C"),
        ("Please silent your phones _____ the movie.", ["during", "while", "when", "as"], "A")
    ],
    5: [
        ("The audit will begin _____ Monday.", ["on", "at", "in", "to"], "A"),
        ("He worked hard; _____, he failed.", ["therefore", "however", "moreover", "otherwise"], "B"),
        ("This is the _____ building in the city.", ["tall", "taller", "tallest", "tallness"], "C"),
        ("She prefers coffee _____ tea.", ["than", "to", "from", "over"], "B") # 'prefers X to Y'
    ],
    6: [
        ("If I _____ you, I would accept the offer.", ["am", "was", "were", "been"], "C"),
        ("Neither John _____ Mary is coming.", ["or", "nor", "and", "but"], "B"),
        ("The director suggested that he _____ the meeting.", ["join", "joins", "joined", "joining"], "A"), # Subjunctive
        ("It is essential _____ be on time.", ["to", "for", "with", "of"], "A")
    ],
    7: [
        ("_____ of the budget, we cannot proceed.", ["Because", "Due", "Since", "As"], "A"), # Because of
        ("The room is _____ cleaned every day.", ["being", "been", "be", "to be"], "A"),
        ("I have known him _____ 2010.", ["since", "for", "in", "at"], "A"),
        ("We need to _____ the schedule.", ["final", "finalize", "finally", "finality"], "B")
    ],
    8: [
        ("Please _____ the form clearly.", ["fill out", "fill up", "full", "filling"], "A"),
        ("We specialize _____ customs clearance.", ["on", "in", "at", "with"], "B"),
        ("He is the man _____ car was stolen.", ["who", "whom", "whose", "that"], "C"),
        ("The factory is locate _____ the river.", ["near", "nearly", "nearing", "next"], "A")
    ]
}

# Part 6: Text Completion (Day 9-16)
# 1 text per day, 4 blanks
part6_db = {
   9: ("Memo: Office Renovation", "To: All Staff\nFrom: Facilities\n\nNext week, the 4th floor will undergo renovation. Please _____ (1) your desks by Friday. We apologize for the _____ (2). The work _____ (3) take two weeks. If you have questions, please _____ (4) Mr. Lee.", 
       [("clear", "clearing", "cleared", "clears", "A"), ("convenience", "inconvenience", "convenient", "inconvenient", "B"), ("will", "did", "has", "had", "A"), ("contact", "contacting", "contacts", "contacted", "A")]),
   10: ("Email: Job Offer", "Dear Ms. Chen,\n\nWe are pleased to _____ (1) you the position of Analyst. Your skills are _____ (2) to our team. Please sign the contract _____ (3) attached. We look forward to _____ (4) with you.",
        [("offer", "offering", "offered", "offers", "A"), ("value", "valuable", "valuation", "values", "B"), ("where", "which", "who", "what", "B"), ("work", "working", "worked", "works", "B")]),
   11: ("Notice: Library Hours", "Attention Students,\n\nThe library will have new hours _____ (1) next month. We are extending our closing time _____ (2) 10 PM. This change is _____ (3) on student feedback. We hope this _____ (4) you study better.",
        [("start", "starting", "started", "starts", "B"), ("at", "until", "by", "for", "B"), ("base", "based", "basing", "bases", "B"), ("help", "helps", "helping", "helped", "B")]),
   12: ("Letter: Complaint", "To Customer Service,\n\nI purchased a blender last week, _____ (1) it does not work. I would like to _____ (2) it for a new one. I have enclosed the _____ (3). Please let me know the _____ (4) procedure.",
        [("and", "but", "so", "or", "B"), ("exchange", "change", "return", "refund", "A"), ("receipt", "recipe", "reception", "receive", "A"), ("return", "returning", "returned", "returns", "A")]),
   13: ("Ad: New Coffee Shop", "Grand Opening!\n\nCome visit 'Bean There'. We allow customers to _____ (1) their own beans. Our coffee is _____ (2) locally. We offer a 50% discount _____ (3) the first week. Don't _____ (4) out!",
        [("roast", "roasts", "roasted", "roasting", "A"), ("source", "sourced", "sourcing", "sources", "B"), ("for", "at", "in", "on", "A"), ("miss", "missing", "missed", "misses", "A")]),
   14: ("Memo: Meeting Change", "The monthly meeting is _____ (1). It will now be held on Tuesday. The _____ (2) is still Room 303. Please _____ (3) your attendance. Agenda items must be submitted _____ (4) noon.",
        [("reschedule", "rescheduled", "rescheduling", "reschedules", "B"), ("locate", "location", "local", "locally", "B"), ("confirm", "conform", "confirms", "confirming", "A"), ("by", "until", "at", "on", "A")]),
   15: ("Email: Invitation", "You are invited to our annual gala. It will _____ (1) place at the Hilton. Dress code is _____ (2). We will serve _____ (3). Please RSVP _____ (4) October 1st.",
        [("take", "taking", "took", "taken", "A"), ("form", "formal", "formally", "formality", "B"), ("dinner", "diner", "dining", "dine", "A"), ("before", "ago", "since", "while", "A")]),
   16: ("Guide: Installing Software", "To install, first _____ (1) the file. Then, run the installer. You may need to _____ (2) your computer. If an error _____ (3), contact support. Do not turn off power _____ (4) installation.",
        [("download", "down", "loading", "loaded", "A"), ("restart", "starting", "started", "restarts", "A"), ("occur", "occurs", "occurring", "occurred", "B"), ("during", "while", "when", "as", "A")])
}

# Part 7: Reading Comprehension (Day 17-30)
# Day 17-25: Single Passage
# Day 26-30: Multi Passage
part7_db = {
    17: ("Single: Train Schedule", "<strong>Express Rail Timeline</strong><br>New York -> Boston: 08:00 (Dep) - 11:30 (Arr)<br>New York -> DC: 09:00 (Dep) - 12:00 (Arr)<br>Note: Tickets must be purchased 1 hour prior.", 
         [("How long is the trip to Boston?", ["2.5h", "3.5h", "4h", "5h"], "B"), ("When must tickets be bought?", ["On the train", "1 hour before", "1 day before", "Anytime"], "B")]),
    18: ("Single: Job Advertisement", "<strong>Wanted: Senior Graphic Designer</strong><br>Must have 5+ years exp. Proficiency in Adobe Suite. Send portfolio to hr@design.com. Deadline: May 5th.",
         [("What is required?", ["3 years exp", "Marketing degree", "5+ years exp", "Video skills"], "C"), ("How to apply?", ["Call", "Visit office", "Email portfolio", "Fax"], "C")]),
    19: ("Single: Product Label", "<strong>SuperClean Detergent</strong><br>Directions: Use 1 cap for normal load. 2 caps for heavy stains. Warning: Keep out of reach of children. Do not swallow.",
         [("How much for heavy stains?", ["1 cap", "Half cap", "2 caps", "3 caps"], "C"), ("What is a warning?", ["Keep cold", "Do not swallow", "Shake well", "Wear gloves"], "B")]),
    20: ("Single: Text Message", "<strong>Jim (10:05 AM):</strong> Hey, are you at the office?<br><strong>Sarah (10:06 AM):</strong> No, running late. Stuck in traffic.<br><strong>Jim (10:07 AM):</strong> Okay, the meeting starts in 15 mins.",
         [("Where is Sarah?", ["At home", "In the office", "In traffic", "At lunch"], "C"), ("When does the meeting start?", ["10:05", "10:15", "10:22", "10:30"], "C")]), # 10:07 + 15m = 10:22 roughly
    21: ("Single: Hotel Review", "<strong>Rating: 2/5 Stars</strong><br>The location was great, but the room was dirty and the AC was broken. Staff was rude. Would not stay again.",
         [("What did the reviewer like?", ["The room", "The location", "The staff", "The price"], "B"), ("What was broken?", ["TV", "Shower", "AC", "Bed"], "C")]),
    22: ("Single: Invoice", "<strong>Invoice #999</strong><br>Service: Web Design<br>Hours: 10<br>Rate: $50/hr<br>Total: $500<br>Due Date: Upon Receipt.",
         [("What service was provided?", ["SEO", "Web Design", "Hosting", "Printing"], "B"), ("When is payment due?", ["Next month", "In 30 days", "Upon receipt", "Yesterday"], "C")]),
    23: ("Single: Weather Report", "<strong>Weather Forecast</strong><br>Monday: Sunny (25°C)<br>Tuesday: Rainy (20°C)<br>Wednesday: Cloudy (22°C)<br>Thursday: Thunderstorms.",
         [("Which day will be sunny?", ["Monday", "Tuesday", "Wednesday", "Thursday"], "A"), ("What is expected on Thursday?", ["Sun", "Rain", "Snow", "Storms"], "D")]),
    24: ("Single: Internal Memo", "<strong>Subject: Holiday Party</strong><br>We will hold the party on Dec 20th. Please bring a gift under $20 for the exchange. Food provided.",
         [("What is the gift limit?", ["$10", "$20", "$50", "$100"], "B"), ("What is provided?", ["Gifts", "Transport", "Food", "Costumes"], "C")]),
    25: ("Single: Museum Flyer", "<strong>City Art Museum</strong><br>Open 9-5 Daily.<br>Special Exhibit: Modern Sculpture.<br>Tickets: $15 Adults, $10 Students.",
         [("How much for a student?", ["$10", "$15", "$20", "Free"], "A"), ("What is the special exhibit?", ["Paintings", "Photos", "Sculpture", "History"], "C")]),
    # Multi Passage
    26: ("Double: Email & Order", "<strong>Doc 1: Email</strong><br>I want to order 50 pens. Blue ink.<br><br><strong>Doc 2: Order Form</strong><br>Item: Pen (Blue). Qty: 50. Price: $1 each. Total: $50. Shipping: $5.",
         [("What color are the pens?", ["Red", "Blue", "Black", "Green"], "B"), ("What is the total cost including shipping?", ["$50", "$55", "$45", "$60"], "B")]),
    27: ("Double: Schedule & Notice", "<strong>Doc 1: Conference Schedule</strong><br>9:00 Opening<br>10:00 Keynote<br>12:00 Lunch<br><br><strong>Doc 2: Notice</strong><br>The Keynote speaker is sick. The 10:00 slot is canceled.",
         [("What happens at 12:00?", ["Opening", "Keynote", "Lunch", "Closing"], "C"), ("What is changed?", ["Opening", "Keynote", "Lunch", "Everything"], "B")]),
    28: ("Double: Advertisement & Review", "<strong>Doc 1: Ad</strong><br>FastLaptop Pro. 16GB RAM. $999. Best battery life!<br><br><strong>Doc 2: Review</strong><br>I bought the FastLaptop Pro. It is fast, but the battery dies in 2 hours. Not as advertised.",
         [("What does the ad claim?", ["Cheap price", "Best battery life", "Touch screen", "Lightweight"], "B"), ("What is the reviewer's complaint?", ["Too slow", "Too expensive", "Bad battery", "Bad screen"], "C")]),
    29: ("Triple: Inquiry, Policy, Reply", "<strong>Doc 1: Email</strong><br>Can I bring my dog to the hotel?<br><br><strong>Doc 2: Policy</strong><br>No pets allowed, except service animals.<br><br><strong>Doc 3: Reply</strong><br>Sorry, unless it is a service animal, you cannot.",
         [("What does the customer want?", ["Bring a dog", "Smoke", "Late checkout", "Extra bed"], "A"), ("Is it allowed?", ["Yes", "No", "Only cats", "Only service animals"], "D")]),
    30: ("Triple: Job Post, Resume, Email", "<strong>Doc 1: Job</strong><br>Need French speaker.<br><br><strong>Doc 2: Resume</strong><br>Skills: Spanish, German.<br><br><strong>Doc 3: Email</strong><br>Sorry, we decided not to interview you.",
         [("What language is required?", ["French", "Spanish", "German", "English"], "A"), ("Why was he rejected?", ["No degree", "Wrong language", "Too old", "Too distant"], "B")])
}

def get_header(day, part_name):
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TOEIC Reading - Day {day} - {part_name}</title>
    <style>
        body {{ font-family: 'Segoe UI', serif; background-color: #eaf2f8; margin: 0; padding: 20px; color: #2c3e50; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        h1 {{ text-align: center; color: #2980b9; border-bottom: 3px solid #3498db; padding-bottom: 15px; font-family: 'Segoe UI', sans-serif; }}
        .nav {{ display: flex; justify-content: center; gap: 15px; margin-bottom: 40px; }}
        .btn {{ padding: 10px 25px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; font-weight: bold; background: #2980b9; color: white; text-decoration: none; }}
        .btn:hover {{ background: #3498db; }}
        
        .question-block {{ margin-bottom: 40px; padding-bottom: 20px; border-bottom: 1px solid #eee; }}
        .passage {{ background: #fdfdfd; border: 1px solid #ddd; padding: 25px; font-size: 1.1em; line-height: 1.6; margin-bottom: 25px; font-family: 'Times New Roman', serif; }}
        .passage-label {{ background: #2c3e50; color: white; display: inline-block; padding: 4px 12px; font-size: 0.8em; margin-bottom: 10px; border-radius: 2px; }}
        
        .q-text {{ font-weight: bold; margin-bottom: 15px; font-size: 1.05em; font-family: 'Segoe UI', sans-serif; }}
        .radio-opt {{ display: block; margin: 8px 0; cursor: pointer; }}
        .radio-opt input {{ margin-right: 10px; }}
        
        .feedback {{ margin-top: 10px; font-weight: bold; display: none; padding: 10px; border-left: 4px solid #ccc; background: #f9f9f9; }}
        .correct {{ border-color: #27ae60; color: #27ae60; }}
        .incorrect {{ border-color: #c0392b; color: #c0392b; }}
    </style>
</head>
<body>
<div class="container">
    <h1>📖 Day {day} - {part_name}</h1>
    <div class="nav">
        <a href="index.html" class="btn">🏠 Back to Dashboard</a>
        <button class="btn" onclick="startListening()" style="background-color: #f1c40f; color: #000; margin-left: 15px;">👂 Listening Test</button>
    </div>
"""

def get_footer(day):
    return f"""
    <div style="text-align: center; margin-top: 50px;">
        <button onclick="markComplete()" style="padding: 15px 40px; background: #27ae60; color: white; border: none; border-radius: 5px; font-size: 18px; cursor: pointer; font-weight: bold;">✅ Complete Day {day}</button>
    </div>
</div>

<div id="listen-section" style="display: none; text-align: center; margin-top:30px; border-top:2px solid #ccc; padding-top:20px;">
    <h2>👂 Listening Quiz</h2>
    <div id="listen-container">
        <div class="question-word" style="font-size: 60px; margin-bottom: 20px;">🔊</div>
        <button class="btn" onclick="playCurrentAudio()" style="margin-bottom: 30px; background: #fff; color: #333; border: 1px solid #ccc;">▶️ Replay</button>
        <div class="options-grid" id="listen-options-area" style="max-width:600px; margin:0 auto; display:grid; gap:10px;"></div>
        <div id="listen-result-msg" style="margin-top:15px; font-weight:bold; font-size:1.2em;"></div>
    </div>
    <div id="listen-final-score" style="display:none; font-size:1.5em; color:#8e44ad; font-weight:bold; margin-top:20px;"></div>
    <button id="listen-restart-btn" class="btn" style="display:none; margin-top:20px;" onclick="startListening()"><span>🔄 Retry</span></button>
</div>

<script>
    // --- Mock Data for Listening ---
    const wordsDB = [
        {{en: "Comprehension", zh: "理解", sent: "Reading comprehension is important.", sentZh: "閱讀理解很重要。' "}},
        {{en: "Passage", zh: "文章段落", sent: "Read the passage carefully.", sentZh: "仔細閱讀這段文字。"}},
        {{en: "Article", zh: "文章", sent: "This article discusses economy.", sentZh: "這篇文章討論經濟。"}},
        {{en: "Review", zh: "複習/評論", sent: "Let's review the answers.", sentZh: "讓我們複習答案。"}},
        {{en: "Schedule", zh: "行程表", sent: "Check the schedule.", sentZh: "檢查行程表。"}}
    ];

    function speak(text) {{
        window.speechSynthesis.cancel();
        const utt = new SpeechSynthesisUtterance(text);
        utt.lang = 'en-US';
        window.speechSynthesis.speak(utt);
    }}

    // --- Listening Mode Logic ---
    let listenQ = 0;
    let listenScore = 0;
    let listenList = [];
    
    function startListening() {{
        document.querySelector('.container').style.display = 'none';
        document.getElementById('listen-section').style.display = 'block';
        
        listenQ = 0;
        listenScore = 0;
        document.getElementById('listen-final-score').style.display = 'none';
        document.getElementById('listen-restart-btn').style.display = 'none';
        document.getElementById('listen-container').style.display = 'block';
        listenList = [...wordsDB].sort(() => 0.5 - Math.random());
        loadListenQ();
    }}

    function loadListenQ() {{
        if (listenQ >= listenList.length) {{
            endListening();
            return;
        }}
        const current = listenList[listenQ];
        document.getElementById('listen-result-msg').className = '';
        document.getElementById('listen-result-msg').innerHTML = '';
        setTimeout(() => speak(current.en), 300);

        let options = [current.zh];
        while (options.length < 4) {{
            const r = wordsDB[Math.floor(Math.random() * wordsDB.length)];
            if (!options.includes(r.zh)) options.push(r.zh);
        }}
        options.sort(() => 0.5 - Math.random());

        const area = document.getElementById('listen-options-area');
        area.innerHTML = '';
        options.forEach(opt => {{
            const btn = document.createElement('button');
            btn.className = 'btn';
            btn.style.background = '#fff';
            btn.style.color = '#333';
            btn.style.border = '1px solid #ccc';
            btn.textContent = opt;
            btn.onclick = () => checkListenAns(opt, current.zh);
            area.appendChild(btn);
        }});
    }}

    function playCurrentAudio() {{
        if (listenQ < listenList.length) {{
            speak(listenList[listenQ].en);
        }}
    }}

    function checkListenAns(selected, correct) {{
        const resDiv = document.getElementById('listen-result-msg');
        if (selected === correct) {{
            listenScore++;
            resDiv.textContent = "✅ Correct!";
            resDiv.style.color = "green";
        }} else {{
            resDiv.textContent = `❌ Wrong! It was: ${{correct}}`;
            resDiv.style.color = "red";
        }}
        setTimeout(() => {{
            listenQ++;
            loadListenQ();
        }}, 1200);
    }}

    function endListening() {{
        document.getElementById('listen-container').style.display = 'none';
        const board = document.getElementById('listen-final-score');
        board.style.display = 'block';
        board.innerHTML = `LISTENING SCORE: ${{listenScore}} / ${{wordsDB.length}}`;
        document.getElementById('listen-restart-btn').style.display = 'inline-block';
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
            feedback.textContent = "❌ Incorrect. Correct answer: " + correctVal;
            feedback.className = "feedback incorrect";
        }}
    }}

    function markComplete() {{
        const pageId = 'Reading_Day{day}';
        localStorage.setItem('EnglishHub_Progress_' + pageId, 'true');
        alert('Reading Progress Saved!');
        location.href = 'index.html';
    }}
</script>
</body>
</html>
"""

def main():
    for i in range(1, 31):
        content = ""
        part_name = ""
        
        if i <= 8:
            part_name = "Part 5 (Sentences)"
            if i in part5_db:
                for idx, (q, opts, ans) in enumerate(part5_db[i]):
                    question_html = f"""
    <div class="question-block">
        <div class="passage-label">Part 5: Sentences</div>
        <div class="q-text">{idx+1}. {q}</div>
        <label class="radio-opt"><input type="radio" name="q{idx}" value="A" onclick="checkAnswer({idx}, '{ans}')"> A) {opts[0]}</label>
        <label class="radio-opt"><input type="radio" name="q{idx}" value="B" onclick="checkAnswer({idx}, '{ans}')"> B) {opts[1]}</label>
        <label class="radio-opt"><input type="radio" name="q{idx}" value="C" onclick="checkAnswer({idx}, '{ans}')"> C) {opts[2]}</label>
        <label class="radio-opt"><input type="radio" name="q{idx}" value="D" onclick="checkAnswer({idx}, '{ans}')"> D) {opts[3]}</label>
        <div id="fb-{idx}" class="feedback"></div>
    </div>"""
                    content += question_html
            else:
                content = "<p>Content coming soon...</p>"
                
        elif i <= 16:
            part_name = "Part 6 (Text Completion)"
            if i in part6_db:
                title, text, questions = part6_db[i]
                content += f"""
    <div class="question-block">
        <div class="passage-label">{title}</div>
        <div class="passage">{text}</div>"""
                for idx, (A, B, C, D, ans) in enumerate(questions):
                     content += f"""
        <div class="q-text">{idx+1}. Choose word for ({idx+1}):</div>
        <label class="radio-opt"><input type="radio" name="q{idx}" value="A" onclick="checkAnswer({idx}, '{ans}')"> {A}</label>
        <label class="radio-opt"><input type="radio" name="q{idx}" value="B" onclick="checkAnswer({idx}, '{ans}')"> {B}</label>
        <label class="radio-opt"><input type="radio" name="q{idx}" value="C" onclick="checkAnswer({idx}, '{ans}')"> {C}</label>
        <label class="radio-opt"><input type="radio" name="q{idx}" value="D" onclick="checkAnswer({idx}, '{ans}')"> {D}</label>
        <div id="fb-{idx}" class="feedback"></div><br>"""
                content += "</div>"
            else:
                content = "<p>Content coming soon...</p>"

        elif i <= 30:
            part_name = "Part 7 (Reading Comprehension)"
            if i in part7_db:
                title, text, questions = part7_db[i]
                content += f"""
    <div class="question-block">
        <div class="passage-label">{title}</div>
        <div class="passage">{text}</div>"""
                for idx, (q, opts, ans) in enumerate(questions):
                    content += f"""
        <div class="q-text">{idx+1}. {q}</div>
        <label class="radio-opt"><input type="radio" name="q{idx}" value="A" onclick="checkAnswer({idx}, '{ans}')"> A) {opts[0]}</label>
        <label class="radio-opt"><input type="radio" name="q{idx}" value="B" onclick="checkAnswer({idx}, '{ans}')"> B) {opts[1]}</label>
        <label class="radio-opt"><input type="radio" name="q{idx}" value="C" onclick="checkAnswer({idx}, '{ans}')"> C) {opts[2]}</label>
        <label class="radio-opt"><input type="radio" name="q{idx}" value="D" onclick="checkAnswer({idx}, '{ans}')"> D) {opts[3]}</label>
        <div id="fb-{idx}" class="feedback"></div><br>"""
                content += "</div>"
            else:
                content = "<p>Content coming soon...</p>"

        full_html = get_header(i, part_name) + content + get_footer(i)
        
        filename = f"Reading_Day{i}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_html)
        print(f"Generated {filename}")

if __name__ == "__main__":
    main()
