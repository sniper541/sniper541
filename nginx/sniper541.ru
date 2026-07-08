server {
    server_name sniper541.ru www.sniper541.ru;

    root /opt/project/sniper541/site;
    index owner.html;
    charset utf-8;

    location = /webdav {
        return 301 /webdav/;
    }

    location /webdav/ {
        alias /opt/project/;

        dav_methods     PUT DELETE MKCOL COPY MOVE;
        dav_ext_methods PROPFIND OPTIONS;
        dav_access      user:rw group:rw all:r;

        create_full_put_path on;
        client_max_body_size 0;

        auth_basic "WebDAV";
        auth_basic_user_file /etc/nginx/.htpasswd;

        autoindex on;
        add_header MS-Author-Via "DAV" always;
    }

    location / {
        try_files $uri $uri/ /owner.html;
    }

    location /map/get_places {
        alias /opt/project/sniper541/site/sites/map/data.json;
        default_type application/json;
        add_header Access-Control-Allow-Origin *;
    }

    location /map/save_places {
        proxy_pass http://127.0.0.1:5000/save_places;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location ~ ^/sites/(book|game|resume)/.*\.(css|js|png|jpg|jpeg|gif|ico|woff|woff2|ttf|svg|eot)$ {
        root /opt/project/sniper541/site;
        try_files $uri =404;
    }

    location /book {
        alias /opt/project/sniper541/site/sites/book;
        index index.html;
    }

    location /game {
        alias /opt/project/sniper541/site/sites/game;
        index index.html;
    }

    location /resume {
        alias /opt/project/sniper541/site/sites/resume;
        index index.html;
    }

    location /map {
        alias /opt/project/sniper541/site/sites/map;
        index index.html;
    }

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/sniper541.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/sniper541.ru/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    if ($host = www.sniper541.ru) {
        return 301 https://$host$request_uri;
    }

    if ($host = sniper541.ru) {
        return 301 https://$host$request_uri;
    }

    listen 80;
    server_name sniper541.ru www.sniper541.ru;
    return 404;
}
