# nsjail-docker-example


## Test google cloud
```bash
curl -X POST https://python-nsjail-api-896690362254.europe-west1.run.app/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    print(\"running\")\n    return {\"message\": \"hello from jail\"}"}'
```

## Run locally

```bash
docker build -t python-nsjail-api . && docker run --rm -p 8080:8080 --cap-add=SYS_ADMIN --cap-add=SYS_CHROOT python-nsjail-api
```
