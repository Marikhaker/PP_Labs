from wsgiref.simple_server import make_server
from flask import Flask

app = Flask(__name__)

@app.route('/api/v1/hello-world-23')
def hello_world():
    return 'Hello World! 23'

with make_server('', 8080, app) as server:
    print("Main http://127.0.0.1:8080")
    print("Hello World! http://127.0.0.1:8080/api/v1/hello-world-23")
    server.serve_forever()

if __name__ == '__main__':
    app.run()

# flask