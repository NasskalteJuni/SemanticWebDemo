FROM python:3.9-buster

ARG NB_USER=sparql
ARG NB_UID=1234
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}
RUN adduser --disabled-password --gecos "Default user" --uid ${NB_UID} ${NB_USER}
WORKDIR ${HOME}
COPY . .
USER root
RUN pip install --no-cache-dir -r ./requirements.txt
RUN jupyter nbextension install --py hide_code
RUN jupyter nbextension enable --py hide_code
RUN jupyter serverextension enable --py hide_code
RUN chown -R ${NB_UID} ${HOME}
# USER ${NB_USER}

EXPOSE 80
CMD ["jupyter", "notebook", "--NotebookApp.token=sparql_and_rdf", "--NotebookApp.iopub_data_rate_limit=1e10", "--port=80", "--ip=0.0.0.0", "--no-browser", "index.ipynb"]
