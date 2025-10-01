from flask import Flask, render_template, request
import re

app = Flask(__name__)

def clean_words(text):
    # remove punctuation and split into usable words
    text = re.sub(r'[^\w\s]', '', text)
    words = [w for w in text.split() if len(w) > 1 and w.lower() != "podcast"]
    return words

def one_word(text):
    words = clean_words(text)
    modified = []
    for w in words:
        modified.append(f"{w} podcast")
        modified.append(f"{w} podcasts")
    return ", ".join(modified)

def two_words(text):
    words = clean_words(text)
    modified = []
    for i in range(len(words) - 1):
        pair = f"{words[i]} {words[i+1]}"
        modified.append(f"{pair} podcast")
        modified.append(f"{pair} podcasts")
    return ", ".join(modified)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    action = ""
    if request.method == 'POST':
        description = request.form.get('description', '').strip()
        action = request.form.get('action', '')
        # debug print to console so you can verify which button value reached the server
        print("DEBUG: received action ->", action)

        if description:
            if action == 'one_word':
                result = one_word(description)
            elif action == 'two_words':
                result = two_words(description)
            else:
                result = "Invalid action. Use the buttons provided."

    return render_template('index.html', result=result, action=action)

if __name__ == '__main__':
    app.run(debug=True)
