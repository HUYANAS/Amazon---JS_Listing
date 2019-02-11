# 不可变数据类型:数字,字符串,元组         可变类型:列表,字典
#
# l=[2,2,3]
# print(id(l))
# l[0]=5
# print(id(l))   # 当你对可变类型进行修改时,比如这个列表对象l,它的内存地址不会变化,注意是这个列表对象l,不是它里面的元素
#                # this is the most important
#
# s='alex'
# print(id(s))   #像字符串,列表,数字这些不可变数据类型,,是不能修改的,比如我想要一个'Alex'的字符串,只能重新创建一个'Alex'的对象,然后让指针只想这个新对象
#
# s[0]='e'       #报错
# print(id(s))

# 重点:浅拷贝
# a = [[1, 2], 3, 4]
# b = a[:]  # b=a.copy()
#
# print(a, b)
# print(id(a), id(b))
# print('*************')
# print('a[0]:', id(a[0]), 'b[0]:', id(b[0]))
# print('a[0][0]:', id(a[0][0]), 'b[0][0]:', id(b[0][0]))
# print('a[0][1]:', id(a[0][1]), 'b[0][1]:', id(b[0][1]))
# print('a[1]:', id(a[1]), 'b[1]:', id(b[1]))
# print('a[2]:', id(a[2]), 'b[2]:', id(b[2]))
#
# print('___________________________________________')
# b[0][0] = 8
#
# print(a, b)
# print(id(a), id(b))
# print('*************')
# print('a[0]:', id(a[0]), 'b[0]:', id(b[0]))
# print('a[0][0]:', id(a[0][0]), 'b[0][0]:', id(b[0][0]))
# print('a[0][1]:', id(a[0][1]), 'b[0][1]:', id(b[0][1]))
# print('a[1]:', id(a[1]), 'b[1]:', id(b[1]))
# print('a[2]:', id(a[2]), 'b[2]:', id(b[2])) # outcome

# L1 = ['a', 'b', ['c','h']]
# L2 = L1
# L3 = L1[:]
#
# print('L1=', L1)
# print('L2=', L2)
# print('L3=', L3)
# print('*'*30)
#
#
# L1.append('d')
# print('L1=', L1)
# print('L2=', L2)
# print('L3=', L3)
# print('*'*30)
#
# L1[2].append('p')
# print('L1=', L1)
# print('L2=', L2)
# print('L3=', L3)
# print('*'*30)
#
# L3[0] = 'o'
# print('L1=', L1)
# print('L2=', L2)
# print('L3=', L3)
# print('*'*30)
#
# L3.append('e')
# print('L1=', L1)
# print('L2=', L2)
# print('L3=', L3)
# print('*'*30)
#
#
# L2.remove('a')
# print('L1=', L1)
# print('L2=', L2)
# print('L3=', L3)

# a = [1.5,-2,3,-8,9,-5,9,8,5,-6]
# a[[i for i in a if i<0]] = 0
# print(a)


import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

x = np.arange(1,0,-0.001)
y = (-3*x*np.log(x) + np.exp(-(40*(x-1/np.e))**4)/25)
plt.figure(figsize=(5,7))
plt.plot(y,x,'r-',linewidth=2)
plt.grid(True)
plt.show()