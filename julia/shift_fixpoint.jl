
# ------ These codes compute the stationary distribution for the super-spacey random surfer -------------

# --------------- Author: Tao Wu
#---------------- Email: wutao27@gmail.com

#compute the corresponding value of the kron of x for index-th value of tensor P
function compute_kron(P, index, x)
  m = size(P,1)-1; result = 1
  for i in 1:m-1
    result = result*x[P[i+1][index]]
  end
  return result
end

# Compute Px where P is a tensor
function sparse_kron(P, x)
  n = size(x,1); m = size(P,1)-1; Px = zeros(n)
  for ind = 1:size(P[1],1)
    Px[P[1][ind]] += P[m+1][ind]*compute_kron(P,ind,x)
  end
  return Px
end


# P is a sparse tensor with row(columns) list and value list
function shift_fix(P, v, alpha, gama, n)
  maxiter = 10000; tol = 1/10^(6); e = ones(n)/n
  x_old = rand(n)
  x_old = x_old/sum(x_old)
  for i = 1:maxiter
    Px = sparse_kron(P, x_old)
    x_new = (alpha/(1+gama))*Px + ((1-alpha)/(1+gama))*v + (gama/(1+gama))*x_old
    #sumx = sum(x_new); x_new += (1-sumx)*e
    sumx = sum(x_new); x_new = x_new/sumx
    #println("1-norm of x_old is $sumx")
    res = sum(abs.(x_new-x_old))
    if res <= tol
      #println("find the fix point within $i iterations")
      return(x_new)
    end
    #println("---iter $i residual is $res")
    x_old = x_new
  end
  error("cannot find the fix point within $maxiter iterations")
end
