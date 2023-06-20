# import os
# from io import BytesIO
# import tarfile
# import subprocess
# import brotli
# import json
# import base64
# import boto3
# # import aspose.words as aw
# # from pdf2docx import Converter
# import tabula
# from pdf2docx import parse
from flask import Flask, request, redirect, jsonify,send_file
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './temp'
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024




@app.route('/upload', methods=['POST'])
def file_conversion():
    # json_data = request.json
    # target_format = json_data["target_format"]
    # filename = json_data["filename"]
    target_format = request.form['target_format']
    filename = request.form['filename']

    print('filename',filename)
    print('target_format',target_format)
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    

   
    headers = {'Access-Control-Allow-Headers': 'Content-Type','Access-Control-Allow-Origin': '*','Access-Control-Allow-Methods': 'OPTIONS,POST'}

 
    data =  {"statusCode":200,"headers":headers,"response": "upload succesfull"}
    return jsonify(data)


    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0")
