#!/usr/bin/env python
from igraph import *

def distance(p1, p2):
    return ((p1[0]-p2[0]) ** 2 + (p1[1]-p2[1]) ** 2) ** 0.5
    
g = Graph.Read_Pajek("net/1.net")
#g = Graph.Watts_Strogatz(5 , 2, 1, 0.6)
#Lattice([2,10], nei =1, directed =False, mutual =True, circular =True)

#g = Graph.Watts Strogatz([2,3])
#GRG(100, 0.2, return_coordinates=True)
#layout = Layout(zip(xs, ys))

#weights = [distance(layout[edge.source], layout[edge.target]) for edge in g.es]
#max_weight = max(weights)
#g.es["width"] = [6 - 5*weight/max_weight for weight in weights]
#mst = g.spanning_tree(weights)
#c=g.community_edge_betweenness(g, clusters=None, directed =True)

c=g.community_leading_eigenvector(clusters=None, return_merges=False)

print(c)

colors = ["lightgray", "cyan", "magenta", "yellow", "blue", "green", "red"]
for component in g.components():
  color = colors[min(6, len(component)-1)]
  for vidx in component: 
    g.vs[vidx]["color"] = color
  
plot(g, layout="fr", vertex_label=None)

#layout = g.layout("circle")
#plot(g, layout=layout)
#fig = Plot()
#fig.add(g)
#fig.add(mst, layout=layout, edge_color="red", vertex_label=None)
#fig.show()