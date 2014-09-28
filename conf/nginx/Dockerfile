FROM dockerfile/ubuntu

# Install Nginx
RUN \
    add-apt-repository -y ppa:nginx/stable && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y nginx && \
    chown -R www-data:www-data /var/lib/nginx

# cleanup
RUN \
    apt-get clean && \
    rm -Rf /var/cache/apt

# Define mountable directories.
VOLUME ["/data", "/etc/nginx", "/var/log/nginx", "/ssl"]

# Define working directory.
WORKDIR /etc/nginx

# Define default command.
CMD ["nginx"]

# Expose ports.
EXPOSE 80
EXPOSE 443
