## Features
Provides a free IP proxy pool service. After startup, available IPs can be obtained via an API interface implemented with Flask.

Provides a Dockerfile for one-click deployment.

## Get Random IP
http://127.0.0.1:5555/random

## Get Max IP
http://127.0.0.1:5555/max

## Delete a Specific IP
http://127.0.0.1:5555/useless

## Deployment
`pip intall -r requirements.txt -i http://pypi.doubanio.com/simple`

Redis is optional; if not used, IPs will be loaded directly into memory.
