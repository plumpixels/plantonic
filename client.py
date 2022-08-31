from requests import post

res = post("localhost:5000/data", json={"test": "hi"})
print(res.content)
