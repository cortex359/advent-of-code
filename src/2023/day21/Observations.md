# Observations for Part 2

Steps $26,501,365$, resulting in a grid repetition of at the axis of 
$\frac{26,501,365}{131} \cdot 2 = 404,601$ grids.

The graph is unweighted, cyclic and undirected.

### Example:

| steps | garden plots | 
|------:|-------------:|
|     6 |           16 |
|    10 |           50 |
|   100 |         6536 |
|  1000 |       668697 |
|    50 |         1594 |
|   500 |       167004 |
|  5000 |     16733044 | 

### Input:

| steps | garden plots | 
|------:|-------------:|
|    64 |         3722 |
|    65 |         3814 |
|   101 |         9144 |
|   201 |        35947 |
|   301 |        79593 |


| i mit s = i*131 + 65 | Steps    | Start Position | Grid Size     | Garden Plots     |
|----------------------|----------|----------------|---------------|------------------|
| 0                    | 65       | (196, 196)     | 393x393       | 3814             |
| 1                    | 196      | (327, 327)     | 655x655       | 33952            |
| 2                    | 327      | (458, 458)     | 917x917       | 94138            |
| 3                    | 458      | (589, 589)     | 1179x1179     | 184372           |
| 4                    | 589      | (720, 720)     | 1441x1441     | 304654           |
| 5                    | 720      | (851, 851)     | 1703x1703     | 454984           |
| 6                    | 851      | (982, 982)     | 1965x1965     | 635362           |
| 7                    | 982      | (1113, 1113)   | 2227x2227     | 845788           |
| 8                    | 1113     | (1244, 1244)   | 2489x2489     | 1086262          |
| 9                    | 1244     | (1375, 1375)   | 2751x2751     | 1356784          |
| 10                   | 1375     | (1506, 1506)   | 3013x3013     | 1657354          |
| 11                   | 1506     | (1637, 1637)   | 3275x3275     | 1987972          |
| 12                   | 1637     | (1768, 1768)   | 3537x3537     | 2348638          |
| 202300               | 26501365 |                | 404601x404601 | 614864614526014  |


Sei $d=65$ die Startposition im Gitter, $n=131$ die Länge des Gitters und $s=26.501.365$ die Anzahl der Schritt.
Wir definieren $i := \frac{s - 65}{131} + 1$ als relevante Vielfache und erhalten eine Funktion $g(i)$ für die Anzahl der Gartenbeete in Abhängigkeit von $i$.
$$g(i) = 15.024 \cdot i^2 - 14.934 \cdot i + 3.724$$

