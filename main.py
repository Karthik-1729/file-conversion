import os
from io import BytesIO
import tarfile
import subprocess
import brotli
import json
import base64
import boto3
import aspose.words as aw
# from pdf2docx import Converter
import tabula
# from pdf2docx import parse


libre_office_install_dir = '/tmp/instdir'


def load_libre_office():
    if os.path.exists(libre_office_install_dir) and os.path.isdir(libre_office_install_dir):
        print('We have a cached copy of LibreOffice, skipping extraction')
    else:
        print('No cached copy of LibreOffice, extracting tar stream from Brotli file.')
        buffer = BytesIO()
        with open('/opt/lo.tar.br', 'rb') as brotli_file:
            d = brotli.Decompressor()
            while True:
                chunk = brotli_file.read(1024)
                buffer.write(d.decompress(chunk))
                if len(chunk) < 1024:
                    break
            buffer.seek(0)
        print('Extracting tar stream to /tmp for caching.')
        with tarfile.open(fileobj=buffer) as tar:
            tar.extractall('/tmp')
        print('Done caching LibreOffice!')
    return f'{libre_office_install_dir}/program/soffice.bin'




def convert_file_to_pdf(soffice_path, inp_file_path, output_dir):
    conv_cmd = f"{soffice_path} --headless --norestore --invisible --nodefault --nofirststartwizard --nolockcheck --nologo --convert-to pdf:calc_pdf_Export --outdir {output_dir} {inp_file_path}"
    response = subprocess.run(conv_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if response.returncode != 0:
        response = subprocess.run(conv_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if response.returncode != 0:
            return False
    return True

def convert_file(conv_cmd):
    # conv_cmd = f"{soffice_path} --headless --norestore --invisible --nodefault --nofirststartwizard --nolockcheck --nologo --convert-to docx --outdir {output_dir} {inp_file_path}"
    response = subprocess.run(conv_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if response.returncode != 0:
        response = subprocess.run(conv_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if response.returncode != 0:
            return False
    return True

def pdf2docx_convert(pdf_file,docx_file):
    # pdf_file = '/path/to/sample.pdf'
    # docx_file = 'path/to/sample.docx'
    # load the PDF file
    doc = aw.Document(pdf_file)

    # convert PDF to Word DOCX format
    doc.save(docx_file)
    # cv = Converter(pdf_file)
    # cv.convert(docx_file)
    # cv.close()

    return True

# def pdf2docx_convert(pdf_file,docx_file):
#     # pdf_file = '/path/to/sample.pdf'
#     # docx_file = 'path/to/sample.docx'
#     # load the PDF file
#     # doc = aw.Document(pdf_file)

#     # convert PDF to Word DOCX format
#     # doc.save(docx_file)
#     # cv = Converter(pdf_file)
#     # cv.convert(docx_file)
#     # cv.close()

# # convert pdf to docx
#     parse(pdf_file, docx_file)

#     return True

def pdf2pptx_convert(inp_file_path,out_path):
    # list_files=subprocess.run(["pdf2pptx",inp_file_path,"-o {}".format(out_path)])
    list_files=subprocess.run(["pdf2pptx",inp_file_path])
    return

def pdf_to_xls(data_path,output_path):
  dfs=tabula.read_pdf(data_path,pages='all')
  tabula.convert_into(data_path,output_path,output_format='csv',pages='all')
  return True
 

def convert_from_pdf(soffice_path,inp_file_path,out_path,target_format,upload_folder,basename,output_folder):
    if target_format == 'docx':
        temp_status = pdf2docx_convert(inp_file_path,out_path)
    elif target_format == 'txt' or target_format == 'rtf':
        temp_docx_path = f'{upload_folder}/{basename}.docx'
        temp_status = pdf2docx_convert(inp_file_path,temp_docx_path)
        conv_cmd = conv_cmd_gen(soffice_path, temp_docx_path, output_folder,'docx',target_format)
        conv_status = convert_file(conv_cmd)
        os.remove(temp_docx_path)
    elif target_format == 'pptx':
        temp_status = pdf2pptx_convert(inp_file_path,out_path)
    elif target_format == 'xlsx':
        temp_status = pdf_to_xls(inp_file_path,out_path)
    return True


def conv_cmd_gen(soffice_path, inp_file_path, output_dir,src_format,target_format):
    if src_format == 'pdf':
        conv_cmd = f"{soffice_path} --headless --infilter='writer_pdf_import' --norestore --invisible --nodefault --nofirststartwizard --nolockcheck --nologo --convert-to {target_format} --outdir {output_dir} {inp_file_path}"
    else:
        conv_cmd = f"{soffice_path} --headless --norestore --invisible --nodefault --nofirststartwizard --nolockcheck --nologo --convert-to {target_format} --outdir {output_dir} {inp_file_path}"    
    return conv_cmd

def upload_to_s3(file_path, bucket, key):
    s3 = boto3.client("s3")
    s3.upload_file(file_path, bucket, key)



def lambda_handler(event, context):
    target_format = event["target_format"]
    filename = event["filename"]
    key_prefix = 'tmp'
    bucket = 'kr-nmt'
    basename,src_format = filename.split('.')
    print('filename',filename)
    encoded_string = event["file"].encode('ascii')
    upload_folder = "/tmp"
    inp_file_path = os.path.join(upload_folder,filename)
    with open(os.path.join(upload_folder,filename), "wb") as fi:
        fi.write(base64.b64decode(encoded_string))
    output_folder = "/tmp"
    out_filename = filename.split('.')[0] + '.'+target_format
    out_path = os.path.join(output_folder,out_filename)
    soffice_path = load_libre_office()
    print('loading soffice succeful')
    headers = {'Access-Control-Allow-Headers': 'Content-Type','Access-Control-Allow-Origin': '*','Access-Control-Allow-Methods': 'OPTIONS,POST'}

    try:
        if target_format == 'pdf':
            conv_status = convert_file_to_pdf(soffice_path, inp_file_path, output_folder)
        elif (src_format != 'pptx') and (src_format != 'pdf'):
            conv_cmd = conv_cmd_gen(soffice_path, inp_file_path, output_folder,src_format,target_format)
            conv_status = convert_file(conv_cmd)
        elif src_format == 'pdf':
            conv_status = convert_from_pdf(soffice_path,inp_file_path,out_path,target_format,upload_folder,basename,output_folder)
        elif src_format == 'pptx':
            temp_status = convert_file_to_pdf(soffice_path, inp_file_path, output_folder)
            temp_pdf_path = f'{upload_folder}/{basename}.pdf'
            conv_status = convert_from_pdf(temp_pdf_path,out_path,target_format,upload_folder)
            os.remove(temp_pdf_path)
        else:
            print('conversion not possible')
            conv_status = False
        print('conversion status',conv_status)
        upload_to_s3(out_path, bucket, f"{key_prefix}/{out_filename}")
        response = f'https://kr-nmt.s3.ap-south-1.amazonaws.com/tmp/{out_filename}'
        os.remove(out_path)
        os.remove(inp_file_path)
        return {"statusCode":200,"headers":headers,"response":response}
    except:
        os.remove(inp_file_path)
        return {"statusCode":500,"headers":headers,"response":'',"errorMessage":'Currently,file conversion is not possible from {} to {}.'.format(src_format,target_format)}

    # headers = {'Access-Control-Allow-Headers': 'Content-Type','Access-Control-Allow-Origin': '*','Access-Control-Allow-Methods': 'OPTIONS,POST'}

    # return {"statusCode":200,"headers":headers,"response":response}
