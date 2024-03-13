"""
outbreak_tester

this time, dynamically deal with it

"""

from typing import List, Tuple
# from functools import cache
import numpy
import matplotlib.pyplot as plt


def outbreak_check(data: List[int], sequence_length: int = 3) -> List[Tuple[int, int]]:
    """
    get the sequence of data and find abnormality
    """

    outbreaks = abnormality_check(data, 0, sequence_length)

    print("----------Possible Outbreaks----------")

    for idx in range(0, len(outbreaks), 2):
        print(data[outbreaks[idx]:outbreaks[idx+1]])

    print("--------------------------------------")


def abnormality_check(data: List[int],
                      starting_index: int,
                      running_size: int = 3,
                      prev_average: float = None,
                      prev_diff: float = None,
                      abnormal: bool = False,
                      decreasing: bool = False,
                      abnormal_count: int = 0,
                      last_normal_average: float = None) -> List[int]:

    if running_size+starting_index > len(data):
        if abnormal:
            return [len(data) - abnormal_count, len(data)]
        return []

    average = numpy.average(data[starting_index:starting_index+running_size])

    if prev_average is None:
        return abnormality_check(data, starting_index+1, running_size, average)

    diff = data[starting_index+running_size-1] - prev_average

    if abnormal:
        if decreasing:
            if abs(average - last_normal_average) / average < 0.15:
                return ([starting_index - abnormal_count + 1, starting_index+1]
                        + abnormality_check(data, starting_index+1,
                                            running_size, average))

        if diff < 0:
            return abnormality_check(data, starting_index+1, running_size, average, diff,
                                     abnormal=True,
                                     decreasing=True,
                                     abnormal_count=abnormal_count+1,
                                     last_normal_average=last_normal_average)

        return abnormality_check(data, starting_index+1, running_size, average, diff,
                                 abnormal=True,
                                 abnormal_count=abnormal_count+1,
                                 last_normal_average=last_normal_average)

    if prev_diff is None:
        return abnormality_check(data, starting_index+1, running_size, average, diff)

    if diff - prev_diff > average*0.3:
        return abnormality_check(data, starting_index+1, running_size, average, diff,
                                 abnormal=True,
                                 abnormal_count=abnormal_count+1,
                                 last_normal_average=prev_average)

    return abnormality_check(data, starting_index+1, running_size, average, diff)


if __name__ == "__main__":
    TEST_DATA = [10, 10, 10, 11,
                 11, 13, 12, 11,
                 16, 12, 18, 14,
                 10, 12, 15, 12,
                 11, 10, 10, 11,
                 13, 12, 14, 11,
                 17, 19, 25, 40,
                 39, 36, 34, 32,
                 21, 20, 23, 20,
                 20, 17, 12, 11,
                 19, 12, 15, 20,
                 22, 20, 25, 12,
                 10, 15, 10, 9]

    TEST_DATA2 = [20, 18, 16, 23, 21,
                  26, 30, 23, 20, 22,
                  74, 80, 65, 50, 20,
                  30, 20, 30, 25, 20,
                  17, 19, 20]

    outbreak_check(TEST_DATA)
    outbreak_check(TEST_DATA2)

    outbreak_index = abnormality_check(TEST_DATA, 0)

    for i in range(0, len(outbreak_index), 2):
        for j in range(outbreak_index[i], outbreak_index[i+1]):
            plt.scatter(j, TEST_DATA[j], color="red")

    plotted_data = numpy.array(TEST_DATA)

    plt.plot(plotted_data)
    plt.title("Visiual Representation")
    plt.xlabel("Index")
    plt.ylabel("Numbers")
    plt.grid(False)
    plt.show()

    outbreak_index = abnormality_check(TEST_DATA2, 0)

    for i in range(0, len(outbreak_index), 2):
        for j in range(outbreak_index[i], outbreak_index[i+1]):
            plt.scatter(j, TEST_DATA2[j], color="red")

    plotted_data = numpy.array(TEST_DATA2)

    plt.plot(plotted_data)
    plt.title("Visiual Representation")
    plt.xlabel("Index")
    plt.ylabel("Numbers")
    plt.grid(False)
    plt.show()
