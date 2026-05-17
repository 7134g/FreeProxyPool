FROM python:3.7

MAINTAINER 7134g

COPY ./ /app/proxy

WORKDIR /app/proxy

EXPOSE 5555

RUN pip3 install -r requirements.txt -i https://pypi.doubanio.com/simple
CMD python3 ./run.py