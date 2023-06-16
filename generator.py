from resource import *
import random

def writeGraph(n, m, edges, f):
	f.write(str(n)+" "+str(n)+" "+str(m)+"\n")
	for v in range(n + 1):
		for u in edges[v]:
			f.write(str(v)+" "+str(u)+"\n")

file = open("graph.txt", "w")
n = int(input("Digite numero de vértices:\n"))
den = int(input("Digite densidade:\n"))

m = 0
edges: list[list[int]] = [[] for i in range(n + 1)]

for v in range(n + 1):
	for u in range(1, n + 1):
		if(random.randint(1, 100) < den):
			m = m+1
			edges[v].append(u)
   
writeGraph(n,m,edges,file)

file.close()