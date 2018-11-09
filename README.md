<h3>Бота можно найти и протестировать здесь в телеграме:  @geojs_bot</h3>
<h3>Что начать работу наберите "info" и  бот выведет список доступных комманд. Для загрузки geojson файла можно использовать drug &amp; drop или кнопку загрузки.</h3>
<h2>Инструкция к установке:</h2>
Что бы обрабатывать POST запросы от API телеграма бот использует FLASK и необходимо установить самоподписной SSL сертификат иначе телеграм API не работает, следующие шаги буду об этом. Если все это настроено, то можно скопировать репозиторий в папку с проектом Flask и настроить <strong>config.py</strong>.

<strong>Установка Nginx:</strong>
<ul class="prefixed">
 	<li class="line">
<pre>sudo apt-get update</pre>
</li>
 	<li class="line">
<pre>sudo apt-get install python-pip python-dev nginx</pre>
</li>
</ul>
<strong>Cоздание виртуального окружения и установка нужных библиотек:</strong>
<ul class="prefixed">
 	<li class="line">
<pre>mkdir ~/<span class="highlight">myproject  </span></pre>
</li>
 	<li class="line">
<pre>cd ~/<span class="highlight">myproject</span></pre>
</li>
 	<li class="line">
<pre><span class="highlight">virtualenv myprojectenv</span></pre>
</li>
 	<li class="line">
<pre><span class="highlight">source myprojectenv/bin/activat</span></pre>
</li>
 	<li class="line">
<pre>pip install uwsgi flask</pre>
</li>
 	<li class="line">
<pre>pip install pytelegrambotapi, requests</pre>
</li>
</ul>
Скопировать репозиторий в папку <strong>/myproject </strong>и в файле wsgi.py поменять путь для логгирования если папка не существует.

Создать Unitfile что бы линукс система автоматическеи запускала и uWSGI.
<ul>
 	<li>
<pre>sudo nano /etc/systemd/system/<span class="highlight">myproject</span>.service</pre>
</li>
</ul>
Добавить это в файл:
<pre style="padding-left: 90px;">[Unit]
Description=uWSGI instance to serve myproject
After=network.target

[Service]
User=user
Group=www-data
WorkingDirectory=/home/user/myproject
Environment="PATH=/home/user/myproject/myprojectenv/bin"
ExecStart=/home/user/myproject/myprojectenv/bin/uwsgi --ini myproject.ini

[Install]
WantedBy=multi-user.target</pre>
Запустить сервис:
<ul class="prefixed">
 	<li class="line">
<pre>sudo systemctl start <span class="highlight">myproject</span></pre>
</li>
 	<li class="line">
<pre>sudo systemctl enable <span class="highlight">myproject</span></pre>
</li>
</ul>
<span class="highlight">*После этого в папке my project </span>

Создаем блок конфиграции Nginx:
<ul>
 	<li>
<pre>sudo nano /etc/nginx/sites-available/<span class="highlight">myproject</span></pre>
</li>
</ul>
поместить вот это в файл:
<pre>server { 

listen 443 default ssl; server_name ваш_ип; 
keepalive_timeout 60; ssl_certificate /etc/ssl/server.crt; 
ssl_certificate_key /etc/ssl/server.key; 
ssl_protocols TLSv1 TLSv1.1 TLSv1.2; ssl_ciphers "HIGH:!RC4:!aNULL:!MD5:!kEDH"; 
add_header Strict-Transport-Security 'max-age=604800'; 
access_log /var/log/nginx_access.log; 
error_log /var/log/ngingx_error.log; 
location / { include uwsgi_params; uwsgi_pass unix:/home/user/myproject/myproject.sock;

 } }</pre>
Cоздадим самоподписной SSL сертификат:
<ul>
 	<li class="highlight">
<pre>cd /etc/ssl/</pre>
</li>
 	<li class="highlight">
<pre>sudo openssl genrsa -des3 -passout pass:x -out server.pass.key 2048</pre>
</li>
 	<li class="highlight">
<pre>sudo openssl rsa -passin pass:x -in server.pass.key -out server.key</pre>
</li>
 	<li class="highlight">
<pre>sudo openssl req -new -key server.key -out server.cs</pre>
</li>
 	<li>
<pre>sudo openssl x509 -req -sha256 -days 365 -in server.csr -signkey server.key -out server.crt</pre>
</li>
</ul>
Проверим что фаил конфигурации Nginx настроен и запустим его:
<ul>
 	<li class="highlight">
<pre>sudo nginx -t</pre>
</li>
 	<li class="highlight">
<pre>sudo service nginx restart</pre>
</li>
</ul>
&nbsp;
<h3>Теперь осталось настроить файл config.py</h3>
<ul>
 	<li>
<pre>token='672334303:AAHLJsGUU7gs8rwKhJA5jROrQDPyX5FJA2g' # токен телеграм бота</pre>
</li>
 	<li>
<pre>dir_path='/home/user/myproject/' # путь в котором находится ваш проект, если это не myproject то нужно поменять</pre>
</li>
 	<li>
<pre>WEBHOOK_SSL_CERT = '/etc/ssl/server.crt' # путь к созданным SSL сертификатам</pre>
</li>
 	<li>
<pre>HOST = '104.248.35.29' # ваш IP адресс</pre>
</li>
</ul>
Если все прошло успешно то бот должен работать.