FROM python:3.8.15


# Required for LibreOffice
COPY lo.tar.br   /opt/

# COPY main.py ./

COPY requirements.txt .

# RUN yum install mesa-libGL -y
COPY inp_files ./inp_files
# RUN python -m pip install --upgrade pip
# RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install -r requirements.txt

# RUN  pip3 install -r requirements.txt

COPY fullchain.pem ./
COPY privkey.pem ./

COPY app.py ./



# CMD ["main.lambda_handler"]

CMD ["app.py"]
ENTRYPOINT ["python"]
