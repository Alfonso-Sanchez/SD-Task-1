import redis
import json

nodes = [
    {
        "conn": redis.Redis(host='localhost', port=6379, db=0),
        "request_queue": "requests_node1",
        "response_queue": "client_filter_queue_node1"
    },
    {
        "conn": redis.Redis(host='localhost', port=6380, db=0),
        "request_queue": "requests_node2",
        "response_queue": "client_filter_queue_node2"
    },
    {
        "conn": redis.Redis(host='localhost', port=6381, db=0),
        "request_queue": "requests_node3",
        "response_queue": "client_filter_queue_node3"
    }
]

frases = [
    "Alfonso eres idiota",
    "Neus eres una zorra",
    "Clara eres una boba"
]

print("🔴 Cliente Filter: solicitando filtrados...")

try:
    i = 0
    while True:
        node_index = i % len(nodes)
        node_info = nodes[node_index]
        rconn = node_info["conn"]

        frase = frases[i % len(frases)]
        request_data = {
            "type": "filter",
            "phrase": frase,
            "response_queue": node_info["response_queue"]
        }
        request_json = json.dumps(request_data)

        rconn.rpush(node_info["request_queue"], request_json)
        print(f"📤 Frase para filtrar (Nodo {node_index+1}): {frase}")

        data = rconn.blpop(node_info["response_queue"], timeout=5)
        if data:
            filtrada = data[1].decode("utf-8")
            print(f"📥 Nodo {node_index+1} responde: {filtrada}")
        else:
            print(f"⚠️ Sin respuesta de Nodo {node_index+1} en 5s.")

        i += 1

except KeyboardInterrupt:
    print("\n🔴 Cliente Filter interrumpido.")