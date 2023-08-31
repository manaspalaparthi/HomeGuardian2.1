FROM continuumio/miniconda3

ENV PATH /opt/conda/bin:$PATH

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY . /app

WORKDIR /app

RUN conda env create -f env.yml

ENV CONDA_DEFAULT_ENV=homeguardian
ENV CONDA_PREFIX=/opt/conda/envs/$CONDA_DEFAULT_ENV
ENV PATH=$CONDA_PREFIX/bin:$PATH

#env varibles
ENV PYTHONPATH=/app


