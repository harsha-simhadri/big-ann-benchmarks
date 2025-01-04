from PyCANDYAlgo import utils
import numpy as np

sp = utils.NumpyIdxQueue(5)
print(sp.size())
print(sp.capacity())

ar1=np.array([[1,2,3],[2,3,4]],dtype=float)
ar2=np.array([[3,4,5],[4,5,6]],dtype=float)
ar3=np.array([[5,6,7],[6,7,8]],dtype=float)
ar4=np.array([[7,8,9],[8,9,10]],dtype=float)
ar5=np.array([[9,10,11],[10,11,12]],dtype=float)
ar6=np.array([[10,11,12],[11,12,13]],dtype=float)

sp.try_push(utils.NumpyIdxPair(ar1,[1,2]))
print(f"size={sp.size()}")
print(f"front={sp.front().vectors} {sp.front().idx}")


n2=utils.NumpyIdxPair(ar2,[3,4])
n3=utils.NumpyIdxPair(ar3,[5,6])
n4=utils.NumpyIdxPair(ar4,[7,8])
n5=utils.NumpyIdxPair(ar5,[9,10])
n6=utils.NumpyIdxPair(ar6,[11,12])
sp.push(n2)
sp.push(n3)
sp.push(n4)
sp.push(n5)
print(f"After pushing 5 elements size={sp.size()}")
print(f"After pushing 5 elements front={sp.front().vectors} {sp.front().idx}")
sp.push(n6)
print(f"After pushing n6 size={sp.size()}")
print(f"After pushing n6 front={sp.front().vectors} {sp.front().idx}")
del n2
print(f"After delete n2 size={sp.size()}")
print(f"After delete n2 front={sp.front().vectors} {sp.front().idx}")

sp.pop()
print(f"After popping 1st front={sp.front().vectors} {sp.front().idx}")
print(f"After popping 1st size={sp.size()}")

sp.pop()
print(f"After popping 2nd front={sp.front().vectors} {sp.front().idx}")
print(f"After popping 2nd size={sp.size()}")

sp.pop()
print(f"After popping 3rd front={sp.front().vectors} {sp.front().idx}")
print(f"After popping 3rd size={sp.size()}")

sp.pop()
print(f"After popping 4th front={sp.front().vectors} {sp.front().idx}")
print(f"After popping 4th size={sp.size()}")

sp.pop()
#print(f"After popping 5th front={sp.front().vectors} {sp.front().idx}")
print(f"After popping 5th size={sp.size()}")


