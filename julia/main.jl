#=
run:
- Julia version:
- Author: Allen
- Date: 2018-08-17
=#
inputfile = "data/arabidopsis-Gtensor"
outputfile= "data/M-tran-matrix"
include("util.jl");
para = algPara(0.8, 5, 100, 0.4, outputfile);
P = read_tensor(inputfile);
tensor_srw(P, para);
