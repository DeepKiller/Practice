# Состав:

## DCS - Директория проекта:
### UserControl - приложение для взаимодействия с пользователями:
Endpoint|Метод|Аргументы|Описание|Необходимая роль
:---:|:---:|:---:|:---:|:---:
/usercontrol/registration|POST|Email,Password - string|Регистрация нового пользователя|NONE
/usercontrol/login|POST|Email,Password - string|Вход в учётную запись|NONE
/usercontrol/delete|DELETE|Email - string|Удаление указанного пользователя|Admin
/usercontrol/view|GET|page - integer|Отображение списка пользователей на указанной странице|Admin

### FacilityControl - приложение для взаимодействия с установками:
Endpoint|Метод|Аргументы|Описание|Необходимая роль
:---:|:---:|:---:|:---:|:---:
/facilitycontrol/create|POST|Name, Description, SerialNumber - string, FirmwareVersion - Float|Создание установки|Admin
/facilitycontrol/delete|DELETE|id - integer|Удаление установки|Admin
/facilitycontrol/view|GET|page - integer|Отображение списка установок|Admin
/facilitycontrol/connect|PUT|UIN - string|Подключение установки|ALL
/facilitycontrol/change|PUT|Name, UIN, Description, DeviceMode, NetworkMode - string, LastCO2Value - float, NightModeEnabled, NightModeAuto - bool,NightModeFrom, NightModeTo - time|Изменение привязанной установки|User
/facilitycontrol/change|PUT|id - integer, fields - array|Изменяет указанные поля, у указанной установки|Admin
### LogControl - приложение для управления логами:
Endpoint|Метод|Аргументы|Описание|Необходимая роль
:---:|:---:|:---:|:---:|:---:
/logcontrol/create|POST| id - integer, logcontent - string|Добавляет лог для указанной установки|User
/logcontrol/view|GET|page - integer, id - integer(Only Admin)|Отображает список логов на указанной странице. Для администратора для запрошенной установки, для пользователя для привязанной.|ALL
/logcontrol/delete|DELETE|id - integer|Удаляет логия для указанной установки|Admin
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
