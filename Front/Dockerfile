FROM almalinux:8
RUN mkdir /Front
# COPY . /Front
WORKDIR /Front
ENV LC_CTYPE=en_US.UTF-8
#-y = yes
RUN curl --silent --location https://rpm.nodesource.com/setup_16.x | bash -
RUN yum -y install nodejs
RUN npm install vue --save
RUN npm install axios@1.3.6 --save
CMD [ "npm","run","dev", "--", "--host=0.0.0.0"]



