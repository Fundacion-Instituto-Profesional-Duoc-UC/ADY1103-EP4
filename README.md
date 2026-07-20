# 🚀 Evaluación Parcial 4 (EP4)
## Auditoría FinOps y Observabilidad Financiera en la Nube

---

## 📖 Descripción

En esta cuarta evaluación asumirás el rol de **FinOps Practitioner**, dando continuidad al caso de estudio desarrollado durante el semestre.

El objetivo es analizar el comportamiento financiero de una infraestructura cloud mediante métricas históricas simuladas en AWS CloudWatch.

Se proporciona una aplicación en Python capaz de inyectar telemetría financiera histórica, simulando costos operacionales asociados a distintos servicios, regiones y entornos.

A partir de esto deberás:

- Analizar comportamiento de costos.
- Segmentar gastos mediante dimensiones.
- Construir dashboards financieros.
- Identificar patrones de consumo.
- Configurar alarmas preventivas.
- Elaborar recomendaciones de optimización.

El entregable final es un informe ejecutivo con análisis, conclusiones y evidencias.

---

## 🎯 Objetivos de la Evaluación

- Comprender fundamentos de FinOps.
- Analizar métricas financieras en AWS CloudWatch.
- Segmentar costos mediante dimensiones.
- Construir dashboards financieros.
- Identificar oportunidades de optimización.
- Implementar monitoreo financiero preventivo.

---

## 📑 Contenido

- [Prerrequisitos](#-prerrequisitos)
- [Configuración del Entorno](#️-configuración-del-entorno)
- [Ejecución del Simulador](#-ejecución-del-simulador)
- [Diccionario de Métricas FinOps](#-diccionario-de-métricas-finops)
- [Limpieza del Entorno AWS](#-limpieza-del-entorno-aws)

---

# 📋 Prerrequisitos

Antes de comenzar, verifica que dispones de:

| Requisito | Versión |
|-----------|----------|
| Sistema Operativo | Linux (Ubuntu o Debian recomendado) |
| Python | 3.10 o superior |
| AWS CLI | Última versión estable |
| Git | Última versión estable |
| Cuenta AWS Academy Learner Lab | Activa |

---

## ☁️ Requisitos AWS

La instancia EC2 debe contar con un **IAM Role (LabRole)** con permisos para publicar métricas en CloudWatch.

> ⚠️ Sin este rol, las métricas no serán visibles en AWS.

---

## 🔐 Verificación de credenciales

```bash
aws sts get-caller-identity
```

---

# ⚙️ Configuración del Entorno

## 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Fco-Quiroga/ADY1103-Monitoreo-Observabilidad.git

cd ADY1103-Monitoreo-Observabilidad/08_Ev_Parcial_4-Auditoria_FinOps
```

---

## 2️⃣ Crear y activar entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4️⃣ Ejecutar el simulador

```bash
python3 app.py
```

---

# 🎮 Ejecución del Simulador

Al iniciar el script se mostrará un menú con los rubros disponibles:

- Banco
- Clínica
- Fintech
- E-commerce
- Contabilidad

Selecciona el número correspondiente para iniciar la simulación.

---

## ⏳ Ingesta de Datos Históricos (Máquina del Tiempo)

Este simulador no genera datos en tiempo real, sino que **inyecta historial financiero simulado**:

- Genera **13 días de costos históricos**
- Inyecta datos hora por hora
- Publica métricas en CloudWatch
- Muestra barra de progreso

> ⚠️ El proceso dura aproximadamente 1–2 minutos. Al finalizar verás:  
> `[✓] Carga completada`

## 📊 Visualización en AWS

Dirígete a:

```text
CloudWatch → Metrics → All Metrics
```

Namespace:

```text
FinOpsLab/Billing
```

> ℹ️ Los datos pueden tardar 2–5 minutos en aparecer.

---

# 💰 Diccionario de Métricas FinOps

## 📌 Métrica principal

### HourlyEstimatedCharge

Representa el costo estimado en USD por hora.

> Usa estadística **SUM** para análisis correcto.

---

## 📊 Dimensiones

### 🏢 Environment
- Production
- Development

### 🌎 Region
- us-east-1
- sa-east-1

### ⚙️ Service
- AmazonEC2
- AmazonRDS
- AmazonS3
- AmazonCloudWatch
- AmazonDynamoDB

---

# 🧹 Limpieza del Entorno AWS

> ⚠️ Importante: elimina los recursos al finalizar para evitar consumo de créditos.

## 1️⃣ Detener ejecución

```bash
CTRL + C
```

---

## 2️⃣ Terminar instancia EC2

- EC2 → Instance → Terminate

---

## 3️⃣ Finalizar Learner Lab

- AWS Academy → End Lab

---

> ✅ Con esto se asegura el cierre correcto del laboratorio.

---

# 📚 Conceptos Clave

| Concepto | Descripción |
|-----------|------------|
| FinOps | Gestión financiera en la nube |
| CloudWatch | Servicio de monitoreo AWS |
| Cost Allocation | Distribución de costos por dimensiones |
| Dashboard Financiero | Visualización de gasto cloud |
| Observabilidad Financiera | Visibilidad del comportamiento económico |
| Cost Optimization | Reducción de gasto cloud |

---

## 👨‍💻 Autor

**ADY1103 - Monitoreo y Observabilidad**

Evaluación Parcial 4 — Auditoría FinOps