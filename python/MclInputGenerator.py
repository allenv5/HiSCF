import os

if __name__ == '__main__':
    root_dir = "data\\triangle"
    dataset = 'arabidopsis'
    tran_matrix_file_template = os.path.join(root_dir, '{0}-tran_matrix')
    dic_file_template = os.path.join(root_dir, '{0}-dic')
    mcl_abc_file_template = '{0}-mcl-abc'

    f = open(dic_file_template.format(dataset))
    idDic = {}
    for line in f:
        items = line.split(" ")
        idDic[int(items[1])] = items[0]

    f = open(tran_matrix_file_template.format(dataset))
    array = [line.split("\t") for line in f]

    content = ''
    for i in range(0, len(array)):
        sum = 0
        for j in range(0, len(array[i])):
            sum += float(array[i][j])

        for j in range(0, len(array[i])):
            cell = float(array[i][j])
            if cell > 0:
                content += ("" if len(content) == 0 else "\n") + idDic[i + 1] + "\t" \
                           + idDic[j + 1] + "\t" + str(cell / sum)

    mcl_abc_file_path = os.path.join(root_dir, mcl_abc_file_template).format(dataset)
    mcl_abc_file = open(mcl_abc_file_path, 'w')
    mcl_abc_file.write(content)
    mcl_abc_file.close()
