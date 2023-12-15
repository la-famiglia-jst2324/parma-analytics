FROM --platform=linux/amd64 mambaorg/micromamba:1.5.3

COPY --chown=$MAMBA_USER:$MAMBA_USER environment-prod.yml /tmp/environment.yml

RUN micromamba install -y -n base -f /tmp/environment.yml && \
    micromamba clean --all --yes

WORKDIR /app

COPY --chown=$MAMBA_USER:$MAMBA_USER parma_analytics /app/parma_analytics

ENV POSTGRES_HOST=$POSTGRES_HOST
ENV POSTGRES_PORT=$POSTGRES_PORT
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB

EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/_entrypoint.sh"]
CMD ["uvicorn", "parma_analytics.api:app", "--host", "0.0.0.0", "--port", "8080"]
