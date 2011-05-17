library(igraph)
library(Cairo)

rm(list=ls(all=TRUE))

# postscript(file="plot.eps", onefile=FALSE, fonts=c("serif", "Palatino"), horizontal=FALSE)

setwd("~/Desktop/wsanalysis/net")
# memberships <- list()

G <- read.graph("infx.net", format="pajek")
# is.simple(gs)
G <- simplify(G)
# # 
# # G <- minimum.spanning.tree(G)
# betweenness(G)
# 

# d <- degree(G, mode="in")
# power.law.fit(d+1, 20)

# d <- degree(g, mode="in")
# power.law.fit(d+1, 20)
# 
lout <- layout.fruchterman.reingold(G)
# 
# 
# plot(G, layout=lout1, vertex.size=10)

# plot(G, layout=lout)

### leading.eigenvector.community
lec <- leading.eigenvector.community(G)
memberships <- lec$membership

## color
comps <- memberships
colbar <- rainbow(max(comps)+1)
V(G)$color <- colbar[comps+1]
plot(G, layout=lout, vertex.size=10)
title(main="eigenvector")
modularity(G, comps)

# dend <- as.dendrogram(lec, use.modularity=TRUE)
# plot(dend, nodePar=list(pch=c(20, 20)))
# title(main="eigenvector")