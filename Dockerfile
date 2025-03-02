# 使用Python 3.8作为基础镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

# 安装系统依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        chromium \
        chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY requirements.txt .
COPY . .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建必要的目录
RUN mkdir -p instance/logs

# 设置权限
RUN chmod -R 755 /app

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "app.py"] 