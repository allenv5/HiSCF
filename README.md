# HiSCF: leveraging higher-order structures for clustering analysis in biological networks

#### Lun Hu
#### Jun Zhang
#### Xiangyu Pan
#### Hong Yan
#### Zhu-Hong You
------
### Folders
* `data` contains the biological network data used in the paper.
* `python` contains the python scripts to generate the tensor data and input files for Markov Clustering algorithm (MCL).
* `julia` contains the julia scripts to generate the transition matrix of the first-order Markov chain that approximates the higher-order Markov chain.
* `java` contains the java files to merge the clusters generated from different motifs.


### Usage
1. run `python\main.py` to generate the tensor data for different motifs. Currently, we only support triangle and rectangle motifs.
2. run `julia\main.jl` to generate the transition matrix of the approximating first-order Markov chain.
3. run `python\MclInputGenerator.py` to generate the input files for MCL
4. run MCL to identify clusters for each of selected motifs.
5. run the class of `java\HiSCF_Pruning.java` to merge all the clusters based on the post-processing step described in the paper.

Note: The codes should be compatible with Julia 0.6, Python 3.6 and Java 1.8. If you get errors when running the scrips, please try the recommended versions.
