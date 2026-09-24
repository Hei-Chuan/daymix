FROM python:3.12-slim
WORKDIR /app
COPY skills/daymix ./skills/daymix
COPY web/app.py web/storage.py ./web/
COPY web/public ./web/public
RUN useradd --system --uid 10001 daymix && mkdir /data && chown daymix:daymix /data
USER daymix
ENV DAYMIX_WEB_HOST=0.0.0.0 DAYMIX_WEB_PORT=8000 DAYMIX_WEB_DB=/data/daymix.sqlite3
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s CMD python -c "from urllib.request import urlopen; assert urlopen('http://127.0.0.1:8000/healthz', timeout=2).status == 200"
CMD ["python", "web/app.py"]
