#!/bin/bash

# Servidores
python3 server_cluster.py & 
python3 server_cluster.py & 
python3 server_cluster.py &

# Broadcaster
python3 broadcaster.py &

# Clientes
python3 client_insult.py & 
python3 client_insult.py & 
python3 client_insult.py & 
python3 client_insult.py & 
python3 client_insult.py &

# Cliente filtro
python3 client_filter.py &

# 🟢 Mostrar monitor en primer plano
python3 monitor.py