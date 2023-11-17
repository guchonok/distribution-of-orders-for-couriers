# distribution-of-orders-for-couriers
REST API сервис для распределения заказов по курьерам. 

### запуск

* docker-compose up --build поднимет окружение бэкенда
* в docker-compose.yaml у сервиса backend:command имеется команда bash src/pre-start.sh для генерации начальных данных (3 курьера и 3 заказа). 
