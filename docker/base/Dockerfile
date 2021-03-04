# A multi-stage python build to create a smaller final image
# As described in the blog posts at https://pythonspeed.com/articles/smaller-python-docker-images/

# The build-stage image:
ARG USER
FROM continuumio/miniconda3 AS build

# Install the package as normal:
COPY ./setup/environment.yml /environment.yml
RUN conda env create -f environment.yml

# Install conda-pack:
RUN conda install -c conda-forge conda-pack

# Use conda-pack to create a standalone environment
# in /venv:
RUN conda-pack -n rad_pipeline_env -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack

# The runtime-stage image; we can use Debian as the
# base image since the Conda env also includes Python
# for us.
FROM debian:buster AS runtime

# Copy /venv from the previous stage:
COPY --from=build /venv /venv

ARG UID
RUN useradd docker -l -u $UID -s /bin/bash -m

RUN chown $UID:1000 /venv

USER docker

# When image is run, run the code with the environment
# activated:
SHELL ["/bin/bash", "-c"]
ENTRYPOINT source /venv/bin/activate && \
           python -c "import numpy; print('success!')"
