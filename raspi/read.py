from serial import Serial
from doctest import testmod
from math import sqrt

# S1:0|1|2|3....255;
# S2:0|1|2|3....255;
# S3:0|1|2|3....255;
# S4:0|1|2|3....255;

# Reading from sensors
# S:a0|a1| ...... d0|d1| ... d255|\n


def stat(lst):
    """Calculate mean and std deviation from the input list."""
    n = float(len(lst))
    mean = sum(lst) / n
    stdev = sqrt((sum(x*x for x in lst) / n) - (mean * mean))
    return mean, stdev


def parse(lst, n):
    cluster = []
    cluster_index = 0
    for index, val in enumerate(lst):
        if len(cluster) <= 1:    # the first two values are going directly in
            cluster.append(val)
            continue

        mean, stdev = stat(cluster)

        if abs(mean - val) > n * stdev:
            yield cluster, cluster_index + len(cluster) / 2, mean
            cluster_index += len(cluster)
            cluster[:] = []

        cluster.append(val)
    yield cluster, cluster_index + len(cluster) / 2, mean


def get_clusters(a, range_start=0, range_end=1500):
    """
    >>> a = [1023, 983, 834, 675, 698, 456, 234, 324, 456, 363, 1023, 1045, 982, 763, 674, 743]
    >>> res = get_clusters(a)
    >>> res
    [{'cluster_coordinate': 1.0, 'cluster': [1023, 983], 'cluster_mean': 1003.0}, {'cluster_coordinate': 3.5, 'cluster': [834, 675, 698], 'cluster_mean': 735.6666666666666}, {'cluster_coordinate': 7.5, 'cluster': [456, 234, 324, 456, 363], 'cluster_mean': 366.6}, {'cluster_coordinate': 11.0, 'cluster': [1023, 1045], 'cluster_mean': 1034.0}, {'cluster_coordinate': 14.0, 'cluster': [982, 763, 674, 743], 'cluster_mean': 806.3333333333334}]
    """
    if not a:
        return []

    res = []
    for cluster, cluster_coordinate, cluster_mean in parse(a, 3):
        if range_start < cluster_mean < range_end:
            res.append({
                'cluster': cluster[:],
                'cluster_coordinate': cluster_coordinate,
                'cluster_mean': cluster_mean,
            })
    return res

def get_vals(l):
    """
    >>> line = b'S:1023|983|834|234|324|456|363|1023|1045|\\n'
    >>> get_vals(line)
    [1023, 983, 834, 234, 324, 456, 363, 1023, 1045]
    """
    line = l.decode('utf-8')
    label_vals = line.split(':')
    label = label_vals[0]
    try:
        vals = label_vals[1].split('|')
        vals.pop()
        vals = list(map(int, vals))
        return vals
    except Exception as e:
        return []


def get_means(a, chunk_size):
    """
    >>> a = [1023, 983, 834, 234, 324, 456, 363, 1023, 1045]
    >>> get_means(a, 3)
    {0: 946.6666666666666, 1: 683.6666666666666, 2: 464.0, 3: 338.0, 4: 381.0, 5: 614.0, 6: 810.3333333333334}
    """
    index_mean_map = {}
    for index, value in enumerate(a):
        last_index = index + chunk_size
        subarray = a[index: last_index]
        if len(subarray) == chunk_size:
            index_mean_map[index] = sum(subarray) / chunk_size

    return index_mean_map


def get_sums(a, chunk_size):
    """
    >>> a = [1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0]
    >>> get_sums(a, 3)
    {0: 2, 1: 1, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1, 7: 0, 8: 0, 9: 1, 10: 1}
    """
    index_sum_map = {}
    for index, value in enumerate(a):
        last_index = index + chunk_size
        subarray = a[index: last_index]
        if len(subarray) == chunk_size:
            index_sum_map[index] = sum(subarray)
    return index_sum_map


def read_from_serial():
    ser = Serial(
        # port='/dev/cu.usbmodem1411',
        port='/dev/ttyACM0',
        baudrate=250000,
        timeout=1,
    )
    # to ignore garbage values
    ser.readline()
    # for the string 'Reading from sensors'
    ser.readline()

    while True:
        line = ser.readline()
        arr = get_vals(line)
        res = get_clusters(arr, range_start=400, range_end=700)
        val = 0

        print(arr)
        if res:
            val = res[0]
            print('coordinate')
            print(val['cluster_coordinate'])
        # else:
        #     print('no clusters in range')


    ser.close()


def read():
    read_from_serial()

if __name__ == '__main__':
    # testmod()
    read()
