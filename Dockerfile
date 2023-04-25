#Use offical PYTHON runtime

FROM python:3.8-slim-buster

#set working directory 
WORKDIR /app 

#Copy the code base in the current directory to the container /app
COPY . /app

#Upgrade pip
RUN pip3 install --upgrade pip

#Install needed packages 
RUN pip3 install -r requirements.txt

#Set default command to run when starting the container
CMD ["python", "app.py"]