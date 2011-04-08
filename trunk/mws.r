library(igraph)
library(Cairo)

rm(list=ls(all=TRUE))

setwd("~/Desktop/wsanalysis/")
# memberships <- list()

G <- read.graph("mws.paj", format="pajek")
# is.simple(gs)
G <- simplify(G)
# 
# G <- minimum.spanning.tree(G)

# par(mfrow=c(3,2))

degree(G)
diameter(G)

lout <- layout.fruchterman.reingold(G)

plot(G, layout=lout)

# ### leading.eigenvector.community
# lec <- leading.eigenvector.community(G)
# memberships <- lec$membership
# 
# ## color
# comps <- memberships
# colbar <- rainbow(max(comps)+1)
# V(G)$color <- colbar[comps+1]
# plot(G, layout=lout, vertex.size=10)
# title(main="eigenvector")
# modularity(G, comps)