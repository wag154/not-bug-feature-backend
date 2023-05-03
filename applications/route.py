from applications import app

@app.route('/')
def hello():
    return 'hello', 200