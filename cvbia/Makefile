docker/cvbia/login:
	az acr login -n cvbia

apps/cvbia_streamlit/build:
	docker build -f Dockerfile.streamlit -t cvbia:latest .

apps/cvbia_streamlit/push:
	docker tag cvbia:latest cvbia.azurecr.io/cvbia:latest
	docker push cvbia.azurecr.io/cvbia:latest

apps/cvbia_streamlit/run:
	docker run -p 80:80 cvbia:latest

apps/cvbia_fastapi/build:
	docker build -f Dockerfile.fastapi -t cvbia_fastapi:latest .

apps/cvbia_fastapi/push:
	docker tag cvbia_fastapi:latest cvbia.azurecr.io/cvbia_fastapi:latest
	docker push cvbia.azurecr.io/cvbia_fastapi:latest

apps/cvbia_fastapi/run:
	docker run -p 80:80 cvbia_fastapi:latest
