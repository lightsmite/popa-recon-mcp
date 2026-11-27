FROM python:3.12-slim
WORKDIR /app
COPY popa_recon_mcp.py .
ENTRYPOINT ["python", "-u", "/app/popa_recon_mcp.py"]
