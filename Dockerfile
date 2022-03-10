# Python version can be changed, e.g.
# FROM python:3.8
# FROM docker.io/fnndsc/conda:python3.10.2-cuda11.6.0
FROM docker.io/python:3.10.2-slim-buster

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="Surface Smoothness Error" \
      org.opencontainers.image.description="A ChRIS plugin to calculate smoothness error (difference in curvature between neighbor vertices) for surfaces."

WORKDIR /usr/local/src/pl-smoothness-error

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install .

CMD ["smtherr", "--help"]
