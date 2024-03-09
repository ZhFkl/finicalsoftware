FROM python:3.8
WORKDIR /app
COPY ./ ./
# RUN sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list 
RUN rm -Rf /var/lib/apt/lists/* && apt-get update
RUN apt-get install -y graphviz xdg-utils
RUN pip install -r requirements.txt 
# -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install ./3rdparty/ExKMC
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
