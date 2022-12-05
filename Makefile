download:
	wget -O data.tar "https://kilthub.cmu.edu/ndownloader/files/24857825"
	tar -xf data.tar

redis:
	docker run -d --name redis -e ALLOW_EMPTY_PASSWORD=yes -p 6379:6379 bitnami/redis:latest

make data:
	make download
	make redis

clean:
	docker stop redis && docker rm redis


