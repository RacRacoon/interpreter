def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i  # min_idx diinisialisasi dengan i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j  # perbarui min_idx jika elemen yang lebih kecil ditemukan
        arr[i], arr[min_idx] = arr[min_idx], arr[i]  # tukar elemen
    return arr

arr = [5, 2, 3, 1, 4]
sorted_arr = selection_sort(arr)
print(sorted_arr)
