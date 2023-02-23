FROM python:3.10-slim-buster

WORKDIR /backend-flask

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"] 
#Replacing the CMD command above with the following comand and using bash script to run the command: python3 -m flask run --host=0.0.0.0 --port=4567
ADD run_flask_server.sh /
RUN chmod 777 /run_flask_server.sh 
CMD ["/run_flask_server.sh"]