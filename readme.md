---

# Flask Microservice con PostgreSQL y Kubernetes

## Descripción del Proyecto

Este proyecto implementa un **microservicio Flask** que realiza operaciones CRUD sobre una base de datos **PostgreSQL**, containerizado con **Docker**, desplegado en **Kubernetes** mediante **Helm**, y automatizado con **CI/CD usando GitHub Actions**.

El proyecto está preparado para futura integración con **ArgoCD** para despliegues declarativos y sincronización automática.

---

## Tecnologías Utilizadas

* Python 3.10 + Flask
* PostgreSQL
* Docker
* Kubernetes
* Helm
* GitHub Actions (CI/CD)
* (Pendiente) ArgoCD

---

## Estructura del Proyecto

```bash
/flask-microservice
├─ app.py                     # Microservicio Flask con CRUD
├─ requirements.txt           # Dependencias de Python
├─ Dockerfile                 # Dockerfile del microservicio
├─ helm-chart/                # Helm chart para Kubernetes
│  ├─ Chart.yaml
│  ├─ values.yaml
│  └─ templates/
│     ├─ deployment.yaml      # Deployment del microservicio
│     ├─ service.yaml         # Service NodePort para Flask
│     └─ postgres-service.yaml # Service ClusterIP para PostgreSQL
└─ .github/workflows/ci-cd.yaml # Pipeline CI/CD
```

---

## Endpoints del Microservicio

| Método | Ruta          | Descripción                             |
| ------ | ------------- | --------------------------------------- |
| GET    | `/`           | Health check                            |
| GET    | `/items`      | Listar todos los items                  |
| POST   | `/items`      | Crear un item (`{"name": "item_name"}`) |
| PUT    | `/items/<id>` | Actualizar un item existente            |
| DELETE | `/items/<id>` | Eliminar un item existente              |

---

## Dockerización

* **Dockerfile:**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

* **Construcción y prueba local:**

```bash
docker build -t flask-app:latest .
docker run -p 5000:5000 flask-app:latest
```

* Acceder a: `http://localhost:5000/`

---

## Kubernetes / Helm

### Despliegue Microservicio

* **Service NodePort (`service.yaml`):**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-service
spec:
  type: NodePort
  selector:
    app.kubernetes.io/name: flask-microservice
  ports:
    - port: 5000
      targetPort: 5000
      nodePort: 30942
```

* Despliegue con Helm:

```bash
helm upgrade --install flask-microservice ./helm-chart \
  --set image.repository=flask-app \
  --set image.tag=latest
```

### Servicio PostgreSQL

* **Service ClusterIP (`postgres-service.yaml`):**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  selector:
    app: postgres
  ports:
    - port: 5432
      targetPort: 5432
  type: ClusterIP
```

* Flask se conecta usando:

```python
host='postgres', port=5432, dbname='itemsdb', user='postgres', password='pass123'
```

---

## CI/CD – GitHub Actions

Pipeline automatizado:

1. Detecta commits en `master`.
2. Ejecuta pruebas unitarias (`pytest`).
3. Construye la imagen Docker.
4. Despliega en Kubernetes usando Helm.

* **Archivo:** `.github/workflows/ci-cd.yaml`

```yaml
# (Contenido completo del pipeline que ya compartiste)
```

---

## ArgoCD (Pendiente)

* Objetivo: Integrar despliegue declarativo y sincronización automática desde Git.
* Pasos futuros:

  1. Instalar ArgoCD en el clúster.
  2. Configurar repositorio Git como fuente.
  3. Crear aplicación apuntando al Helm chart.
  4. Validar sincronización automática al hacer commit.

---

## Verificación

* Ver pods y servicios:

```bash
kubectl get pods
kubectl get svc
kubectl port-forward svc/flask-service 5000:5000
```

* Acceder a microservicio:

```bash
curl http://localhost:5000/
curl http://localhost:5000/items
```

---

## Observaciones

* Microservicio funcional con Docker, PostgreSQL y Kubernetes.
* Pipelines CI/CD completamente automatizados.
* Documentación clara y lista para entrega.
* ArgoCD documentado para futura integración.

---

