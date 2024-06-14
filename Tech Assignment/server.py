from flask import Flask, request, jsonify

app = Flask('Flask_Testing')
req_data = []

@app.route('/route/sensor/data', methods= ['GET'])
def push():
    return jsonify(req_data)

@app.route('/route/sensor/data',methods=['POST'])
def data():
    print(request.data)
    req_data.append(request.get_json())
    return "Success"

if __name__ == '__main__':
    app.run(host='0.0.0.0')