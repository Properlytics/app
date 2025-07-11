
from flask import Flask, request, render_template, send_file
import openai
import json
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Template load error: {e}", 500

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['property_data']
        data = json.load(file)

        prompt = f"""
        You are a real estate analyst at Properlytics. Based on the following property data, generate a professional 2-page investment memo:

        {data}
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You generate investment memos for real estate investors."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        memo_text = response.choices[0].message.content
        with open("investment_memo.txt", "w") as f:
            f.write(memo_text)

        return send_file("investment_memo.txt", as_attachment=True)

    except Exception as e:
        return f"Something went wrong: {e}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
