from dataset import load_movie_lens
from dataset import print_matrix
from dataset import load_pickle
from dataset import save_pickle
from dataset import file_exists
from memory_based_collaborative_filtering import *

data = load_movie_lens('ml-100k/u2.base')
#print_matrix(data)
print('1')
user_similar_matrix = build_user_similarity_matrix(data)
print_matrix(user_similar_matrix)



print('done')