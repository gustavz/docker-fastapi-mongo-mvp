if [ "$1" = "down" ]; then
    docker-compose down -v
fi

docker-compose build && docker-compose up -d
