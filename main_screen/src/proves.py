import requests

resposta = requests.get("https://jsonplaceholder.typicode.com/todos/3")
dades = resposta.json()
print(dades)