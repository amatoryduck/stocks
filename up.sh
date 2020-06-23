docker build -t stocks .
docker run --name stocks -itd stocks bash
docker exec -it stocks bash