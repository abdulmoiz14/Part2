FROM python:3.6
LABEL maintainer = "abdulmoiz1443@gmail.com"
COPY . /
WORKDIR /
RUN pip install -r requirements.txt
EXPOSE 8080
entrypoint ["python"]
CMD ["application.py"]
