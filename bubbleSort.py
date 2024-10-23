import numpy as np

arr = np.array([2,1,3,4,6,5])

def bubbleSort(arr) :
    while True :
        switch = 0
        for i in range(len(arr)-1):
            if arr[i] > arr[i+1] :
                temp = arr[i]
                arr[i] = arr[i+1]
                arr[i+1] = temp
                switch += 1
                
            if switch == 0 :
                return arr
            
sorted_arr = bubbleSort(arr)
print(sorted_arr)