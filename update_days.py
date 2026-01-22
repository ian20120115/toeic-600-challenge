import os

def update_day_file(day_num):
    filename = f"c:/Users/ian20/OneDrive/桌面/English/TOEIC_Day{day_num}.html"
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the button to add
    back_btn = '        <a href="index.html" class="btn btn-learn" style="text-decoration:none; display:inline-flex; align-items:center; justify-content:center;">🏠 回主選單</a>'
    
    # Check if button already exists
    if "回主選單" in content:
        print(f"Day {day_num}: Button already exists.")
        return

    # Find insertion point (inside .nav div, before the first button)
    target = '<div class="nav">'
    replacement = f'<div class="nav">\n{back_btn}'
    
    if target in content:
        new_content = content.replace(target, replacement)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Day {day_num}: Updated.")
    else:
        print(f"Day {day_num}: Could not find .nav div.")

def main():
    for i in range(1, 31):
        update_day_file(i)

if __name__ == "__main__":
    main()
