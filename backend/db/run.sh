
sudo docker run --name postgres-db -p 5432:5432 -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=fintech_project -d postgres:15