# version code 80e56511a793+
# Please fill out this stencil and submit using the provided submission script.

from GF2 import one, zero
from vec import Vec
from mat import Mat
from bitutil import bits2mat, str2bits, noise, mat2bits, bits2str
from matutil import coldict2mat, mat2coldict

## Task 1
""" Create an instance of Mat representing the generator matrix G. You can use
the procedure listlist2mat in the matutil module (be sure to import first).
Since we are working over GF (2), you should use the value one from the
GF2 module to represent 1"""
from matutil import listlist2mat

G = listlist2mat([[one, zero, one, one],
                  [one, one, zero, one],
                  [zero, zero, zero, one],
                  [one, one, one, zero],
                  [zero, zero, one, zero],
                  [zero, one, zero, zero],
                  [one, zero, zero, zero]])
print(G)

## Task 2
# Please write your answer as a list. Use one from GF2 and 0 as the elements.
from vecutil import list2vec

p = list2vec([one, zero, one, zero])
print(G * p)
encoding_1001 = [0, 0, one, one, 0, 0, one]

## Task 3
# Express your answer as an instance of the Mat class.
R = listlist2mat([[zero, zero, zero, zero, zero, zero, one],
                  [zero, zero, zero, zero, zero, one, zero],
                  [zero, zero, zero, zero, one, zero, zero],
                  [zero, zero, one, zero, zero, zero, zero]])
print(R * G)

## Task 4
# Create an instance of Mat representing the check matrix H.
H = listlist2mat([[zero, zero, zero, one, one, one, one],
                  [zero, one, one, zero, zero, one, one],
                  [one, zero, one, zero, one, zero, one]])
print(H * G)


## Task 5
def find_error(syndrome):
    """
    Input: an error syndrome as an instance of Vec
    Output: the corresponding error vector e
    Examples:
        >>> find_error(Vec({0,1,2}, {0:one})) == Vec({0, 1, 2, 3, 4, 5, 6},{3: one})
        True
        >>> find_error(Vec({0,1,2}, {2:one})) == Vec({0, 1, 2, 3, 4, 5, 6},{0: one})
        True
        >>> find_error(Vec({0,1,2}, {1:one, 2:one})) == Vec({0, 1, 2, 3, 4, 5, 6},{2: one})   
        True
        >>> find_error(Vec({0,1,2}, {})) == Vec({0,1,2,3,4,5,6}, {})
        True
    """
    index = sum([2 ** (2 - x) for x in syndrome.f.keys() if syndrome.f[x] == one])
    if index == 0:
        return Vec({0, 1, 2, 3, 4, 5, 6}, {})
    else:
        return Vec({0, 1, 2, 3, 4, 5, 6}, {index - 1: one})


## Task 6
# Use the Vec class for your answers.
non_codeword = Vec({0, 1, 2, 3, 4, 5, 6}, {0: one, 1: 0, 2: one, 3: one, 4: 0, 5: one, 6: one})
print('non_codeword', non_codeword)
error_syndrome = H * non_codeword
print('error_syndrome', error_syndrome)
error_vector = find_error(error_syndrome)
print('error_vector', error_vector)
code_word = non_codeword + error_vector
print('code_word', code_word)
original = R * code_word
print('original', original)


## Task 7
def find_error_matrix(S):
    """
    Input: a matrix S whose columns are error syndromes
    Output: a matrix whose cth column is the error corresponding to the cth column of S.
    Example:
        >>> S = listlist2mat([[0,one,one,one],[0,one,0,0],[0,0,0,one]])
        >>> find_error_matrix(S) == Mat(({0, 1, 2, 3, 4, 5, 6}, {0, 1, 2, 3}), {(1, 3): 0, (3, 0): 0, (2, 1): 0, (6, 2): 0, (5, 1): one, (0, 3): 0, (4, 0): 0, (1, 2): 0, (3, 3): 0, (6, 3): 0, (5, 0): 0, (2, 2): 0, (4, 1): 0, (1, 1): 0, (3, 2): one, (0, 0): 0, (6, 0): 0, (2, 3): 0, (4, 2): 0, (1, 0): 0, (5, 3): 0, (0, 1): 0, (6, 1): 0, (3, 1): 0, (2, 0): 0, (4, 3): one, (5, 2): 0, (0, 2): 0})
        True
    """

    return coldict2mat({k: find_error(mat2coldict(S)[k]) for k in mat2coldict(S).keys()})


S = listlist2mat([[0, one, one, one], [0, one, 0, 0], [0, 0, 0, one]])
print(find_error_matrix(S) == Mat(({0, 1, 2, 3, 4, 5, 6}, {0, 1, 2, 3}),
                                  {(1, 3): 0, (3, 0): 0, (2, 1): 0, (6, 2): 0, (5, 1): one, (0, 3): 0, (4, 0): 0, (1, 2): 0, (3, 3): 0, (6, 3): 0, (5, 0): 0, (2, 2): 0, (4, 1): 0,
                                   (1, 1): 0, (3, 2): one, (0, 0): 0, (6, 0): 0, (2, 3): 0, (4, 2): 0, (1, 0): 0, (5, 3): 0, (0, 1): 0, (6, 1): 0, (3, 1): 0, (2, 0): 0,
                                   (4, 3): one, (5, 2): 0, (0, 2): 0}))

## Task 8
s = "I'm trying to free your mind, Neo. But I can only show you the door. You're the one that has to walk through it."

P = bits2mat(str2bits(s))
print(P)

## Task 9
C = G * P
print(C)
bits_before = len(str2bits(s))
print(bits_before)
bits_after = len(mat2bits(C))
print(bits_after
      )
## Ungraded Task
CTILDE = C + noise(C, 0.02)
print(CTILDE)


## Task 10
def correct(A):
    """
    Input: a matrix A each column of which differs from a codeword in at most one bit
    Output: a matrix whose columns are the corresponding valid codewords.
    Example:
        >>> A = Mat(({0,1,2,3,4,5,6}, {1,2,3}), {(0,3):one, (2, 1): one, (5, 2):one, (5,3):one, (0,2): one})
        >>> correct(A) == Mat(({0, 1, 2, 3, 4, 5, 6}, {1, 2, 3}), {(0, 1): 0, (1, 2): 0, (3, 2): 0, (1, 3): 0, (3, 3): 0, (5, 2): one, (6, 1): 0, (3, 1): 0, (2, 1): 0, (0, 2): one, (6, 3): one, (4, 2): 0, (6, 2): one, (2, 3): 0, (4, 3): 0, (2, 2): 0, (5, 1): 0, (0, 3): one, (4, 1): 0, (1, 1): 0, (5, 3): one})
        True
    """
    return A + find_error_matrix(H * A)


print(bits2str(mat2bits(CTILDE)))
print(bits2str(mat2bits(R * correct(CTILDE))))
