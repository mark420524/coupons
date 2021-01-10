FROM python:3.7-slim

MAINTAINER Snow Wang <admin@farseer.vip>

WORKDIR /coupons
COPY requirements.txt requirements.txt
COPY . /coupons

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo '$TZ' > /etc/timezone && \
    mkdir /coupons && \
    pip install -r requirements.txt
    
ENTRYPOINT ["python", "/coupons/main.py"]
