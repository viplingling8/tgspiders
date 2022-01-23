# 设置基础镜像
FROM togeek_data:V1.1

# 设置代码文件夹工作目录
RUN mkdir -p /root/dockerapp/tgspiders

# 复制当前代码文件到容器中
#ADD ./ tgspiders
COPY tgspiders.whl /root/dockerapp/tgspiders

WORKDIR /root/dockerapp/tgspiders

# 设置时间
#RUN cp /usr/share/zoneinfo/Asia/Shanghai/etc/localtime

# 安装所需的包，这里的requirement文件名需和项目生成的一致
#RUN pip install --trusted-host mirrors.tuna.tsinghua.edu.cn -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn.pypi/web/simple/
RUN pip install tgspiders.whl

# 执行入口文件
CMD ['python', 'main.py']