```python
import numpy as np

x_data = np.array([1., 2., 3.])
y_data = np.array([2., 4., 6.])

W = 0.0
b = 0.0

n_data = len(x_data)

epochs = 1000
learning_rate = 0.01

for i in range(epochs):
    hypothesis = x_data * W + b
    cost = np.sum((hypothesis - y_data) ** 2) / n_data
    gradient_w = np.sum((W * x_data - y_data + b) * 2 * x_data) / n_data
    gradient_b = np.sum((W * x_data - y_data + b) * 2) / n_data

    W -= learning_rate * gradient_w
    b -= learning_rate * gradient_b

    f = 'Epoch ({:10d}/{:10d}) cost: {:10f}, W: {:10f}, b: {:10}'.format(
            i, epochs, cost, W, b)
    if i % 100 == 0:
        print(f)

print('W: {:10}'.format(W))
print('b: {:10}'.format(b))
print('result:')
print(x_data * W + b)
```
