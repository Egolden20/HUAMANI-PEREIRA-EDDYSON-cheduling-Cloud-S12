# Simulador de Scheduling Cloud — Semana 12

**Curso:** Servicios Cloud · **Universidad:** Universidad Tecnológica del Perú (UTP)  
**Estudiante:** Eddyson Cesar Huamani Pereira

## Descripción

Proyecto académico de simulación local de planificación (scheduling) de tareas sobre máquinas virtuales lógicas. Se comparan algoritmos y se generan tablas y gráficas para analizar makespan, espera media y utilización de recursos. **No aprovisiona máquinas virtuales reales ni consume servicios de AWS, Azure o Google Cloud.**

## Experimentos

- **Laboratorio (A):** 50 tareas sintéticas con semilla fija y 5 VM heterogéneas (1000, 1500, 2000, 2500 y 3000 MIPS), comparando FCFS y Min-Min.
- **Evaluación (B):** 8 trabajos con 3 VM homogéneas, aplicando reparto circular Round Robin, SJF con selección de VM menos cargada y una asignación optimizada.

## Ejecución en Windows (PowerShell)

1. Instalar Python 3.
2. Clonar o descargar este repositorio y abrir su carpeta.
3. Instalar las dependencias:

```powershell
py -m pip install -r requirements.txt
```

4. Ejecutar:

```powershell
py simulador_scheduling.py
```

En Linux/macOS se puede utilizar `python3` en lugar de `py`.

## Archivos que genera automáticamente

- `resultados.json` — indicadores y configuración.
- `dataset_50_tareas.csv` — dataset sintético reproducible.
- `laboratorio_fcfs.csv` y `laboratorio_minmin.csv` — asignaciones del experimento A.
- `evaluacion_rr.csv`, `evaluacion_sjf.csv` y `evaluacion_optimizado.csv` — asignaciones del experimento B.
- `comparacion_laboratorio.png`, `cargas_laboratorio.png` y `comparacion_evaluacion.png` — gráficas.

## Resultados de referencia

| Escenario | Estrategia | Makespan |
|---|---|---:|
| 50 tareas / 5 VM | FCFS | 135,142 segundos |
| 50 tareas / 5 VM | Min-Min | 120,403 segundos |
| 8 trabajos / 3 VM | Round Robin | 21 minutos |
| 8 trabajos / 3 VM | SJF + VM con menor carga | 22 minutos |
| 8 trabajos / 3 VM | Asignación optimizada | 18 minutos |

Los resultados corresponden a una simulación determinista, no a mediciones en infraestructura cloud real. Las figuras PNG se generan cuando se ejecuta el script; las capturas personales de VS Code y terminal deben obtenerse en el equipo del estudiante.

## Arquitectura lógica

Dataset de trabajos → Scheduler → Colas y calendarios por VM → 3 o 5 VM simuladas → Métricas y archivos de resultados.

## Referencias del ejercicio

Guía de Laboratorio de Planificación (Scheduling) en Cloud Computing y Guía de Evaluación Práctica Individual del curso Servicios Cloud, Semana 12.
