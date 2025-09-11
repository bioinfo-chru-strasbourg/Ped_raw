FROM almalinux:8
# WORKDIR /home1/data/WORKDIR_SOLENE/Ped_raw/Back
# COPY . .
ENV LC_CTYPE=en_US.UTF-8
RUN yum -y install python3.12
#-y = yes
RUN curl --silent --location https://rpm.nodesource.com/setup_16.x | bash -
RUN yum -y install nodejs
RUN python3.12 -m ensurepip --upgrade
RUN python3.12 -m pip install --upgrade pip
RUN python3.12 -m pip install Flask Flask-Cors openpyxl
RUN python3.12 -m pip install pronto
# ENTRYPOINT FLASK_APP=/home1/data/WORKDIR_SOLENE/Back/app.py flask run --host=0.0.0.0
CMD [ "python3.12", "/Back/app.py"]
