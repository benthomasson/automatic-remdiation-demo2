
.PHONY: all build


all: build

build:
	docker build -f Dockerfile -t quay.io/bthomass/automatic-remediation2:latest .

run:
	docker run -it quay.io/bthomass/automatic-remediation2:latest ansible-events --rules process_down2.yml -i inventory3.yml

shell:
	docker run -it  quay.io/bthomass/automatic-remediation2:latest /bin/bash

push:
	docker push quay.io/bthomass/automatic-remediation2:latest
