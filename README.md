# DevOps Lab 10 — K8s Tools (Helm, Kustomize, Kompose)

## Описание проекта

Лабораторная работа по дополнительным инструментам Kubernetes:
- **Helm** — пакетный менеджер для Kubernetes
- **Kustomize** — оверлейная кастомизация манифестов
- **Kompose** — конвертация docker-compose в Kubernetes манифесты

---

## Структура репозитория
```
.
├── README.md
├── flask-redis-kustomize/          # Задание 1: Kustomize
│   ├── base/                       # Базовые манифесты
│   │   ├── flask-deployment.yaml
│   │   ├── flask-service.yaml
│   │   ├── kustomization.yaml
│   │   ├── redis-deployment.yaml
│   │   └── redis-service.yaml
│   ├── dev/                        # Dev окружение
│   │   ├── deployment-patch.yaml
│   │   ├── kustomization.yaml
│   │   └── service-patch.yaml
│   ├── prod/                       # Prod окружение
│   │   ├── deployment-patch.yaml
│   │   ├── kustomization.yaml
│   │   └── service-patch.yaml
│   └── flask-redis/                # Исходники приложения
│       ├── Dockerfile
│       ├── app.py
│       ├── compose.yaml
│       └── requirements.txt
├── prometheus-grafana-compose.yaml # Исходный docker-compose
├── promgra/                        # Задание 2: Helm chart
│   ├── Chart.yaml
│   ├── README.md
│   ├── values.yaml
│   └── templates/
│       ├── blackbox-deployment.yaml
│       ├── blackbox-service.yaml
│       ├── grafana-cm0-configmap.yaml
│       ├── grafana-data-persistentvolumeclaim.yaml
│       ├── grafana-deployment.yaml
│       ├── grafana-service.yaml
│       ├── prom-data-persistentvolumeclaim.yaml
│       ├── prometheus-cm0-configmap.yaml
│       ├── prometheus-deployment.yaml
│       └── prometheus-service.yaml
└── promgra-0.0.1.tgz               # Упакованный Helm chart
```
---

## Задание 1: Kustomize — Flask + Redis (dev/prod окружения)

### Описание

Базовое приложение Flask + Redis кастомизируется для двух окружений:
- **Dev**: 2 реплики Flask, порт сервиса 54321
- **Prod**: 5 реплик Flask, порт сервиса 12345

### Особенности реализации

- Имя Redis-сервера вынесено в переменную окружения `REDIS_HOST`
- Используется `namePrefix` для разделения ресурсов по окружениям
- Патчи через `patches` с `labelSelector` для точечной модификации
- Общие лейблы `app: devops-course-2025` добавляются ко всем ресурсам

### Команды для проверки

```bash
# Применить dev окружение
kubectl apply -k flask-redis-kustomize/dev/

# Применить prod окружение
kubectl apply -k flask-redis-kustomize/prod/

# Проверить сервисы
minikube service dev-service-devops --url
minikube service prod-service-devops --url

# Проверить curl
curl http://<dev-url>
curl http://<prod-url>

Результат

```
Dev:  Hello World! My env: DEVELOPMENT
Prod: Hello World! My env: PRODUCTION
```

Задание 2: Helm — Prometheus + Grafana
Описание
Helm-chart создан из docker-compose проекта prometheus-grafana через kompose convert --chart.
Особенности реализации
Chart создан через Kompose из docker-compose.yml
Добавлен type: LoadBalancer и externalIPs в сервисы Grafana и Prometheus
Добавлен values.yaml с переменными:
EXTERNAL_IP — внешний IP для сервисов
EXTERNAL_PORT — порт Grafana
GF_ADMIN_PASSWORD — пароль администратора Grafana
Шаблон grafana-service.yaml использует {{ .Values.EXTERNAL_PORT }} и {{ .Values.EXTERNAL_IP }}
Выполнен upgrade релиза с переопределением порта на 3456
Команды для проверки

```
# Установить релиз
```
helm install promgra ./promgra-0.0.1.tgz
```
# Проверить статус
```
helm list
kubectl get all
```
# Получить URL сервисов
```
minikube service grafana --url
minikube service prometheus --url
```
# Проверить curl
curl http://<grafana-url>    # → <a href="/login">Found</a>
curl http://<prometheus-url> # → <a href="/query">Found</a>

# Проверить значения релиза
helm get values promgra

# Upgrade с новым портом
helm upgrade promgra ./promgra-0.0.1.tgz --set EXTERNAL_PORT=3456
```
Результат
Table
Сервис	URL	Статус
Grafana	http://192.168.49.2:31359	✅ Welcome to Grafana
Prometheus	http://192.168.49.2:31107	✅ Query page

Технологии
Kubernetes (minikube)
Helm v4.2.2
Kustomize (встроен в kubectl)
Kompose v1.34.0
Docker
Python/Flask
Redis
Prometheus
Grafana

Автор
AndreySokolovInterprogram
