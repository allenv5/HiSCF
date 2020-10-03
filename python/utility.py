INPUT_DATA_DELIMITER = "\t"


def read_node_map_from_graph(filename):
    node_map = {}
    index = 0

    f = open(filename)
    for line in f:
        items = line.rstrip('\n').split(INPUT_DATA_DELIMITER)
        if items[0] == 'v':
            node_map[items[1].strip()] = index
            index += 1

    return node_map
