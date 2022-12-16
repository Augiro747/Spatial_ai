echo "Input"
read B
printf "Coarsening="$B>.env
docker-compose up opendronemap-creator #-e Coarsening=$B
