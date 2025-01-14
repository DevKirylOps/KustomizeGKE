FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    ca-certificates \
    apt-transport-https \
    software-properties-common && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/

RUN curl -fsSL https://pgp.mongodb.com/server-6.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/mongodb-archive-keyring.gpg] https://repo.mongodb.com/apt/debian buster/mongodb-enterprise/6.0 main" | tee /etc/apt/sources.list.d/mongodb-enterprise.list && \
    apt-get update && apt-get install -y mongodb-mongosh && \
    rm -rf /var/lib/apt/lists/*

COPY update-mongo-password.sh /usr/local/bin/update-mongo-password.sh
RUN chmod +x /usr/local/bin/update-mongo-password.sh

WORKDIR /workspace

CMD ["/usr/local/bin/update-mongo-password.sh"]
