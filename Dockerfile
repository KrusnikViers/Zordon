FROM python:3-slim

# TODO: Add strict git reset --hard f9158e3129efd4ccdc291aefb840209791226a77 on release
RUN apt-get update                                            && \
    apt-get install -y git                                    && \
    mkdir /zordon                                             && \
    cd /zordon                                                && \
    git clone https://github.com/KrusnikViers/Zordon.git .    && \
    pip3 install --no-cache-dir --upgrade -r requirements.txt && \
    apt-get purge -y git                                      && \
    apt-get autoremove -y                                     && \
    apt-get clean

CMD ["/zordon/scripts/docker_entry.sh"]
