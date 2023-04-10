import requests
import json 
import base64

url_local = 'http://localhost:8080/2015-03-31/functions/function/invocations'
# url_lambda = "https://h8brgez541.execute-api.us-east-1.amazonaws.com/testing/predict"
url_lambda = "https://dxtayceow1.execute-api.ap-south-1.amazonaws.com/dev/convert"
# data1 = {"values":[[0.1,2,0.1,3]]}
# data2 ={"values":[[5.9,3.0,5.1,2.3]]}


filename = 'BI.docx'
# filename = 'docker_commands.pdf'
input_path = 'C:/Users/karth/Desktop/mydockerbuild/input_files/'+filename


# files = {'file': open(input_path, 'rb')}
with open(input_path, 'rb') as f:
#   contents = f.read()
#   files = {'file': f}
#   result1= requests.post(url_local, data=json.dumps({'pdf': base64.b64encode(f.read()).decode("ascii")}).encode())
  result1= requests.post(url_local, data = json.dumps({'file':base64.b64encode(f.read()).decode("ascii"),'target_format':'rtf','filename':filename}))
#   result1= requests.post(url_local, data=json.dumps({'pdf': base64.b64encode(f.read()).decode("ascii")}).encode())

# data = {'target_format':target_format}
# result1,result2 = requests.post(url_lambda, json=data1).json(),requests.post(url_lambda, json=data2).json()
# result1= requests.post(url_local, files=contents)
print(result1.content)


json_obj = json.loads(result1.content)
response = json.loads(json_obj["response"])

encoded_string = response["file"]
with open('./BI.rtf', "wb") as fi:
    fi.write(base64.b64decode(encoded_string))
print(json_obj)