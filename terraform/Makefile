.PHONY: setup build-image

# prerequisite for terraform
setup:
	gcloud auth login
	gcloud config set project la-famiglia-parma-ai
	gcloud auth configure-docker europe-west1-docker.pkg.dev

build-image:
	docker build -t europe-west1-docker.pkg.dev/la-famiglia-parma-ai/parma-registry/parma-analytics:staging-$(git rev-parse --short HEAD) ./..
	docker push europe-west1-docker.pkg.dev/la-famiglia-parma-ai/parma-registry/parma-analytics:staging-$(git rev-parse --short HEAD)
