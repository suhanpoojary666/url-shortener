#use python environment
FROM python:3.14.6

#set /url-shortener as main DIR
WORKDIR /url-shortener

#copy the requirements file to main DIR(.)
COPY requirements.txt .

#install the dependencies
RUN pip install -r requirements.txt

#copy the application files to main DIR
COPY . .

#this runs the script files for migrate cmd
RUN chmod +x /url-shortener/entrypoint.sh

ENTRYPOINT ["/url-shortener/entrypoint.sh"]

#set the communication port to 8000
EXPOSE 8000

#use this cmd to start the app
CMD ["python","manage.py","runserver","0.0.0.0:8000"]