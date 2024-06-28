from flask import Flask, request, jsonify
import pymongo
from pymongo import MongoClient

app = Flask('Flask_Testing')
req_data = []

uri = 'mongodb+srv://2201020103:vqj8QxoY9llRIHXM@mydb.rvfulzg.mongodb.net/?retryWrites=true&w=majority&appName=myDB'
try:
    conn = MongoClient(uri)
    conn.server_info() 
except pymongo.errors.ServerSelectionTimeoutError as err:
    print(err)
    
mydb = conn.mydatabase
mycol = mydb.sensors_data

@app.route('/data', methods= ['GET'])
def push():
    return jsonify(req_data)

@app.route('/sensor1/temp/all', methods= ['GET'])
def allTemp():
    if request.args.get("sort")!=None and request.args.get("sort") != "":
        sort_stage = [("temp", 1 if request.args.get("sort", default="asc") == 'asc' else -1)]
        record = mydb.sensors_data.find().sort(sort_stage)
        data = [{"temp": rec["temp"]} for rec in record]
        return jsonify({
            "data": data
        })
    return jsonify({
        "data" : sum([data['temp'] for data in mydb.sensors_data.find()])
    })

@app.route('/sensor1/hum/all', methods= ['GET'])
def allHum():
    if request.args.get("sort")!=None and request.args.get("sort") != "":
        sort_stage = [("hum", 1 if request.args.get("sort", default="asc") == 'asc' else -1)]
        record = mydb.sensors_data.find().sort(sort_stage)
        data = [{"hum": rec["hum"]} for rec in record]
        return jsonify({
            "data": data
        })
    return jsonify({
        "data" : sum([data['hum'] for data in mydb.sensors_data.find()])
    })

@app.route('/sensor1/temp/avg', methods= ['GET'])
def avgTemp():
    result = list(mydb.sensors_data.aggregate([{"$group": {"_id": None, "averageTemp": {"$avg": "$temp"}}}]))
    avg_temp = result[0]['averageTemp'] if result else None
    return jsonify({
        "data": avg_temp
    })

@app.route('/sensor1/hum/avg', methods= ['GET'])
def avgHum():
    result = list(mydb.sensors_data.aggregate([{"$group": {"_id": None, "averageHum": {"$avg": "$temp"}}}]))
    avg_hum = result[0]['averageHum'] if result else None
    return jsonify({
        "data": avg_hum
    })


@app.route('/data',methods=['POST'])
def data():
    print(request.data)
    # rec_id1 = mycol.insert_one({
    #     "temp" : request.get_json()["temp"],
    #     "hum" : request.get_json()['hum']
    # })
    req_data.append(request.get_json())
    return "Success"

if __name__ == '__main__':
    app.run(host='0.0.0.0')