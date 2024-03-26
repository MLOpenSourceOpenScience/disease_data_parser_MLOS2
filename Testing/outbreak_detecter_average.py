"""
outbreak_tester

tried using average diffrence calculation but failed.

"""

from typing import List, Tuple
# from functools import cache
import numpy
import matplotlib.pyplot as plt

def outbreak_check(data: List[int]) -> List[Tuple[int, int]]:
    """
    get the sequence of data and find abnormality
    """

    outbreaks = []

    return outbreaks


def abnormality_detection(data: List[int],
                          current: int = 0,
                          sample_length: int = 20,
                          abnormal_indexes: List[int] = None,
                          abnormal_length: int = 0) -> List[int]:
    """
    Check outbreaks!!!!!
    """

    if current == 0:
        return abnormality_detection(data, current+1)

    if current >= len(data):
        return []

    if abnormal_indexes is None:
        abnormal_indexes = []

    starting_index = current - sample_length

    if starting_index < -15:
        return abnormality_detection(data, current+1,
                                     abnormal_indexes= abnormal_indexes)

    if starting_index < 0:
        starting_index = 0
        # at least 5 samples prior

    clean_data = []

    for i, value in enumerate(data):
        if starting_index <= i and i < current and i not in abnormal_indexes:
            clean_data.append(value)

    sample_median = numpy.median(clean_data[:len(clean_data)])
    refined_data = [abs(x - sample_median) for x in clean_data]

    standard_deviation = numpy.std(refined_data)

    if sample_median + 4*standard_deviation < data[current]:
        abnormal_indexes.append(current)
        return [current] + abnormality_detection(data, current+1,
                                                 abnormal_indexes= abnormal_indexes,
                                                 abnormal_length= abnormal_length+1)

    return abnormality_detection(data, current+1,
                                 abnormal_indexes= abnormal_indexes)

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
                  17, 19, 20, 20, 19,
                  30, 22, 15, 20, 21]

    TEST_DATA3 = [100, 100, 100, 100, 100,
                  125, 150, 200, 200, 210,
                  190, 175, 150, 120, 120,
                  130, 120, 110, 100, 90,
                  80, 90, 80, 100, 90,
                  70, 80, 90, 80, 70]

    outbreak_index = abnormality_detection(TEST_DATA)

    for idx in outbreak_index:
        plt.scatter(idx, TEST_DATA[idx], color="red")

    plotted_data = numpy.array(TEST_DATA)

    plt.plot(plotted_data)
    plt.title("Visiual Representation")
    plt.xlabel("Index")
    plt.ylabel("Numbers")
    plt.grid(False)
    plt.show()

    outbreak_index = abnormality_detection(TEST_DATA2)

    for idx in outbreak_index:
        plt.scatter(idx, TEST_DATA2[idx], color="red")

    plotted_data = numpy.array(TEST_DATA2)

    plt.plot(plotted_data)
    plt.title("Visiual Representation")
    plt.xlabel("Index")
    plt.ylabel("Numbers")
    plt.grid(False)
    plt.show()

    outbreak_index = abnormality_detection(TEST_DATA3)

    for idx in outbreak_index:
        plt.scatter(idx, TEST_DATA3[idx], color="red")

    plotted_data = numpy.array(TEST_DATA3)

    plt.plot(plotted_data)
    plt.title("Visiual Representation")
    plt.xlabel("Index")
    plt.ylabel("Numbers")
    plt.grid(False)
    plt.show()
