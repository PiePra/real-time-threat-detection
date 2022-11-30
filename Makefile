download:
	wget -O data.tar "https://kilthub.cmu.edu/ndownloader/files/24857825"
	tar -xf data.tar

db:
	docker run --name postgres -d -p 5432:5432 -e POSTGRES_USER=digger -e POSTGRES_PASSWORD=digger -e POSTGRES_DB=digger postgres	
	python database/filldata.py

make data:
	make download
	make db

clean:
	docker stop postgres && docker rm postgres


