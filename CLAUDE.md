# CLAUDE.md - AI Assistant Guide

## Repository Overview

**Repository Name:** `wsanalysis` (Wireless/Social Network Analysis)

**Purpose:** Network analysis toolkit for studying graph structures, social networks, and wireless network topologies. The project focuses on:
- Community detection and clustering
- Network topology analysis
- Path finding algorithms
- Graph visualization
- Statistical analysis of network properties

**Primary Languages:**
- **Python** (graph analysis using igraph library)
- **R** (statistical analysis and visualization)
- **AWK** (data preprocessing and format conversion)

**Domain:** Network Science, Graph Theory, Social Network Analysis

---

## 📁 Repository Structure

```
wsanalysis/
├── py/                     # Python scripts (igraph-based analysis)
│   ├── socialn.py         # Convert igraph to SONIA visualization format
│   ├── kautz.py           # Kautz graph generation and visualization
│   ├── mst.py             # Community detection (betweenness, eigenvector)
│   └── findpath.py        # Path finding algorithms (recursive DFS)
│
├── R/                      # R statistical analysis scripts
│   ├── comm.r             # Community detection (multiple algorithms)
│   ├── camx.r             # CAM network specific analysis
│   ├── clusterall.r       # Hierarchical clustering
│   ├── cdfine*.r          # Community detection fine-tuning
│   └── [20+ other R scripts]
│
├── net/                    # Network data files (Pajek format)
│   ├── ws*.net            # Wireless network topologies (various timescales)
│   ├── camx.net           # CAM network data
│   └── pajek.net          # Pajek format files
│
├── trace/                  # Network trace data
│   ├── camx.trc           # CAM network trace (1.3MB)
│   └── mesh*.trc          # Mesh network traces
│
├── *.awk                   # AWK data processing scripts
├── *.dat                   # Raw data files
├── *.pdf                   # Generated visualizations
└── *.son                   # SONIA visualization files
```

---

## 🔑 Key Concepts & Terminology

### Network Analysis Terms
| Term | Definition | Usage in Code |
|------|------------|---------------|
| **Vertex/Node** | A point in the network | `g.vs`, `V(G)` |
| **Edge/Arc** | Connection between vertices | `g.es`, `E(G)` |
| **Degree** | Number of connections a vertex has | `degree(G)` |
| **Betweenness** | Measure of centrality | `betweenness(G)` |
| **Closeness** | Inverse of average distance to all nodes | `closeness(G)` |
| **Community** | Densely connected subgraph | `community_*` functions |
| **Modularity** | Quality metric for community partitions | `modularity(G, membership)` |
| **MST** | Minimum Spanning Tree | `minimum.spanning.tree(G)` |

### Data Formats
- **Pajek (.net/.paj)**: Standard network file format
- **SONIA (.son)**: Dynamic network visualization format
- **Trace (.trc)**: Network activity logs
- **DAT (.dat)**: Raw tabular data (space/tab separated)

---

## 🐍 Python Code Conventions

### Core Library: igraph
All Python scripts use the `igraph` library for graph analysis.

**Common Patterns:**

```python
from igraph import *

# Reading network files
g = Graph.Read_Pajek("path/to/file.net")

# Graph operations
g = simplify(g)  # Remove self-loops and multiple edges
mst = minimum.spanning.tree(g)  # Get MST

# Community detection
communities = community_edge_betweenness(g)
communities = leading_eigenvector_community(g)

# Visualization
plot(g, layout="fr", vertex_size=10)  # Fruchterman-Reingold layout
```

### File Path Conventions
- **Python scripts**: Use relative paths or absolute paths with `/home/amc/Desktop/wsanalysis/`
- **R scripts**: Use `setwd("~/Desktop/wsanalysis/")` or `setwd("~/Desktop/wsanalysis/net")`

### Key Python Scripts

#### 1. `socialn.py` - SONIA Conversion
**Purpose:** Convert igraph objects to SONIA dynamic visualization format

**Key Function:**
```python
def igraph2sonia(graph, soniaFile):
```

**Requirements:**
- All vertices must have a `time` attribute
- Optional attributes: `color`, `size`, `width`
- Time can be scalar (start time) or tuple (start, end)

**Output Format:** Tab-separated file with node and edge sections

---

#### 2. `kautz.py` - Kautz Graph Visualization
**Purpose:** Create and visualize Kautz graphs (specialized network topology)

**Parameters:**
- `m`: Degree parameter (alphabet size)
- `n`: Diameter parameter

**Usage:** Used for studying efficient network topologies

---

#### 3. `mst.py` - Community Detection
**Purpose:** Identify communities using multiple algorithms

**Algorithms Implemented:**
1. **Edge Betweenness:** Iteratively removes high-betweenness edges
2. **Leading Eigenvector:** Uses spectral properties

**Output:** Colored visualization showing community membership

---

#### 4. `findpath.py` - Path Finding
**Purpose:** Find all paths between two vertices

**Algorithm:** Recursive depth-first search with cycle detection

**Key Function:**
```python
def adjlist_find_paths(a, n, m, path=[]):
    # Returns list of all paths from node n to node m
```

---

## 📊 R Code Conventions

### Core Library: igraph (R version)
R scripts also use igraph, but with R syntax.

**Common Patterns:**

```r
library(igraph)
library(Cairo)  # For high-quality graphics

# Reading networks
G <- read.graph("file.net", format="pajek")
G <- simplify(G)

# Community detection
lec <- leading.eigenvector.community(G)
wt <- walktrap.community(G, modularity=TRUE)
sc <- spinglass.community(G, spins=10)

# Visualization
plot(G, layout=layout.fruchterman.reingold, vertex.size=10)
colbar <- rainbow(max(membership)+1)
V(G)$color <- colbar[membership+1]
```

### Key R Scripts

#### 1. `comm.r` - Comprehensive Community Detection
**Purpose:** Compare multiple community detection algorithms

**Algorithms:**
- `clique.community()` - K-clique based
- `largeScaleCommunity()` - Label propagation variant
- `walktrap.community()` - Random walk based
- `leading.eigenvector.community()` - Spectral method
- `spinglass.community()` - Statistical physics approach

**Output:** Dendrogram and colored network plot

---

#### 2. `camx.r` - CAM Network Analysis
**Purpose:** Analyze specific CAM (Cambridge) network dataset

**Features:**
- Multiple community detection methods
- Comparative visualization (2x2 plots)
- K-Clique, Fiedler, and H-cluster methods

---

#### 3. `clusterall.r` - Hierarchical Clustering
**Purpose:** Perform hierarchical clustering on adjacency matrices

**Methods:**
- `hclust()` with different linkage methods (average, ward, single)
- Distance matrix computation from adjacency
- Closeness centrality analysis

**Visualization:** Dendrograms and network plots with clusters

---

#### 4. `cdfine2.r` - Community Detection Fine-tuning
**Purpose:** Compare different community detection algorithms on wireless networks

**Algorithms Tested:**
- Leading eigenvector
- Spinglass (with 10 spins)
- Edge betweenness

**Layout:** Uses `layout.circle` for clear visualization

---

## 🔧 AWK Scripts

### Data Processing Pipeline

AWK scripts handle data preprocessing and format conversion.

#### 1. `12.awk` - Simple Network Converter
**Purpose:** Extract edge list from raw data

**Input:** Multi-column data (node1, node2, time1, time2, ...)
**Output:** Pajek format (vertices declaration + edge list)

```awk
BEGIN { print "*vertices 100"; print "*edges" }
{ print $1, $2 }  # Extract first two columns
```

---

#### 2. `count.awk` - Edge Frequency Counter
**Purpose:** Identify frequently occurring edges

**Algorithm:**
1. Count occurrences of each (i,j) pair
2. Filter edges with count > 100
3. Output: node1, node2, count

**Use Case:** Finding persistent connections in temporal networks

---

## 🎯 Common Workflows

### Workflow 1: Analyzing a New Network

```bash
# Step 1: Preprocess raw data with AWK
./12.awk < raw_data.dat > net/new_network.net

# Step 2: Analyze with R
cd R/
# Edit script to load "new_network.net"
Rscript comm.r

# Step 3: Advanced analysis with Python
cd ../py/
# Edit script to load network
python mst.py
```

### Workflow 2: Community Detection Pipeline

```r
# In R
library(igraph)
G <- read.graph("network.net", format="pajek")
G <- simplify(G)

# Try multiple algorithms
wt <- walktrap.community(G)
lec <- leading.eigenvector.community(G)
eb <- edge.betweenness.community(G)

# Compare modularity scores
modularity(G, wt$membership)
modularity(G, lec$membership)
modularity(G, eb$membership)

# Visualize best result
plot(G, vertex.color=best_membership)
```

### Workflow 3: Temporal Network Analysis

```python
# In Python
from igraph import *

# Create graph with time attributes
g = Graph(...)
for i, v in enumerate(g.vs):
    v["time"] = (start_time, end_time)

# Export for dynamic visualization
igraph2sonia(g, "output.son")
```

---

## 📝 Development Guidelines for AI Assistants

### When Reading Code

1. **Check library imports first**
   - Python: `from igraph import *` vs `import igraph`
   - R: `library(igraph)`, `library(Cairo)`, `library(gclus)`

2. **Identify the network source**
   - Look for `read.graph()` or `Graph.Read_Pajek()`
   - Note the file path (may need updating)

3. **Understand the analysis goal**
   - Community detection? Look for `community_*` functions
   - Visualization? Check `plot()` calls and layout methods
   - Metrics? Look for `degree()`, `betweenness()`, `closeness()`

### When Modifying Code

1. **File Paths**
   - ⚠️ Many scripts have hardcoded paths like `~/Desktop/wsanalysis/`
   - Always verify file paths exist before running
   - Prefer relative paths when possible

2. **Data Format Compatibility**
   - Pajek format requires: `*vertices N` then `*edges` or `*arcs`
   - SONIA format is tab-separated with specific column headers
   - AWK scripts expect space/tab delimited input

3. **Graph Simplification**
   - Always call `simplify(G)` after loading to remove self-loops
   - This prevents errors in many algorithms

4. **Layout Algorithms**
   - `fruchterman.reingold` (FR): General purpose, force-directed
   - `circle`: Nodes on a circle (good for small graphs)
   - `kk`: Kamada-Kawai spring layout
   - `lgl`: Large graph layout (for big networks)

5. **Community Detection Best Practices**
   - Compare multiple algorithms
   - Check modularity scores
   - Visualize results for validation
   - Consider graph size when choosing algorithm

### Common Pitfalls

1. **Python 2 vs Python 3**
   - Some scripts use Python 2 syntax: `except Exception, E:`
   - Update to Python 3: `except Exception as E:`

2. **Missing Working Directory**
   - Many R scripts use `setwd()` with specific paths
   - Adjust to current working directory

3. **Large Data Files**
   - `ws.net` is 9.7MB - may be slow to load
   - Consider sampling for testing

4. **Deprecated igraph Functions**
   - Some function names may have changed in newer igraph versions
   - Check igraph documentation if errors occur

---

## 🔍 Code Analysis Examples

### Example 1: Understanding Community Detection

When you see this pattern in R:
```r
wt <- walktrap.community(G, modularity=TRUE)
wmemb <- community.to.membership(G, wt$merges,
                                steps=which.max(wt$modularity)-1)
memberships <- wmemb$membership
```

**Interpretation:**
1. Run walktrap algorithm (random walk based)
2. Create hierarchical merge tree
3. Cut tree at optimal modularity point
4. Extract community memberships

### Example 2: Understanding Visualization Code

When you see:
```r
colbar <- rainbow(max(comps)+1)
V(G)$color <- colbar[comps+1]
plot(G, layout=layout.fruchterman.reingold, vertex.size=10)
```

**Interpretation:**
1. Create color palette with N colors (N = number of communities)
2. Assign colors to vertices based on community membership
3. Plot with force-directed layout

### Example 3: Understanding AWK Data Processing

When you see:
```awk
{ a[$1,$2]++ }
END { for (i=1; i<=max; i++) for (j=1; j<=max; j++) if (a[i,j]>100) print i,j,a[i,j] }
```

**Interpretation:**
1. Use associative array to count (i,j) pairs
2. Filter pairs with frequency > 100
3. Output filtered edge list

---

## 🚀 Quick Reference

### Python igraph Essentials

```python
# Graph creation
g = Graph()
g = Graph(n=10)  # 10 vertices
g = Graph.Lattice([5, 5])  # 5x5 grid
g = Graph.Kautz(m=3, n=2)
g = Graph.Read_Pajek("file.net")

# Graph properties
g.vcount()  # Number of vertices
g.ecount()  # Number of edges
g.is_simple()  # No self-loops or multiple edges?
g = g.simplify()  # Remove self-loops and multiple edges

# Vertex/Edge attributes
g.vs["name"] = [...] # Set vertex names
g.vs[0]["color"] = "red"
g.es["weight"] = [...]

# Analysis functions
degree(g)
betweenness(g)
closeness(g)
g.community_edge_betweenness()
g.community_leading_eigenvector()

# Visualization
plot(g)
plot(g, layout="fr")
plot(g, layout="circle", vertex_size=10, vertex_color="red")
```

### R igraph Essentials

```r
# Graph creation
G <- graph.empty(n=10)
G <- graph.lattice(c(5,5))
G <- read.graph("file.net", format="pajek")

# Graph operations
simplify(G)
minimum.spanning.tree(G)

# Properties
vcount(G)
ecount(G)
degree(G)
betweenness(G)
closeness(G)

# Community detection
walktrap.community(G)
leading.eigenvector.community(G)
edge.betweenness.community(G)
spinglass.community(G, spins=10)

# Visualization
plot(G, layout=layout.fruchterman.reingold)
V(G)$color <- rainbow(max(membership)+1)[membership+1]
```

### AWK Pattern Matching

```awk
# Basic structure
BEGIN { initialization }
/pattern/ { action }
{ default_action }
END { finalization }

# Common patterns
NR==1 { header }  # First line
NF>5 { action }   # Lines with >5 fields
$3>100 { action } # Third field >100

# Associative arrays
{ count[$1]++ }   # Count occurrences
{ sum[$1]+=$2 }   # Sum by key
```

---

## 🔒 Data Files & Formats

### Network Files (*.net)

**Pajek Format:**
```
*Network
*Vertices 100
*Arcs
1 14 1 c black
2 3 1 c black
...
```

**Fields:** source, target, weight, type, color

### Trace Files (*.trc)

Contact trace data - format varies by dataset

### DAT Files (*.dat)

**WS_DISCRETE_100s.dat format:**
```
node1 node2 start_time duration
1 2 100
1 100 100
...
```

### SONIA Files (*.son)

**Format:**
```
//comment
NodeId	StartTime	EndTime	ColorName	NodeSize	BorderWidth
1	0	100	red	10	0
...
FromId	ToId	StartTime	EndTime	ArcWidth
1	2	0	50	1
...
```

---

## 🎓 Research Context

This repository appears to be academic research code for analyzing:

1. **Wireless Sensor Networks (WS)**
   - Various time scales: 100s, 200s, 300s, etc.
   - Different network sizes: ws100s, ws200s, etc.

2. **Social/Contact Networks (CAM)**
   - Cambridge dataset analysis
   - Community structure studies

3. **Mesh Networks**
   - Trace files suggest mesh topology analysis

### Key Research Questions

Based on the code, this research likely investigates:
- How communities form in wireless networks over time
- Comparison of community detection algorithms
- Network topology efficiency (Kautz graphs)
- Path redundancy and resilience
- Temporal dynamics of network connections

---

## ⚠️ Known Issues & Limitations

1. **Python 2 Syntax**
   - Code uses `except Exception, E:` (Python 2)
   - Needs updating for Python 3

2. **Hardcoded Paths**
   - Many scripts reference `/home/amc/Desktop/wsanalysis/`
   - Will fail on different systems

3. **Missing Documentation**
   - No README or comments explaining dataset sources
   - Parameter choices (e.g., spins=10) not justified

4. **Incomplete Scripts**
   - Many commented-out code blocks
   - Suggests exploratory/experimental nature

5. **No Dependency Management**
   - No requirements.txt or environment.yml
   - Required libraries: igraph, Cairo, gclus

---

## 📚 External Resources

### igraph Documentation
- **Python:** https://igraph.org/python/
- **R:** https://igraph.org/r/

### Pajek File Format
- http://mrvar.fdv.uni-lj.si/pajek/

### Community Detection Algorithms
- Newman, M. E. J. (2006). "Modularity and community structure in networks"
- Blondel, V. D., et al. (2008). "Fast unfolding of communities in large networks"

### Network Science
- Barabási, A.-L. "Network Science" - http://networksciencebook.com/

---

## 🤝 Contributing Guidelines (for AI Assistants)

### When Adding New Features

1. **Follow existing patterns**
   - Use igraph for graph operations
   - Maintain separation: Python for algorithms, R for statistical analysis
   - AWK for preprocessing

2. **Document your changes**
   - Add comments explaining algorithm choices
   - Note parameter significance
   - Reference academic papers if applicable

3. **Test with multiple datasets**
   - Small: ws100s.net
   - Medium: ws300.net
   - Large: ws.net

4. **Maintain compatibility**
   - Keep Pajek format for input/output
   - Preserve visualization capabilities

### When Debugging

1. **Check file paths first**
2. **Verify graph is simplified**
3. **Check for disconnected components**
4. **Validate input data format**
5. **Test with small examples**

---

## 📞 Contact & Maintenance

**Original Author Path:** `/home/amc/` (user: amc)

**Repository Status:** Research/Experimental (not production code)

**Last Updated:** Based on file timestamps (2019-11-21)

---

## 🎯 Summary for AI Assistants

**Primary Use Cases:**
1. Analyzing network topology and structure
2. Detecting communities in social/wireless networks
3. Comparing community detection algorithms
4. Visualizing temporal network dynamics
5. Computing graph metrics (centrality, modularity, etc.)

**Key Strengths:**
- Multiple community detection algorithms implemented
- Both Python and R interfaces
- Handles temporal network data
- Good visualization capabilities

**Key Limitations:**
- Dated code (Python 2, old paths)
- Limited documentation
- No automated testing
- Experimental/research quality

**When Working with This Code:**
- Always update file paths
- Check data formats carefully
- Compare results across multiple algorithms
- Validate outputs with visualizations
- Consider modularity scores for community detection quality

---

**Last AI Update:** 2025-11-22
**CLAUDE.md Version:** 1.0
