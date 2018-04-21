run:
	# :z suffix is needed to work with selinux
	# https://stackoverflow.com/questions/24288616/permission-denied-on-accessing-host-directory-in-docker
	docker run --rm -it \
		-v ~/src:/workspace:z \
		-v pants-centos7-cache:/root/.cache \
		-v pants-centos7-ivy:/root/.m2 \
		-v pants-centos7-maven:/root/.ivy \
		pants-centos7 bash

volume:
	docker volume create --name pants-centos7-cache
	docker volume create --name pants-centos7-ivy
	docker volume create --name pants-centos7-maven

build:
	docker build --tag pants-centos7 .

