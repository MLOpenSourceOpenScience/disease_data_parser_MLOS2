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

    reported_peaks = peak_detection(data)
    reported_peaks.sort()

    start_index = reported_peaks[0]
    end_index = reported_peaks[0]

    outbreaks = []

    for peak, next_peak in zip(reported_peaks, reported_peaks[1:]):
        if not peak or not next_peak:
            break
        if next_peak - peak > 1:
            outbreaks.append([start_index,end_index])
            start_index = next_peak
            end_index = next_peak
        else:
            end_index = next_peak

    outbreaks.append([start_index,end_index])

    return outbreaks


def peak_detection(data: List[int], removed: List[int] = None) -> List[int]:
    """
    read the data and return the peak value
    """

    if removed is None:
        removed = []
    if len(data) - len(removed) == 1:
        return []

    maxima = 0
    maxindex = 0
    for i, num in enumerate(data):
        if i in removed:
            continue
        if num >= maxima:
            maxima = num
            maxindex = i

    percent_changed = average_differnce(data, maxindex)
    new_removed = removed
    new_removed = removed + [maxindex]

    if percent_changed >= 0.05:
        return peak_detection(data, new_removed) + [maxindex]

    return peak_detection(data, new_removed)


def average_differnce(data: List[int], index: int) -> float:
    """
    get the data, then compare the diffrence in average
    """

    normal_average = numpy.mean(data)

    peak_removed_data = data[:index] + data[index+1:]
    deleted_average = numpy.mean(peak_removed_data)

    difference = normal_average - deleted_average

    return difference / normal_average


if __name__ == "__main__":
    TEST_DATA = [0, 0, 0, 0,
                 1, 3, 2, 1,
                 6, 12, 18, 14,
                 0, 2, 5, 2,
                 1, 0, 0, 1,
                 3, 2, 4, 1,
                 7, 9, 15, 10,
                 9, 6, 4, 2,
                 1, 0, 3, 0,
                 0, 1, 2, 1,
                 9, 12, 15, 20,
                 22, 20, 25, 12,
                 10, 5, 0, 0]

    print(average_differnce(TEST_DATA, 10))
    print(peak_detection(TEST_DATA))

    print(outbreak_check(TEST_DATA))

    plotted_data = numpy.array(TEST_DATA)

    plt.plot(plotted_data)
    plt.title("Visiual Representation")
    plt.xlabel("Index")
    plt.ylabel("Numbers")
    plt.grid(False)
    plt.show()
