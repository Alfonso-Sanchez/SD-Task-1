# Documentación: Práctica PYRO4 SingleNode

Esta documentación explica cómo configurar y ejecutar un proyecto basado en Pyro4 que consta de un servidor de insultos (`InsultServer`), un cliente que envía insultos (`Broadcaster`) y un conjunto de pruebas automatizadas (`TestInsultFilter`). El proyecto utiliza un entorno virtual de Python para gestionar dependencias y requiere que el servidor Pyro4 y el Name Server estén activos antes de ejecutar el cliente o las pruebas.

La fecha actual considerada para esta documentación es **31 de marzo de 2025**.

---

## 1. Configuración del Entorno Virtual en Python

### Paso 1: Crear el entorno virtual
Abre una terminal en el directorio raíz del proyecto y ejecuta:
```bash
python -m venv venv
```
Esto creará una carpeta `venv` con el entorno virtual.

### Paso 2: Activar el entorno virtual
Activa el entorno según tu sistema operativo:

- **Windows**:
```bash
venv\Scripts\activate
```
- **Linux/MacOS**:
```bash
source venv/bin/activate
```
Verás `(venv)` en la terminal si se activa correctamente.

### Paso 3: Instalar dependencias
Instala las dependencias listadas en `requirements.txt`:
```bash
pip install -r requirements.txt
```
Contenido de `requirements.txt`:
```
Pyro4==4.82
serpent==1.41
```

### Paso 4: Configurar el Name Server de Pyro4
El proyecto usa Pyro4 con un Name Server. Inicia el Name Server en una terminal separada (con el entorno activado):
```bash
python -m Pyro4.naming
```
Deja esta terminal abierta mientras trabajas con el proyecto.

### Paso 5: Desactivar el entorno (opcional)
Cuando termines, desactiva el entorno con:
```bash
deactivate
```

---

## 2. Ejecución del Código

El proyecto tiene dos componentes principales: el servidor (`InsultServer`) y el cliente (`Broadcaster`). Debes ejecutar el servidor primero y luego el cliente.

### 2.1. Ejecutar el Servidor (`InsultServer`)
El servidor gestiona insultos, filtra palabras ofensivas y muestra estadísticas en una interfaz curses.

#### Paso 1: Iniciar el servidor
En una terminal (con el entorno activado y el Name Server corriendo), ejecuta:
```bash
python insult_server.py
```
- `insult_server.py` es el nombre sugerido para el archivo del servidor.
- Verás una interfaz curses con estadísticas de insultos por segundo, cada 10 segundos y por minuto.
- Presiona `q` para salir del servidor.

#### Notas
- El servidor registra su nombre como `example.insultserver` en el Name Server de Pyro4.
- Mantén esta terminal abierta mientras ejecutas el cliente o las pruebas.

### 2.2. Ejecutar el Cliente (`Broadcaster`)
El cliente envía insultos aleatorios al servidor continuamente.

#### Paso 1: Iniciar el cliente
En otra terminal (con el entorno activado y el servidor corriendo), ejecuta:
```bash
python broadcaster.py
```
- `broadcaster.py` es el nombre sugerido para el archivo del cliente.
- Verás mensajes como `Insulto [texto] enviado con resultado: [resultado]` en la terminal.
- Usa `Ctrl+C` para detener el cliente y mostrar los insultos guardados en el servidor.

#### Notas
- El cliente se conecta al servidor mediante `PYRONAME:example.insultserver`.
- Si hay un error de conexión, verifica que el Name Server y el servidor estén activos.

---

## 3. Ejecución de las Pruebas

El archivo de pruebas (`TestInsultFilter`) verifica el comportamiento del servidor. Requiere que el servidor esté corriendo.

### Paso 1: Asegurarse de que el servidor esté activo
Ejecuta el servidor como se describe en la sección 2.1 antes de las pruebas.

### Paso 2: Ejecutar las pruebas
En una terminal (con el entorno activado), ejecuta:
```bash
python -m unittest test_insult_filter.py
```
- `test_insult_filter.py` es el nombre sugerido para el archivo de pruebas.
- Verás los resultados de las pruebas en la terminal (éxitos o fallos).

### Detalles de las pruebas
- **Prueba 1**: Verifica que una frase sin insultos se guarde correctamente.
- **Prueba 2**: Comprueba que los insultos se censuren como `CENSORED`.
- **Prueba 3**: Asegura que frases duplicadas no se guarden.
- **Prueba 4**: Confirma que múltiples frases se recuperen correctamente.

### Notas adicionales
- Las pruebas asumen que el servidor tiene un método `clearSentences()`. Si no funciona, reinicia el servidor manualmente antes de cada ejecución de pruebas.
- Si el servidor no está activo, las pruebas fallarán con un error de conexión.

---

## Notas Finales
- **Requisitos**: Python 3.8 o superior (compatible con Pyro4 4.82).
- **Estructura sugerida**:
  - `insult_server.py`: Código del servidor.
  - `broadcaster.py`: Código del cliente.
  - `test_insult_filter.py`: Código de las pruebas.
  - `requirements.txt`: Dependencias.
- **Flujo típico**:
  1. Inicia el Name Server (`python -m Pyro4.naming`).
  2. Inicia el servidor (`python insult_server.py`).
  3. Inicia el cliente (`python broadcaster.py`) o las pruebas (`python -m unittest test_insult_filter.py`).
- **Errores comunes**:
  - Name Server no iniciado: "Cannot connect to Pyro name server".
  - Servidor no activo: "Connection refused".