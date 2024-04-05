from pyodm import Node
import time
n = Node.from_url("http://localhost:39387")

print(n.info())
