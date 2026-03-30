import copy
import statistics
import time
from typing import Callable, Iterable, Optional


class Bench:
    @staticmethod
    def this(
        func: Callable[[Iterable], None],
        data: Iterable,
        *,
        repeats: int = 3,
        scale_sizes: Optional[list[int]] = None,
        scale_factor: int = 2,
        max_scale_steps: int = 5,
        inplace: bool = True,
        verbose: bool = True,
    ) -> list[tuple[int, float]]:

        # Подготовка списка размеров
        base_size = len(list(data))
        if scale_sizes is None:
            sizes = [base_size]
            for _ in range(max_scale_steps - 1):
                sizes.append(sizes[-1] * scale_factor)
        else:
            sizes = list(scale_sizes)

        results: list[tuple[int, float]] = []

        for size in sizes:
            # Сформировать входные данные для текущего размера (`size`)
            # Если исходный data меньше требуемого размера - повторим элементы для заполнения;
            # если больше - обрежем.
            src = list(data)
            if len(src) == 0 and size > 0:
                # Если исходный data пустой, то используем range(size)
                base = list(range(size, 0, -1))
            else:
                base = (src * ((size // len(src)) + 1))[:size]

            times: list[float] = []
            for _ in range(repeats):
                arr = copy.deepcopy(base)

                t0 = time.perf_counter()

                res = func(arr)

                t1 = time.perf_counter()

                # Если func возвращает новый объект и inplace=False, можно опереться на res
                if not inplace and res is not None:
                    pass

                times.append(t1 - t0)

            median_time = statistics.median(times)
            results.append((size, median_time))

        if verbose:
            # печать простого табличного вывода
            print(f"{'size':>10} | {'time (s)':>12}")
            print("-"*25)
            for size, t in results:
                print(f"{size:10d} | {t:12.6f}")

        return results
