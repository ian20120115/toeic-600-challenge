import glob
import os
import re

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content

    # Check if fully patched (Audio + Progress)
    if "speak(wordsDB[${index}].sent)" in content and "function markComplete()" in content:
        print(f"Skipping {os.path.basename(filepath)} (already fully patched)")
        return

    # Check if BROKEN patch exists (missing ${})
    if "speak(wordsDB[index].sent)" in content:
        print(f"Repairing {os.path.basename(filepath)} (fixing broken patch)")
        # Replace the broken function call with the correct one
        new_content = content.replace("speak(wordsDB[index].sent)", "speak(wordsDB[${index}].sent)")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return

    # If we are here, it means the file has NO button at all.
    # --- NEW: Inject Mark Complete Button ---
    # Check if we already have the markComplete script
    if "function markComplete()" not in content:
        # We can inject it before </body>
        # Generic button HTML
        complete_btn_html = '''
    <div style="text-align: center; margin-top: 40px; margin-bottom: 20px;">
        <button onclick="markComplete()" style="padding: 15px 30px; background: #27ae60; color: white; border: none; border-radius: 50px; font-size: 18px; cursor: pointer; font-weight: bold; box-shadow: 0 4px 15px rgba(39,174,96,0.3);">✅ 完成今日學習 (Mark Complete)</button>
    </div>

<script>
    function markComplete() {
        const pageId = window.location.pathname.split('/').pop().replace('.html', '');
        localStorage.setItem('EnglishHub_Progress_' + pageId, 'true');
        alert('Good job! 今日學習進度已保存。');
        location.href = 'index.html';
    }
</script>
</body>'''
        content = content.replace("</body>", complete_btn_html)

    # 1. Update forEach loop to include index (Existing Logic)
    # Pattern: wordsDB.forEach(item => {
    # Replacement: wordsDB.forEach((item, index) => {
    content = content.replace("wordsDB.forEach(item => {", "wordsDB.forEach((item, index) => {")

    # 2. Inject Button
    # Button HTML to inject
    # We must use ${index} so that the template literal evaluates to wordsDB[0], wordsDB[1], etc.
    btn_html = ' <button class="speak-btn" style="width:24px; height:24px; font-size:12px; display:inline-flex; vertical-align:middle; margin-left:5px;" onclick="speak(wordsDB[${index}].sent)" title="Listen">🔊</button>'
    
    # Pattern 1: With quotes (e.g. <div class="sentence">"${item.sent}"</div>)
    pattern1 = r'(<div class="sentence">"\${item.sent}")(</div>)'
    
    # Pattern 2: Without quotes (e.g. <div class="sentence">${item.sent}</div>) - Common in TOEIC
    pattern2 = r'(<div class="sentence">\${item.sent})(</div>)'
    
    if re.search(pattern1, content):
        new_content = re.sub(pattern1, r'\1' + btn_html + r'\2', content)
    elif re.search(pattern2, content):
        new_content = re.sub(pattern2, r'\1' + btn_html + r'\2', content)
    else:
        new_content = content

    if new_content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Patched {os.path.basename(filepath)}")
    else:
        print(f"Warning: Could not patch {os.path.basename(filepath)} (no changes needed or pattern not found)")

def main():
    base_dir = "c:/Users/ian20/OneDrive/桌面/English"
    patterns = [
        "TOEIC_Day*.html",
        "Aviation_Day*.html",
        "SimRacing_Day*.html",
        "Travel_Day*.html"
    ]

    for p in patterns:
        files = glob.glob(os.path.join(base_dir, p))
        for file in files:
            patch_file(file)

if __name__ == "__main__":
    main()
