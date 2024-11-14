```shell
# Генерация RSA приватного ключа
openssl genrsa -out jwt-private.pem 2048
```

```shell
# Генерация RSA публичного ключа
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```
