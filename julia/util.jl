# --------------- These codes implement some utility functions for general tensor spectral clustering ---------------------

# --------------- Author: Tao Wu
#---------------- Email: wutao27@gmail.com

# to modify
# readtensor skip

push!(LOAD_PATH, pwd())

import Base.isless
import DataStructures

include("shift_fixpoint.jl")

GAMA = 0.2;

type algPara
  ALPHA::Float64
  MIN_NUM::Int64
  MAX_NUM::Int64
  PHI::Float64
  OUTPUT::String
end

# load the tensor data
# format assumption: the first two rows are non-data
function read_tensor(abPath::AbstractString)
  f = readdlm(abPath, skipstart=0)
  m = size(f,2)
  P = Array[round(Int32,vec(f[:,1]))]
  for i = 2:m-1
      P = [P; Array[round(Int32,vec(f[:,i]))]]
  end
  P = [P; Array[map(Float64,vec(f[:,m]))]]
  f = 0
  return P
end

# normalize the tensor
function norm_tensor(P)
  n = length(P[1]); m = size(P,1)-1
  tab = Dict()
  for k=1:length(P[1])
    tempArray = []
    for i = 2:m
      push!(tempArray,P[i][k])
    end
    tempKey = tuple(tempArray...)
    if haskey(tab,tempKey)
      tab[tempKey] = tab[tempKey] + P[m+1][k]
    else
      tab[tempKey] = P[m+1][k]
    end
  end

  for k=1:length(P[1])
    tempArray = []
    for i = 2:m
      push!(tempArray,P[i][k])
    end
    tempKey = tuple(tempArray...)
    P[m+1][k] = P[m+1][k]/tab[tempKey]
  end
end

# compute transition matrix from the tensor P and the distribution x
function tran_matrix(P, x)
  n = Int64(maximum(P[1]))  #transition matrix column length
  RT = zeros(n,n)
  m = size(P,1)-1  # tensor dimension
  NZ = size(P[1],1) # total number of non-zero items in the tensor
  for i = 1:NZ
    ind1 = P[1][i];ind2 = P[2][i];val = P[m+1][i]
    mul = 1
    for j = 3:m
      mul = mul * x[P[j][i]]
    end
    itemVal = val * mul
    RT[ind2,ind1] += itemVal
  end
  return sparse(RT)
end

# save transition matrix to output file
function save(RT, output)
    f = open(output, "w")
    data = ""
    index = 0
    nonzeros = 0
    for i = 1:size(RT,1)
        vecStr = ""
        for j = 1:size(RT,2)
            separator = j == 1 ? "" : "\t"
            item = RT[i, j]
            vecStr = "$vecStr$separator$item"
        end
        separator = i == 1 ? "" : "\n"
        data = "$data$separator$vecStr"
    end

    write(f, data)
    close(f)
end


# compute the eigenvector by calling shift_fix, tran_matrix and eigs
function compute_egiv(P, al, ga, output)
  n = Int64(maximum(P[1]))
  v = ones(n)/n
  println("\tcomputing the super-spacey random surfer vector")
  x =shift_fix(P,v,al,ga,n)
  xT = transpose(x)
  println("\tgenerating transition matrix: P[x]")
  RT = tran_matrix(P, x)

  save(RT, output)
end

# generate recursive two-way cuts for the tensor
# P is tensor data
# algParameters contains parameters for the algorithm: ALPHA, MIN_NUM, MAX_NUM, PHI
function tensor_srw(P, algParameters::algPara)
  norm_tensor(P);
  println("\ttensor size $(maximum(P[1])) with $(length(P[1])) non-zeros")
  (ev,RT,x) = compute_egiv(P,algParameters.ALPHA,GAMA,algParameters.OUTPUT)
end
