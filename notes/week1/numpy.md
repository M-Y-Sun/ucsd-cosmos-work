# NumPy

### `ndarray`

An array is a way to represent many numbers in an organized way.

- A 1D array is a <i>vectors</i>

  | 0   | 1   | 2   |
  | --- | --- | --- |

- A 2D array is a <i>matrix </i>

  | 0   | 1   | 2   |
  | --- | --- | --- |
  | 0   | 1   | 2   |
  | 0   | 1   | 2   |

- A 3D array is a <i>3rd order tensor</i>
- An nD array is an <i>nth order tensor</i>

### Array Basics

```py
import numpy as np

a1 = np.zeros((4,3))  # create a 4x3 array with zeros. i.e. int arr[4][3];
a2 = np.ones((5,2))   # create a 5x2 array with ones. i.e.  int arr[5][2];
a3 = np.array([[1, 2, 3], [4, 5, 6]])  # create a numpy array from a list

a1[0, 0] = 8    # sets the array at (0, 0) to 5
a1.ndim         # number of dimensions
shp = a1.shape  # tuple of the dimensions of the array
r, c = a1.shape  # tuple of the dimensions of the array
```

##### Slicing

```py
a1[2,1] = 8

a2 = a1          # both a1 and a2 point to the same memory now
a2[2, 1] = 6     # sets the value at index (2, 1)
print(a1[2, 1])  # prints 6

a3 = x1.copy()
a3[2, 1] = 6
print(a3[2, 1])  # prints 8

# the colon
a4 = a1[1:3, :]  # [a:b] gets the element in the range [a,b)
                 # [:] gets all
                 # [a:] means a to end
                 # [:a] means beginning to a

a1[:2, 1:3] = 6  # sets all the sliced elements to 6
```

### Array Operations

```py
a2 = (a1[:, 1:3] > 3)  # creates an array of bools

asum = np.sum(a1)              # gets the sum of all the elements
asum_arr = np.sum(a1, axis=0)  # sums the elements in the first dimension
```
