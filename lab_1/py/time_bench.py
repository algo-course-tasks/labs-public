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
        """
        Замер времени выполнения func на переданных данных.

        Параметры:
        - func: функция, принимающая iterable  и выполняющая сортировку/обработку.
                Должна изменять или возвращать отсортированный результат — Bench перед вызовом делает копию входных данных.
        - data: исходный iterable. Не изменяется методами Bench.
        - repeats: сколько прогонов для каждого размера (медиана берётся для устойчивости).
        - scale_sizes: явный список размеров, на которых нужно измерять (например [100,1000,10000]).
                       Если None, то используются размеры, начинающиеся от len(data) и умножающиеся на scale_factor
                       max_scale_steps раз.
        - scale_factor: множитель размера при автоматическом масштабировании.
        - max_scale_steps: число шагов масштабирования (игнорируется, если scale_sizes передан).
        - inplace: если True, предполагается, что func меняет переданный список на месте;
                   если False, func должна возвращать новый список/итерируемый (Bench использует возвращаемое значение).
        - verbose: печатать таблицу результатов.

        Возвращает:
        - список кортежей (size, median_time_seconds) в порядке проверяемых размеров.
        """

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
            # Сформировать входные данные для текущего размера
            # если исходный data меньше требуемого размера — повторим элементы для заполнения;
            # если больше — обрежем.
            src = list(data)
            if len(src) == 0 and size > 0:
                # если исходный data пустой, используем range(size)
                base = list(range(size, 0, -1))
            else:
                base = (src * ((size // len(src)) + 1))[:size]

            times: list[float] = []
            for _ in range(repeats):
                arr = copy.deepcopy(base)
                t0 = time.perf_counter()
                res = func(arr)
                t1 = time.perf_counter()
                # если func возвращает новый объект и inplace=False, можно опереться на res
                if not inplace and res is not None:
                    # ничего дополнительно не делаем, просто позволим функции вернуть результат
                    pass
                times.append(t1 - t0)

            # используем медиану для устойчивости против выбросов
            median_time = statistics.median(times)
            results.append((size, median_time))

        if verbose:
            # печать простого табличного вывода
            print(f"{'size':>10} | {'time (s)':>12}")
            print("-" * 25)
            for size, t in results:
                print(f"{size:10d} | {t:12.6f}")

        return results
