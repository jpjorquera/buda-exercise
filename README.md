# Buda Spread Exercise

```console
uvicorn app.main:app --reload
```

```console
pytest
pytest --cov=app
```

```console
python -m venv buda-spread
source buda-spread/bin/activate
pip install -r requirements.txt
```

```console
docker build -t buda-spread .
docker run -it -p 8000:8000 buda-spread
```
