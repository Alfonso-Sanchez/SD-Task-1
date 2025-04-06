import redis
import json

nodes = [
    {
        "conn": redis.Redis(host='localhost', port=6379, db=0),
        "request_queue": "requests_node1",
        "response_queue": "client_insult_queue_node1"
    },
    {
        "conn": redis.Redis(host='localhost', port=6380, db=0),
        "request_queue": "requests_node2",
        "response_queue": "client_insult_queue_node2"
    },
    {
        "conn": redis.Redis(host='localhost', port=6381, db=0),
        "request_queue": "requests_node3",
        "response_queue": "client_insult_queue_node3"
    }
]

print("🔴 Cliente Redis: solicitando insultos...")

try:
    i = 0
    while True:
        node_index = i % len(nodes)
        node_info = nodes[node_index]
        rconn = node_info["conn"]

        # Construir la solicitud
        request_data = {
            "type": "insult",
            "response_queue": node_info["response_queue"]
        }
        request_json = json.dumps(request_data)

        # Enviar a la cola del nodo
        rconn.rpush(node_info["request_queue"], request_json)
        print(f"📤 Petición 'insult' al Nodo {node_index+1}")

        # Esperar la respuesta en nuestra cola
        data = rconn.blpop(node_info["response_queue"], timeout=5)
        if data:
            insulto = data[1].decode("utf-8")
            print(f"📜 Nodo {node_index+1} responde: {insulto}")
        else:
            print(f"⚠️ Sin respuesta del Nodo {node_index+1} en 5s.")

        i += 1

except KeyboardInterrupt:
    print("\n🔴 Cliente Redis interrumpido.")