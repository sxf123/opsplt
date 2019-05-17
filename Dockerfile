FROM centos:latest
MAINTAINER sxf
RUN mkdir -p /opt/opsplt
COPY . /opt/opsplt
RUN yum update -y
RUN yum install -y epel-release
RUN yum install -y gcc gcc-c++ make
RUN yum install -y pcre pcre-devel zlib zlib-devel openssl openssl-devel readline readline-devel openssh openssh-clients openssh-server
RUN yum install -y supervisor
ADD Python-3.6.8.tgz /opt
WORKDIR /opt/Python-3.6.8
RUN ./configure --prefix=/opt/python36 && make && make install
ENV PATH $PATH:/opt/python36/bin
WORKDIR /opt/opsplt
RUN pip3 install -r requirements.txt
EXPOSE 8888
COPY supervisord.conf /etc
CMD ["supervisord","-c","/etc/supervisord.conf"]

