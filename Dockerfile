FROM python:3.10.6-slim-bullseye

ARG VERSION=0.1.0

RUN useradd -ms /bin/bash dans

USER dans
WORKDIR /home/dans
ENV PYTHONPATH=/home/dans/dans-file-format-service/src
ENV BASE_DIR=/home/dans/dans-file-format-service
RUN mkdir -p ${BASE_DIR}

COPY ./dist/*.* .

#
RUN mkdir -p ${BASE_DIR}&& \
    pip install --no-cache-dir *.whl && rm -rf *.whl && \
    tar xf dans_file_format_service-${VERSION}.tar.gz -C ${BASE_DIR} --strip-components 1


CMD ["python", "dans-file-format-service/src/main.py"]
#CMD ["tail", "-f", "/dev/null"]