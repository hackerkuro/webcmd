from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>Termux Web Shell</title>
    <style>
        body {
            background-color: black;
            color: white;
            font-family: monospace;
        }
        h1, h2 {
            color: #00ff00;
        }
        form {
            margin-bottom: 20px;
        }
        label {
            color: #00ff00;
        }
        input[type="text"] {
            background-color: #333;
            color: white;
            border: 1px solid #00ff00;
            padding: 5px;
            width: 80%;
        }
        input[type="submit"] {
            background-color: #00ff00;
            color: black;
            border: none;
            padding: 5px 10px;
            cursor: pointer;
        }
        pre {
            background-color: #333;
            padding: 10px;
            border: 1px solid #00ff00;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
    </style>
</head>
<body>
    <h1>Termux Web Shell</h1>
    <form method="post">
        <label for="command">type commond:</label>
        <input type="text" id="command" name="command" required>
        <input type="submit" value="execution">
    </form>
    <h2>result:</h2>
    <pre>{{ result }}</pre>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        command = request.form['command']
        try:
            # コマンドを実行して結果を取得
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        except subprocess.CalledProcessError as e:
            result = f"エラー: {e.output}"

    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)