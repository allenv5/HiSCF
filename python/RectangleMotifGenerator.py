import datetime as dt
import numpy as np
import utility


def run(graph_file):
    print("Start generating tensor at %s" % dt.datetime.now())

    output_file = graph_file + "-motif"
    node_map = utility.read_node_map_from_graph(graph_file)

    b = []
    for line in open(graph_file, 'r'):
        items = line.split()
        if items[0] == 'e':
            id_1 = node_map[items[1].strip()]
            id_2 = node_map[items[2].strip()]
            tmp = [id_1, id_2]
            b.append(tmp)

    b_len = len(b)
    c = []
    for i in range(1, b_len - 1):
        t0 = b[i - 1]
        for j in range(i, b_len):
            if b[j][0] in t0 or b[j][1] in t0:
                t1 = b[j]
                t01 = list(set(t0) & set(t1))
                t02 = sorted(list(set(t0) ^ set(t1)))
                t02.append(t01[0])
                if len(t02) == 3:
                    c.append(t02)

    result = []
    c_len = len(c)
    for i in range(1, c_len - 1):
        x0 = c[i - 1]
        for j in range(i, c_len):
            if c[j][0] == x0[0] and c[j][1] == x0[1]:
                if x0[0] < min(c[j][-1], x0[-1]):
                    x01 = [x0[0], min(c[j][-1], x0[-1]), x0[1], max(c[j][-1], x0[-1])]
                else:
                    x01 = [min(c[j][-1], x0[-1]), x0[0], max(c[j][-1], x0[-1]), x0[1]]
                result.append(x01)

    arr = np.array(result)
    arr_1 = np.unique(arr, axis=0)

    output = open(output_file, 'w')
    for line in arr_1:
        line = [str(x) for x in line]
        line = '%s' % '\t'.join(line)
        output.write(line + "\n")
    output.close()
    print("Saved to file [%s] at %s" % (output_file, dt.datetime.now()))

    return output_file

