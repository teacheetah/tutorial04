FROM nginx
COPY ./config/nginx.conf /etc/nginx/conf.d/default.conf

# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "curl", "-f", "http://localhost/" ]
