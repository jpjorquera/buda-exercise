# Buda Spread Exercise

## Introducción

Esta implementación del ejercicio para el manejo de los spreads de los distintos mercados fue desarrollada usando Python 3.9 y FastAPI.

## Instalación y ejecución

Para instalar las dependencias se recomienda crear un ambiente virtual ejecutando:

```console
python -m venv buda-spread
source buda-spread/bin/activate
```

Luego, se deben instalar las dependencias:

```console
pip install -r requirements.txt
```

Así, se ejecuta el ambiente usando:

```console
uvicorn app.main:app --reload
```

## Pruebas

Para correr las pruebas simplemente se debe correr:

```console
pytest
```

También se puede ver la cobertura de pruebas ya sea por consola o con html ejecutando uno de los siguientes comandos:

```console
pytest --cov=app
pytest --cov=app --cov-report=html
```

## Ambiente Docker

También se puede correr el servidor en un ambiente dockerizado, para ello es necesario construir la imagen:

```console
docker build -t buda-spread .
```

Luego, se puede ejecutar corriendo:

```console
docker run -it -p 8000:8000 buda-spread
```

## Documentación de API

Al tener el servidor corriendo se puede navegar la documentación yendo a:

```
http://localhost:8000/docs
```

## Consideraciones

Para el desarrollo del ejercicio se tuvo algunas consideraciones:

- Al hacer la llamada para obtener el spread ya sea de uno o todos los mercados, se va a envíar `null` cuando el mercado sea válido, pero no haya información en el libro de órdenes suficiente para calcularlo.
- Para las alertas se consideró que estas debiesen guardarse de forma individual para cada mercado y se agregó la opción de enviar un parámetro a la llamada para indicar que se desea guardar la alerta. Esto fue hecho pensando en que los consumidores en el front puedan habilitar una opción para los usuarios a modo de que puedan indicar que desean guardar la alerta.
- Las alertas serán guardadas dentro de la carpeta `spread_alerts` para simular la persistencia. Aunque la estructura del repositorio mantiene desacoplada la implementación, en caso de que se desee agregar en el futuro la persistencia sólo debe mantener el contrato.
