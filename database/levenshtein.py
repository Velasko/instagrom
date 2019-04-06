#from numpy import zeros

def minimo(tab, X, Y, cost):
    if X > 0 and Y > 0:
        return min((tab[X-1][Y] + 1,
                    tab[X][Y-1] + 1,
                    tab[X-1][Y-1] + cost
                    ))
    elif X > 0:
        return tab[X-1][Y] + 1
    elif Y > 0:
        return tab[X][Y-1] + 1
    else:
        return cost

def distance(word1, word2, case_sensitive = False, return_matrix=False, print_matrix=False):
    """This code shows how many operations would be necessary to change the word1 into word2.
    The parameters are:

    case_sensitive: Bool
        Parameter to decide if it wants to consider A = a or not.

    return_matrix: Bool
        If True, returns the matrix for the path.
        False returns the difference between the string

    print_matrix: Bool
        Show or not the matrix showing the path for the change

    """

    if case_sensitive:
        word1 = word1.lower()
        word2 = word2.lower()

    tab = [[ 0 for _ in enumerate(word2)] for _ in enumerate(word1) ]

    for i, e in enumerate(word1):
        tab[i][0] = i
    for j, e in enumerate(word2):
        tab[0][j] = j

    for X, i in enumerate(word1):
        for Y, j in enumerate(word2):
            if i == j:
                cost = 0
            else:
                cost = 1

            tab[X][Y] = minimo(tab, X, Y, cost)

    if print_matrix:
        print(tab)

    if return_matrix:
        return tab
    return tab[-1][-1]

if __name__ == '__main__':
    print(distance('keka', 'kk'))