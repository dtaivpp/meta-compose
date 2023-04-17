# Meta-Compose

Welcome to `meta-compose`! A utility for managing docker compose environments. Meta-compose allows you to string together docker compose files and provide arguments in a straightforward manner. 

### Format:

Meta-compose relies on a compose.json file to create named compose configs. For example, the below section defines two composer environments. One is named `observability` and the other is `opensearch`.

```json
{
  "observability": {}, 
  "opensearch": {}
}
```

Inside you can specify any number of the `docker compose` standard arguments. The argument should be specified in the key and the value should be either a value as a string or a list. 

```json
{
  "observaibility": {
    "file": [
      "opensearch/docker-compose.yml",
      "fluentd/docker-compose.yml"
    ], 
    "env-file": "opensearch/.env",
    "platform": "linux/amd64"
  }
}
```

The above config file would resolve to: 
```bash
docker compose --file opensearch/docker-compose.yml \
               --file fluentd/docker-compose.yml \ 
               --platform linux/amd64
```

Any commands you provide after the composer command and enironment simply get passed to docker compose. This allows you to in a more straghtforward manner control docker compose environments. 

```bash
meta-compose observaibility up -d
```

The above command would resolve to: 

```bash
docker compose --file opensearch/docker-compose.yml \
               --file fluentd/docker-compose.yml \ 
               --platform linux/amd64 \
               up -d
```

You may have noticed that the .env file specification isn't being passed through. That is becuase python-dotenv is ingesting the environment file and injecting it in on the fly.

### Publish notes for future me
```
git tag -a "v0.0.3-beta" -m "<Release Notes>"
git push --tags
```