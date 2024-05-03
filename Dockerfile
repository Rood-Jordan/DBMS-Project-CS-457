# Dockerfile, image, container
FROM python:3.10.5

WORKDIR /DBMS-PROJECT-CS-457

COPY . .

ADD PA5-Rood.py .

RUN pip install colorama 

CMD ["python", "./PA5-Rood.py"]

# run in terminal to create image
    # docker build -t python_dbms .

# run image
    # docker run -i -t python_dbms

# -i flag signals to docker that image is interactive aka user input
# -t flag commands docker to create a pseudo terminal to interact with the image 