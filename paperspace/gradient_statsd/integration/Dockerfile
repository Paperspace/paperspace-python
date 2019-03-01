FROM python:3.7.2
# docker will run the build with context as root and point to this docker file in this directory
COPY . /opt/gradient-statsd
WORKDIR /opt/gradient-statsd
RUN pip install -r requirements.txt
RUN cp -r gradient_statsd /usr/local/lib/python3.7/site-packages
# entrypoint
ENTRYPOINT ["python", "-u", "/opt/gradient-statsd/integration/entrypoint.py"]
