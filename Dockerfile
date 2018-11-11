FROM python:3-slim

# RELEASE-UPDATE: Add strict git reset --hard <hash> on releases

# Set up project files.
RUN apt-get update                                         && \
    apt-get install -y git                                 && \
    mkdir /zordon                                          && \
    cd /zordon                                             && \
    git clone https://github.com/KrusnikViers/Zordon.git . && \
    apt-get purge -y git                                   && \
    apt-get autoremove -y                                  && \
    apt-get clean

# Set up python dependencies
RUN pip3 install --no-cache-dir --upgrade -r /zordon/requirements.txt

CMD ["/zordon/scripts/docker_entry.sh"]
