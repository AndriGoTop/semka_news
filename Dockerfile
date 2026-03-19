FROM python:3.14-slim
LABEL authors="adndi"



ENTRYPOINT ["top", "-b"]