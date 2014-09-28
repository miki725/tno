FROM dockerfile/python

ADD requirements.txt /webapp/requirements.txt

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    libpng12-dev \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    nodejs-legacy \
    npm

# cleanup
RUN \
    apt-get clean && \
    rm -Rf /var/cache/apt

RUN npm install -g \
    less \
    yuglify

RUN pip install -r /webapp/requirements.txt

WORKDIR /webapp

# Define mountable directories.
VOLUME ["/data", "/webapp"]
