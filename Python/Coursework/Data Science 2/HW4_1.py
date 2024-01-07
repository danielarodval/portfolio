from matplotlib import pyplot as plt
import numpy as np
x1 = np.arange(-10,0.1,0.1)
x2 = np.arange(0.1,10,0.1)   # start,stop,step
y2 = np.sin(1/x2)
y1 = np.full(
  shape=101,
  fill_value=0,
  dtype=np.int
)

x = np.concatenate((x1,x2))
y = np.concatenate((y1,y2))

del x1, x2, y1, y2

plt.plot(x,y)
plt.show()