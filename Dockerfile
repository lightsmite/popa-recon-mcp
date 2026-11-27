FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY popa_recon_mcp.py .
USER nobody
ENTRYPOINT ["python", "-u", "/app/popa_recon_mcp.py"]
