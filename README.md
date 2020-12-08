# Состав:

## DCS - Директория проекта:
	* UserControl - приложение для взаимодействия с пользователями:
		
	* FacilityControl - приложение для взаимодействия с установками.
	* LogControl - приложение для управления логами.
## SUU - Директория виртуальной среды.

# Развёртывание:

## 1. Необходимые компоненты:
	1.1. PostgreSQL
	1.2. Apache 
	1.3. Python
		
## 2. Развёртывание приложения:
	2.1. Необходимо указать базу данных в файле /DCS/DCS/settings.py, и указать данные пользователя.
		2.2.1 Официальное руководство - https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-DATABASES
		2.2.2 Необходимо выполнить миграцию, из виртуальной среды выполнить python ./DCS/manage.py migrate
	2.2. В (Расположение Apache)/conf/httpd.conf внести следующие пункты:
		2.2.1. WSGIScriptAlias / "(Расположение директории репозитория)/DCS/DCS/wsgi.py" application-group=%{GLOBAL}
		2.2.2. <Directory "(Расположение директории репозитория)/DCS/DCS">
    	    	 <Files wsgi.py>
      	      	  Require all granted
        		 </Files>
        		</Directory>
		2.2.3. LoadModule wsgi_module "(Расположение директории репозитория)/suu/lib/site-packages/mod_wsgi/server/mod_wsgi.cp39-win_amd64.pyd"
		2.2.4. WSGIPythonHome (Расположение Python)/lib;(Расположение директории репозитория)/suu/lib/site-packages;(Расположение Python)/dlls;(Расположение директории репозитория)/dcs;
	2.3. Запустить (Расположение Apache)/bin/httpd.exe для запуска сервера.
