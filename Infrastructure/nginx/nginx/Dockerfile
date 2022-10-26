from nginx:latest

COPY ui-statics.conf /etc/nginx/conf.d
RUN rm /etc/nginx/conf.d/default.conf
RUN mkdir -p /app/build

CMD ["nginx", "-g", "daemon off;"]
