FROM rad_pipeline-image-base

USER docker

COPY ./requirements_dev.txt /requirements_dev.txt
RUN source /venv/bin/activate && pip install -r /requirements_dev.txt

WORKDIR /app

ENTRYPOINT source /venv/bin/activate && pip install -e . && jupyter notebook --ip=0.0.0.0 --port=8888
