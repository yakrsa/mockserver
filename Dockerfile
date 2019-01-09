# 1.指定基本镜像为Linux(alipine Docker镜像是只有5M的轻量级Linux系统)
FROM alpine:3.5

# 在alipine下安装python和pip，这个app是用Python写的，所以需要安装Python环境，通常是复制文件和安装依赖
RUN apk add --update py2-pip

# 安装app所需的Python所必须的
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# 复制应用必须的文件到镜像中
COPY src/*.py /usr/src/app/



# 设置需要暴露的端口号
EXPOSE 9898

# 设置应用通过cmd启动Python应用程序
CMD ["python", "/usr/src/app/mock_proxy.py"]