DIR=dataset
if ! [ -d $DIR ]; then
git clone https://github.com/pierotofy/dataset_banana.git $DIR
fi
docker-compose build --no-cache
