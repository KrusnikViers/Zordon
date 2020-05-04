FROM python:3-slim

# Set up python dependencies
COPY requirements.txt /
RUN pip3 install --no-cache-dir --upgrade -r /requirements.txt

# Set up project files.
COPY app /instance/app
COPY scripts /instance/scripts
CMD ["/instance/scripts/docker_entry.sh"]
