import requests, time, cv2
from flask import Flask, request

app = Flask(__name__)

regions = ['mx', 'us-ca']

@app.route("/picture", methods=['GET'])
def route():
    args = request.args
    key = args.get('key')
    return principal(key)

def principal(key):
    if key is None:
        return {"Error":"No key provided"}
    else:
        take_image()
        response = apiPlatesResponse()
        status = apiWebResponse(key, response['results'][0]['plate'])
        return {'plate':response['results'][0]['plate'],'key':key,'status':status['msg']}

def take_image():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Photo")
    while True:
        ret, frame = cam.read()
        time.sleep(1)
        if not ret:
            return {"Error":"Failed to capture image"}
        cv2.imshow("Test", frame)
        img_name = "picture.png".format(0)
        cv2.imwrite(img_name, frame)
        break
    cam.release()
    cv2.destroyAllWindows()

def apiPlatesResponse():
    with open('./picture.png', 'rb') as fp:
        response = requests.post('https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions), 
            files=dict(upload=fp),
            headers={'Authorization': 'Token 080c4b462d1ff7a3cd1c8775412f606d89c2687d'})
    return response.json()

def apiWebResponse(key, plate):
    response = requests.get(f'https://truck-manage-production.up.railway.app/api/verify-plate/{key}/{plate}')
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)