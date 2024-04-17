FROM python:3.9

# install underlying dependencies
RUN apt-get update && apt-get install -y python3-opencv

WORKDIR /tmp

COPY requirements.txt .
COPY yolov8_tracking/requirements.txt requirements-model.txt

RUN pip install --upgrade pip
# to cater for lap installation error where it cannot find numpy
RUN pip install numpy 
RUN pip install -r requirements.txt
RUN pip install -r requirements-model.txt

COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/supervisor/conf.d/

WORKDIR /app

COPY *.py .
COPY parser/ parser/
COPY utils/ utils/
COPY yolov8_tracking/ yolov8_tracking/

EXPOSE 9090

CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
