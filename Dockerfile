FROM docker.io/fnndsc/pl-smoothness-error:base-1

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="pl-smoothness-error" \
      org.opencontainers.image.description="A ChRIS plugin to calculate smoothness error (difference in curvature between neighbor vertices) for surfaces."

WORKDIR /usr/local/src/pl-smoothness-error

RUN conda install -c conda-forge -y numpy=1.22.3

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install .

CMD ["smtherr", "--help"]
