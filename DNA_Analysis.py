
from TreeNode import TreeNode
import copy


def parse_fasta(file_name, database):
    """
    COMPLETE
    """

    with open(file_name) as fp:
        while True:
            # strips > symbols change this?
            identifier = (fp.readline()).strip()
            no_arrow = identifier[1:]
            sequence = (fp.readline()).strip()
            if not sequence:
                break
            database[no_arrow] = sequence


def calc_hamming(x, y):
    """
    COMPLETE
    """
    return sum(base1 != base2 for base1, base2 in zip(x, y))


def min_index(d_matrix):
    """
    COMPLETE
    """

    small_cell = 10000
    x = -1
    y = -1

    for i in range(len(d_matrix)):
        for j in range(len(d_matrix[i])):

            if (d_matrix[i][j]) != 0:
                if (d_matrix[i][j]) < small_cell:

                    small_cell = d_matrix[i][j]
                    x, y = i, j

    return x, y


def swap(x, y):
    """
    COMPLETE

    """

    if y < x:

        x, y = y, x

    return x, y


def cluster(d_matrix, x, y):
    """
    COMPLETE
    """

    x, y = swap(x, y)

    change_row = []
    for i in range(0, x):
        change_row.append((d_matrix[x][i] + d_matrix[y][i]) / 2)
    d_matrix[x] = change_row

    for i in range(x + 1, y):
        d_matrix[i][x] = (d_matrix[i][x] + d_matrix[y][i]) / 2

    for i in range(y + 1, len(d_matrix)):
        d_matrix[i][x] = (d_matrix[i][x] + d_matrix[i][y]) / 2
        del d_matrix[i][y]

    del d_matrix[y]


def concat_id(id_list_newick, id_list, x, y):

    id_list_newick[x] = "(" + id_list_newick[x] + "," + id_list_newick[y] + ")"

    cat_label = id_list[x] + "/" + id_list[y]
    id_list[x] = id_list[x] + "/" + id_list[y]

    del id_list[y]
    del id_list_newick[y]

    return cat_label


def upgma(d_matrix, id_list, id_list_newick):

    node_list = []

    while len(id_list) > 1:

        x, y = min_index(d_matrix)

        x_id = id_list[x]
        y_id = id_list[y]

        cluster(d_matrix, x, y)

        root_id = concat_id(id_list_newick, id_list, x, y)

        connect = TreeNode(None, None, root_id)

        for i, node in enumerate(node_list):

            if x_id == node.getName():

                connect.setLeft(node_list[i])

            if y_id == node.getName():

                connect.setRight(node_list[i])

        if connect.getLeft() is None:

            left = TreeNode(None, None, x_id)
            connect.setLeft(left)
            node_list.append(left)

        if connect.getRight() is None:

            right = TreeNode(None, None, y_id)
            connect.setRight(right)
            node_list.append(right)

        node_list.append(connect)

    root_id = node_list[-1]

    return root_id


def populate_matrix(d_matrix, database, id_list):
    """
    COMPLETE
    """

    i = 0
    j = 0

    for key in database.keys():

        id_list.append(key)
        for key_2 in database.keys():
            # switch upper/lower
            if j >= i:
                break

            difference = calc_hamming(database[key], database[key_2])
            d_matrix[i][j] = difference
            j += 1
            
        j = 0
        i += 1


def main():

    # BUILD DATABASE
    database = dict()
    id_list = []

    #data_base = "database_test.txt"
    data_base = "database-sequences.fasta"
    parse_fasta(data_base, database)

    sus_file = "query-sequence.fasta"
    parse_fasta(sus_file, database)

    size = len(database)

    d_matrix = [[0 for x in range(size)] for y in range(size)]
    print("### POPULATING MATRIX ###")
    populate_matrix(d_matrix, database, id_list)

    print("### DONE POPULATING ###")

    id_list_newick = copy.deepcopy(id_list)

    print("### DEVELOPING PHYLOGENETIC TREE ###")

    root = upgma(d_matrix, id_list, id_list_newick)

    print("### DONE DEVELOPING TREE ###")

    f = open('newick.txt', 'w')

    print("### WRITING TO NEWICK ###")

    f.write(id_list_newick[0])

    print("### DONE WRITING TO NEWICK ###")
    print(" - Program Complete -")

    #root.preorder(root)


main()


