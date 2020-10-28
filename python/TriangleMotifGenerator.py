import datetime as dt
import numpy as np
import utility

INPUT_DATA_DELIMITER = "\t"
OUTPUT_DATA_DELIMITER = " "
STAT_STRING_DELIMITER = ","


def __append_matched_top_records(i, j, k):
    save_data = "{0}\t{1}\t{2}\n".format(i, j, k)
    return save_data


def __get_idx_in_data(i, j, n):
    return int((n * 2 - i - 1) * i / 2 + j - i - 1)


def __cal_num_com(arr_1, arr_2):
    num_com = 0
    for item in arr_1:
        num_com += 1 if item in arr_2 else 0
    return num_com


def __single_top_tensor_process(index_array, data, num_nodes, output_file):
    index_len = len(index_array)
    save_data = ""
    for i in range(0, index_len):
        node_i = index_array[i]
        for node_j in range(node_i + 1, num_nodes):
            idx_in_data = __get_idx_in_data(node_i, node_j, num_nodes)
            min_idx = __get_idx_in_data(node_j, node_j + 1, num_nodes)
            max_idx = min_idx + num_nodes - node_j - 1

            for k in range(min_idx, max_idx):
                node_k = node_j + k + 1 - min_idx
                assert node_k > node_j

                if node_k in data[idx_in_data]:
                    save_data += __append_matched_top_records(node_i, node_j, node_k)

    __save(output_file, save_data)


def __single_stat_process(index_arr, new_arr, input_data, num_nodes):
    index_len = len(index_arr)

    for i in range(0, index_len):
        node_i = index_arr[i]

        for node_j in range(node_i + 1, num_nodes):
            new_arr_idx = __get_idx_in_data(node_i, node_j, num_nodes)
            new_arr[new_arr_idx] = __get_com_idx_arr(input_data[node_i], input_data[node_j])


def __get_com_idx_arr(arr_1, arr_2):
    n = len(arr_1)
    arr = []

    for i in range(0, n):
        if arr_1[i] and arr_2[i]:
            arr.append(i)

    return arr


def __split_list(alist, wanted_parts=1):
    length = len(alist)

    if length <= wanted_parts:
        return [[alist[i]] for i in range(0, length)]

    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts] for i in range(wanted_parts)]


def __gen_tensor_data(input_matrix, output_file):
    n = len(input_matrix)
    index_array = [i for i in range(0, n - 1)]

    input_arr_len = int(n * (n - 1) / 2)
    input_arr = []
    for i in range(0, input_arr_len):
        input_arr.append([])

    __single_stat_process(index_array, input_arr, input_matrix, n)
    __single_top_tensor_process(index_array, input_arr, n, output_file)


def __gen_adjacency_matrix(graph_file, node_map):
    n = len(node_map)

    input_data = np.zeros([n, n])
    f = open(graph_file)
    for line in f:
        items = line.rstrip('\n').split(INPUT_DATA_DELIMITER)
        if items[0] == 'e':
            id_1 = node_map[items[1].strip()]
            id_2 = node_map[items[2].strip()]
            input_data[id_1][id_2] = 1
            input_data[id_2][id_1] = 1

    return input_data


def __save(save_file, data):
    file = open(save_file, 'w')
    file.write(data)
    file.close()


def run(graph_file):
    print("Start generating tensor at %s" % dt.datetime.now())
    output_file = graph_file + "-motif"
    input_data = __gen_adjacency_matrix(graph_file, utility.read_node_map_from_graph(graph_file))

    __gen_tensor_data(input_data, output_file)
    print("Saved to file [%s] at %s" % (output_file, dt.datetime.now()))

    return output_file
