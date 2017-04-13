FROM python:3.6.1

COPY requirements.txt /opt/geekhub/
RUN pip3 install --no-cache-dir -r /opt/geekhub/requirements.txt

ADD . /opt/geekhub/

WORKDIR /opt/geekhub/

CMD ["gunicorn", "-w 4", "-b 0.0.0.0", "wsgi:application"]
