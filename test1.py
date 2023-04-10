import requests
import json 
import base64

url_local = 'http://localhost:8080/2015-03-31/functions/function/invocations'
# url_lambda = "https://h8brgez541.execute-api.us-east-1.amazonaws.com/testing/predict"
url_lambda = "https://dxtayceow1.execute-api.ap-south-1.amazonaws.com/dev/convert"
# data1 = {"values":[[0.1,2,0.1,3]]}
# data2 ={"values":[[5.9,3.0,5.1,2.3]]}


filename = 'sample1.rtf'
input_path = 'C:/Users/karth/Desktop/mydockerbuild/input_files/'+filename


# files = {'file': open(input_path, 'rb')}
with open(input_path, 'rb') as f:
#   result1= requests.post(url_lambda, data = json.dumps({'file':base64.b64encode(f.read()).decode("ascii"),'target_format':'pdf','filename':filename}))
#   print(json.dumps({'file':base64.b64encode(f.read()).decode("ascii"),'target_format':'pdf','filename':filename}))
  out_file = open("myfile.json", "w")
  dict1 = {'file':base64.b64encode(f.read()).decode("ascii"),'target_format':'pdf','filename':filename}
  json.dump(dict1, out_file)
  out_file.close()
