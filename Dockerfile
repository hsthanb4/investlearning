# StockLearning 官方开发与回测容器镜像
FROM python:3.12-slim

WORKDIR /workspace

# 安装系统基础构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制并安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Jupyter Lab 与 Web 平台端口
EXPOSE 8888 8000

CMD ["python3", "-m", "http.server", "8000", "--directory", "web"]
