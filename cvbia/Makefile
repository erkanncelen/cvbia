docker/cvbia/login:
	az acr login -n cvbia

apps/cvbia_streamlit/build:
	docker build -f Dockerfile.streamlit -t cvbia:latest .

apps/cvbia_streamlit/push:
	docker tag cvbia:latest cvbia.azurecr.io/cvbia:latest
	docker push cvbia.azurecr.io/cvbia:latest

apps/cvbia_streamlit/run:
	docker run -p 80:80 cvbia:latest

apps/cvbia_slackbot/build:
	docker build -f Dockerfile.slackbot -t cvbia_slackbot:latest .

apps/cvbia_slackbot/push:
	docker tag cvbia_slackbot:latest cvbia.azurecr.io/cvbia_slackbot:latest
	docker push cvbia.azurecr.io/cvbia_slackbot:latest

apps/cvbia_slackbot/run:
	docker run -p 80:80 cvbia_slackbot:latest
