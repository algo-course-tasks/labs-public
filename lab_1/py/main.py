import random

from time_bench import Bench


# Доступ к элементу по индексу - O(1)
def element_by_index(data: list, index: int):
    return data[index]


# Поиск наибольшего числа в массиве - O(n)
def max_in_list(data: list[int]) -> int:
    if not data:
        raise ValueError("Пустой список")
    maximum = data[0]
    for x in data[1:]:
        if x > maximum:
            maximum = x
    return maximum


# Сортировка пузырьком - O(n^2)
def bubble_sort(data: list[int]) -> None:
    swapped = False
    for i in range(0, len(data) - 1):  # O(n)
        swapped = False

        for j in range(0, len(data) - i - 1):  # O(n)
            if data[j] > data[j + 1]:  # O(1) * O(1)
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True

        if not swapped:
            break


# Бинарный поиск в отсортированном массиве - O(log n)
def binary_search(sorted_arr: list[int], target: int) -> int:
    lo, hi = 0, len(sorted_arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_arr[mid] == target:
            return mid
        elif sorted_arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1  # не найдено


# Рекурсивное вычисление чисел Фибоначчи - O(2^n)
def fib_exp(index: int) -> int:
    if index < 0:
        raise ValueError("n >= 0")
    if index <= 1:
        return index
    return fib_exp(index - 1) + fib_exp(index - 2)


def integers(n: int, start: int, end: int) -> list[int]:
    return [random.randint(start, end) for _ in range(n)]


def main() -> None:
    b = Bench.this(
        bubble_sort,
        data=integers(10, 0, 1_000_000),
        scale_factor=10,
        max_scale_steps=4,
    )


if __name__ == "__main__":
    main()
