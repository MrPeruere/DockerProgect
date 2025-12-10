FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html
COPY events.html /usr/share/nginx/html/events.html
COPY register.html /usr/share/nginx/html/register.html
COPY CSS_file.css /usr/share/nginx/html/CSS_file.css
COPY Js_file.js /usr/share/nginx/html/Js_file.js

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]