#include <iostream>
#include <vector>
#include <algorithm>

void printData(std::vector<int> &data)
{
    for (int x : data)
    {
        std::cout << x << " ";
    }
    std::cout << std::endl;
}

void bubbleSort(std::vector<int> &data)
{
    size_t n = data.size();
    bool swapped;
    for (size_t i = 0; i < n - 1; i++)
    {
        swapped = false;
        // Последние i элементов уже на своих местах
        for (size_t j = 0; j < n - i - 1; j++)
        {
            if (data[j] > data[j + 1])
            {
                std::swap(data[j], data[j + 1]);
                swapped = true;
            }
        }

        // Если обменов не было, то массив отсортирован
        if (!swapped)
            break;
    }
}

int main()
{
    std::vector<int> data = {
        2,
        1,
        32,
        8,
        64,
        16,
        4};

    std::cout << "Origin: " << std::endl;
    printData(data);

    bubbleSort(data);

    std::cout << "Sorted: " << std::endl;
    printData(data);

    return 0;
}
