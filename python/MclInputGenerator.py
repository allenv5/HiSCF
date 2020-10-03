if __name__ == '__main__':
    tran_matrix_file = ''
    dic_file = ''
    outputfile = ''

    f = open(dic_file)
    id_dic = {}
    for line in f:
        items = line.split(" ")
        id_dic[int(items[1])] = items[0]

    f = open(tran_matrix_file)
    array = [line.split("\t") for line in f]

    content = ''
    for i in range(0, len(array)):
        sum = 0
        for j in range(0, len(array[i])):
            sum += float(array[i][j])

        for j in range(0, len(array[i])):
            cell = float(array[i][j])
            if cell > 0:
                content += ("" if len(content) == 0 else "\n") + id_dic[i + 1] + "\t" \
                           + id_dic[j + 1] + "\t" + str(cell / sum)

    mcl_abc_file = open(outputfile, 'w')
    mcl_abc_file.write(content)
    mcl_abc_file.close()
