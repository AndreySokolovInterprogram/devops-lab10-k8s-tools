# DevOps Lab 10 — K8s Tools (Helm, Kustomize, Kompose)

## Задание 1: Kustomize — Flask + Redis (dev/prod окружения)

Структура:
- `flask-redis-kustomize/base/` — базовые манифесты
- `flask-redis-kustomize/dev/` — dev окружение (2 реплики, порт 54321)
- `flask-redis-kustomize/prod/` — prod окружение (5 реплик, порт 12345)

Приложение вынесено имя Redis-сервера в переменную окружения `REDIS_HOST`.

## Задание 2: Helm — Prometheus + Grafana

Helm-chart создан через `kompose convert --chart` из docker-compose.

- `promgra/` — helm chart
- `promgra-0.0.1.tgz` — упакованный chart

## Команды для проверки

```bash
# Kustomize
kubectl apply -k dev/
kubectl apply -k prod/
minikube service dev-service-devops --url
minikube service prod-service-devops --url

# Helm
helm install promgra ./promgra-0.0.1.tgz
minikube service grafana --url
minikube service prometheus --url