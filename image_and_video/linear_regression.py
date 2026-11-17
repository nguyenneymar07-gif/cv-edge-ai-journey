import numpy as np

def predict(x, w, b):
    y_pred = w*x + b
    return y_pred

def mse(y_true, y_pred):
    error = y_pred - y_true
    loss = np.mean(error**2)
    return loss,error

def gradient(error, x, w_now, b_now, a):
    w_mes = 2*np.mean(error*x)
    b_mes = 2*np.mean(error)
    w_new = w_now - a*w_mes
    b_new = b_now - a*b_mes    
    return w_new,b_new


x = np.array([1,2,3,4,5])
y = np.array([3,5,7,9,11])
w_now = 0.0
b_now = 0.0
a = 0.01

for i in range(2000):
    y_pred = predict(x,w_now,b_now)
    loss, error = mse(y,y_pred)
    if (i % 200 == 0):
        print(f"i = {i:.2f} | loss = {loss:.6f}")
    w_new, b_new = gradient(error, x, w_now, b_now, a)
    w_now = w_new
    b_now = b_new
print(f"New w is: {w_now:.2f}")
print(f"New b is: {b_now:.2f}")

