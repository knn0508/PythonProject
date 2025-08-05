from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'simple-secret-key-for-vercel'

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Flask App</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
            .btn:hover { background: #0056b3; }
            .result { margin: 20px 0; padding: 15px; background: #e9ecef; border-radius: 5px; }
            input[type="text"] { width: 300px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Simple Flask App on Vercel</h1>
            <p><strong>Status:</strong> ✅ Successfully deployed!</p>
            <p><strong>Time:</strong> ''' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '''</p>
            
            <h3>Test API:</h3>
            <button class="btn" onclick="testAPI()">Test API Call</button>
            <div id="apiResult" class="result" style="display:none;"></div>
            
            <h3>Echo Test:</h3>
            <input type="text" id="echoInput" placeholder="Type something..." />
            <button class="btn" onclick="testEcho()">Echo</button>
            <div id="echoResult" class="result" style="display:none;"></div>
            
            <h3>Math Calculator:</h3>
            <input type="number" id="num1" placeholder="Number 1" />
            <select id="operation">
                <option value="add">+</option>
                <option value="subtract">-</option>
                <option value="multiply">×</option>
                <option value="divide">÷</option>
            </select>
            <input type="number" id="num2" placeholder="Number 2" />
            <button class="btn" onclick="calculate()">Calculate</button>
            <div id="calcResult" class="result" style="display:none;"></div>
        </div>
        
        <script>
            function testAPI() {
                fetch('/api/test')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('apiResult').style.display = 'block';
                        document.getElementById('apiResult').innerHTML = '<strong>API Response:</strong><br>' + JSON.stringify(data, null, 2);
                    });
            }
            
            function testEcho() {
                const text = document.getElementById('echoInput').value;
                fetch('/api/echo', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text})
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('echoResult').style.display = 'block';
                    document.getElementById('echoResult').innerHTML = '<strong>Echo:</strong> ' + data.echo;
                });
            }
            
            function calculate() {
                const num1 = parseFloat(document.getElementById('num1').value);
                const num2 = parseFloat(document.getElementById('num2').value);
                const operation = document.getElementById('operation').value;
                
                fetch('/api/calculate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({num1: num1, num2: num2, operation: operation})
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('calcResult').style.display = 'block';
                    if (data.error) {
                        document.getElementById('calcResult').innerHTML = '<strong>Error:</strong> ' + data.error;
                    } else {
                        document.getElementById('calcResult').innerHTML = '<strong>Result:</strong> ' + data.result;
                    }
                });
            }
        </script>
    </body>
    </html>
    '''

@app.route('/api/test')
def api_test():
    return jsonify({
        'status': 'success',
        'message': 'API is working!',
        'timestamp': datetime.now().isoformat(),
        'environment': 'vercel' if os.environ.get('VERCEL') else 'local'
    })

@app.route('/api/echo', methods=['POST'])
def api_echo():
    data = request.get_json()
    text = data.get('text', '')
    return jsonify({
        'echo': f"You said: {text}",
        'length': len(text),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    try:
        data = request.get_json()
        num1 = data.get('num1')
        num2 = data.get('num2')
        operation = data.get('operation')
        
        if num1 is None or num2 is None:
            return jsonify({'error': 'Both numbers are required'}), 400
            
        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                return jsonify({'error': 'Cannot divide by zero'}), 400
            result = num1 / num2
        else:
            return jsonify({'error': 'Invalid operation'}), 400
            
        return jsonify({
            'result': result,
            'operation': f"{num1} {operation} {num2} = {result}",
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True)
