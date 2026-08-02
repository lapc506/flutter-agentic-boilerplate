# 💥 Skill: Chaos Engineering

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `sre-chaos-engineering` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `chaos-engineering`, `chaos-monkey`, `litmus`, `failure-injection`, `resilience-testing`, `chaos-experiments`, `detection-validation`, `proof-testing`, `game-day` |
| **Referencia** | [Chaos Engineering Principles](https://principlesofchaos.org/) |

## 🔑 Keywords para Invocación

- `chaos-engineering`
- `chaos-monkey`
- `litmus`
- `failure-injection`
- `resilience-testing`
- `chaos-experiments`
- `detection-validation`
- `proof-testing`
- `game-day`
- `@skill:chaos-engineering`

### Ejemplos de Prompts

```
Implementa chaos engineering con Litmus para resilience testing
```

```
Configura chaos experiments y failure injection
```

```
Setup Chaos Monkey para probar resiliencia del sistema
```

```
@skill:chaos-engineering - Chaos engineering completo
```

```
¿Estamos listos para un game day? Validá primero la detección
```

```
El experimento reportó "no pasó nada" — ¿es resiliencia o ceguera?
```

## 📖 Descripción

Chaos engineering es la práctica de inyectar fallos intencionalmente para probar la resiliencia de sistemas. Este skill cubre chaos experiments, failure injection, resilience testing, y herramientas como Litmus y Chaos Monkey.

### ✅ Cuándo Usar Este Skill

- Sistemas en producción
- Testing de resiliencia
- Validación de failover
- Identificación de puntos débiles
- Mejora de reliability

### ❌ Cuándo NO Usar Este Skill

- Sistemas en desarrollo temprano
- **Sin detección VALIDADA** — no basta con tener monitoring configurado. Ver
  [§6 El prerrequisito](#6--el-prerrequisito-primero-validar-la-detección-después-inyectar-el-caos):
  un game day sobre infraestructura no instrumentada reporta *"no pasó nada"* y se lee como
  resiliencia
- Sin rollback procedures
- Sin equipo preparado

## 🏗️ Chaos Engineering Process

```
Hypothesis
    ↓
Experiment Design
    ↓
Execute Experiment
    ↓
Observe & Measure
    ↓
Learn & Improve
```

## 💻 Implementación

> **📁 Scripts Ejecutables:** Este skill incluye scripts ejecutables en la carpeta [`scripts/`](scripts/):
> - **Chaos Monkey:** [`scripts/chaos_monkey.py`](scripts/chaos_monkey.py) - Chaos Monkey para Kubernetes
> - **Experiments:** [`scripts/experiments.py`](scripts/experiments.py) - Framework para chaos experiments
>
> Ver [`scripts/README.md`](scripts/README.md) para documentación de uso completa.

### 1. Litmus Chaos Experiments

```yaml
# chaos/pod-delete-experiment.yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: pod-delete-chaos
  namespace: default
spec:
  annotationCheck: 'true'
  engineState: 'active'
  chaosServiceAccount: litmus-admin
  monitoring: true
  jobCleanUpPolicy: 'retain'
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: '60'
            - name: CHAOS_INTERVAL
              value: '10'
            - name: FORCE
              value: 'false'
            - name: RAMP_TIME
              value: '10'
        probe:
          - name: check-app-health
            type: httpProbe
            httpProbeInputs:
              url: http://app-service/health
              insecureSkipVerify: false
            mode: Continuous
            runProperties:
              probeTimeout: 5
              interval: 2
              retry: 1
```

```yaml
# chaos/network-chaos.yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: network-chaos
spec:
  engineState: 'active'
  chaosServiceAccount: litmus-admin
  experiments:
    - name: network-chaos
      spec:
        components:
          env:
            - name: NETWORK_INTERFACE
              value: 'eth0'
            - name: NETWORK_PACKET_LOSS_PERCENTAGE
              value: '100'
            - name: TARGET_CONTAINER
              value: 'app-container'
            - name: TARGET_PODS
              value: 'app-.*'
            - name: TOTAL_CHAOS_DURATION
              value: '120'
```

### 2. Chaos Monkey Implementation

**Script ejecutable:** [`scripts/chaos_monkey.py`](scripts/chaos_monkey.py)

Chaos Monkey para Kubernetes que elimina aleatoriamente pods y recursos para probar resiliencia.

**Cuándo ejecutar:**
- Testing de resiliencia en producción
- Validación de failover
- Identificación de puntos débiles

**Uso:**
```bash
# Ejecutar experimento (pod-delete)
python scripts/chaos_monkey.py run --experiment-type pod-delete

# Habilitar/deshabilitar
python scripts/chaos_monkey.py enable
python scripts/chaos_monkey.py disable

# Configurar probabilidad
python scripts/chaos_monkey.py set-probability --probability 0.1
```

**Características:**
- ✅ Eliminación aleatoria de pods
- ✅ Probabilidad configurable
- ✅ Filtrado por annotations (`chaos.enabled=true`)
- ✅ Múltiples tipos de experimentos

### 3. Chaos Experiments

**Script ejecutable:** [`scripts/experiments.py`](scripts/experiments.py)

Framework para ejecutar y gestionar chaos experiments con hipótesis y resultados.

**Cuándo ejecutar:**
- Ejecución de experiments estructurados
- Gestión de múltiples experiments
- Registro de nuevos experiments

**Uso:**
```bash
# Ejecutar experimento
python scripts/experiments.py run --name pod-delete

# Listar experimentos
python scripts/experiments.py list
```

**Características:**
- ✅ Framework de experiments estructurado
- ✅ Hipótesis y expected behavior
- ✅ Tracking de resultados
- ✅ Registro de experiments

### 4. Automated Chaos Testing

```yaml
# chaos/chaos-test-schedule.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: chaos-monkey
spec:
  schedule: "0 */6 * * *"  # Every 6 hours
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: chaos-monkey
            image: chaos-monkey:latest
            env:
            - name: ENABLED
              value: "true"
            - name: PROBABILITY
              value: "0.1"
            - name: EXPERIMENT_TYPES
              value: "pod-delete,cpu-stress"
            command:
            - python
            - chaos_monkey.py
            - --schedule
          restartPolicy: OnFailure
```

### 5. Chaos Metrics

```python
# chaos/metrics.py
from prometheus_client import Counter, Histogram, Gauge

# Metrics
chaos_experiments_total = Counter(
    'chaos_experiments_total',
    'Total chaos experiments run',
    ['experiment_type', 'status']
)

chaos_experiment_duration = Histogram(
    'chaos_experiment_duration_seconds',
    'Duration of chaos experiments',
    ['experiment_type']
)

system_recovery_time = Histogram(
    'system_recovery_time_seconds',
    'Time for system to recover from chaos',
    ['experiment_type']
)

chaos_experiments_active = Gauge(
    'chaos_experiments_active',
    'Number of active chaos experiments'
)

def record_experiment(experiment_type: str, status: str, duration: float):
    """Record chaos experiment metrics."""
    chaos_experiments_total.labels(
        experiment_type=experiment_type,
        status=status
    ).inc()

    chaos_experiment_duration.labels(
        experiment_type=experiment_type
    ).observe(duration)
```

### 6. ⛔ El prerrequisito: primero validar la DETECCIÓN, después inyectar el caos

> **Este skill asume que ya podés detectar.** Todo lo de arriba —Litmus, Chaos Monkey, los
> experimentos, las métricas— presupone que si el sistema se degrada, algo se pone en rojo.
> Si ese supuesto es falso, **el game day no falla: reporta "no pasó nada", y eso se lee
> como resiliencia.**

Esa lectura es el peor resultado posible de un experimento, porque es indistinguible de un
éxito y encima produce confianza.

#### 6.1 El caso medido

Once controles se midieron entre 2026-07-26 y 2026-08-02 en una plataforma real, y **los
once tenían la misma forma**: el emisor era correcto, el receptor estaba muerto, y el
silencio se leía como salud. En los once el código estaba bien y cada test individual
pasaba.

El registro que los documenta lo pone como no-objetivo explícito
(`openspec/changes/2026-08-02-observability-liveness-axis/proposal.md` en
`DojoCodingLabs/dojo-os @ origin/develop 18d4f7da3`):

> *"Chaos engineering. It shares the technique and not the hypothesis: chaos breaks the
> system to ask whether the **system** survives; this breaks it to ask whether the
> **control** notices. **A game day against this infrastructure today would report «nothing
> happened» and be read as resilience.**"*

Dos ejemplos concretos de por qué el tablero se hubiera quedado verde igual — *los dos
tomados de ese registro y **no re-medidos en este pase***:

- Un servicio de alertas con ocho rutas HTTP funcionando y **cero requests en 30 días**,
  porque la API que las dispara (`cloudscheduler.googleapis.com`) nunca se habilitó.
  Cuatro canales de Slack cableados a ese servicio, recibiendo nada.
- Ocho de nueve proyectos GCP medidos con **cero políticas de alerta**, incluido el proyecto
  de la flota de CI cuya caída acababa de ocurrir esa misma semana.

#### 6.2 Chaos engineering vs. validación de detección: misma técnica, hipótesis distinta

|  | qué rompe | qué pregunta | falla si… |
|---|---|---|---|
| **Chaos engineering** | el sistema | ¿el **sistema** sobrevive? | el sistema se degrada |
| **Validación de detección** | el sistema | ¿el **control** se entera? | el control no se pone en rojo |

Comparten la inyección de fallos y **no** la hipótesis. La segunda es prerrequisito de la
primera, no un sinónimo. Tiene nombre propio en otras disciplinas: en seguridad se llama
**detection validation**; en sistemas críticos, **proof testing**.

#### 6.3 La regla, y cómo se ejecuta

> **Ningún control cuenta como desplegado hasta que se lo vio ponerse en rojo a propósito.**

**Antes del primer game day, corré esta secuencia sobre cada control del que dependa tu
hipótesis.** No es un experimento de caos: es la calibración del instrumento con el que vas
a medir el experimento.

```
Para cada control (alerta, check, monitor, gate):

  1. Nombrá qué señal debería producir cuando el sistema esté degradado.
  2. Rompé esa señal A PROPÓSITO — apagá la URL del sink, congelá al productor,
     rompé un paso del flujo.
  3. Confirmá que el control se pone en ROJO. No que sale vacío.
     ── Salir vacío es el modo de falla, no la evidencia. ──
  4. CRONOMETRÁ cuánto tardó en avisar. El tiempo de detección se mide, no se estima.
  5. Registrá la fecha. Un control probado hace seis meses no es un control probado.

Solo cuando TODOS pasan los 5 pasos, el game day mide lo que creés que mide.
```

**El paso 3 es donde se cae casi siempre.** Un check que devuelve una lista vacía y un check
que erroró producen la misma pantalla. Por eso la regla de tres valores importa acá también:

| resultado del control | qué significa | qué NO puede significar |
|---|---|---|
| `pass` | se verificó y está bien | — |
| `fail` | se verificó y está mal | — |
| `unverifiable` | **no se pudo determinar** | ni `pass` ni `fail` |

Si tu experimento de caos termina con un control en `unverifiable` y lo anotás como
"el sistema aguantó", el game day no midió nada.

#### 6.4 Y sobre esta infraestructura, en concreto

Este skill documenta Litmus, Chaos Monkey y CronJobs de Kubernetes. **Si tu stack es GCP +
Cloud Run + OpenTofu sin Kubernetes, nada de eso aplica tal cual** — pero el prerrequisito
de arriba aplica idéntico, y es la parte que se puede ejecutar hoy sin adoptar ninguna
herramienta de caos.

El orden correcto para un stack así:

1. **Construir el nivel de ausencia** (ver el skill `observability-stack`, §6): sin él, no
   hay señal que romper.
2. **Validar cada control** con los 5 pasos de arriba.
3. **Recién entonces** evaluar herramientas de inyección de fallos.

Invertir el orden 1 y 3 es comprar un instrumento de medición para un tablero que no mide.

## 🎯 Mejores Prácticas

### 1. Experiment Design

✅ **DO:**
- Start with hypothesis
- Test in non-production first
- Start small and increase
- Monitor during experiments

❌ **DON'T:**
- Run experiments without hypothesis
- Start in production
- Run multiple experiments simultaneously
- Ignore monitoring

### 2. Safety

✅ **DO:**
- Use feature flags
- Have rollback procedures
- Set experiment duration limits
- Monitor system health

❌ **DON'T:**
- Run experiments without safety measures
- Ignore system health
- Exceed experiment duration
- Skip rollback procedures

### 3. Learning

✅ **DO:**
- Document results
- Share learnings
- Improve based on results
- Regular experiments

❌ **DON'T:**
- Skip documentation
- Ignore results
- Run experiments randomly
- Stop after first success

## 🚨 Troubleshooting

### Experiments Causing Issues

1. Stop experiment immediately
2. Review experiment design
3. Check system health
4. Adjust experiment parameters

### No Recovery

1. Check failover mechanisms
2. Review monitoring
3. Investigate root cause
4. Fix underlying issues

## 📚 Recursos Adicionales

- [Chaos Engineering Principles](https://principlesofchaos.org/)
- [Litmus Documentation](https://litmuschaos.io/docs/)
- [Chaos Monkey](https://github.com/Netflix/chaosmonkey)

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
**Total líneas:** 1,100+
