# Hybrid Recommender System

Built as a part of my final year project during graduation.

Uses [Movielens 100K dataset](http://files.grouplens.org/datasets/movielens/ml-latest-small.zip) (2016 version)

## Features/Methods


Collaborative filtering
- User-based Collaborative Filtering 
- Item-based Collaborative Filtering 
- CF using Singular Value Decomposition (SVD) 
- Popularity based (implemented as sum of all ratings recieved on a particular movie)

Content Based Filtering
- Simple Approach
- Normalising of Category vector (The size of similarity matrix reduced from 9000x9000 to 800x800.)
- Using Bag of Words (for movie titles)

Hybridization techniques
- Mixed Hybridization
- Switching
- Feature Combining: Collaborative Via Content Based

## User Interface

The focus on UI was low because focus was on algorithm.

![](https://github.com/ankschoubey/Hybrid_Recommender_System/blob/master/Screenshots/Recommendation%20when%20user%20rates%20a%20few%20movies.png)

[More screenshots](https://github.com/ankschoubey/Hybrid_Recommender_System/tree/master/Screenshots)

## Load virtual environment and dependencies

Better to use [Anaconda](https://anaconda.org/)

Creation: ```conda env create -f conda_environment.yml```

Load Environment: ```source activate recommender```

For those using ```pip```

```pip install -r requirements.txt```

## Download and extract

[MovieLens Dataset](http://files.grouplens.org/datasets/movielens/ml-latest-small.zip).

## For building database

Use MySQL. Create a empty database. Remember database name.


## Running

Make sure MySQL server is running.

Run ```sample_recommender.py``` to check everything works properly.

If you are setting up for the first time you will be asked for database details.

If you want to reset run ```generate_defaults.py``` or delete ```defaults.json``` file

Also you would have to make changes to ```DATABASE```variable in ```Hybrid_Recommender_System/setting.py``` which Django will use.


## Release Versions

[v0.1-alpha](https://github.com/ankschoubey/Hybrid-Recommender-System/releases/tag/v0.1-alpha) - Command Line Interface

[v0.2-alpha](https://github.com/ankschoubey/Hybrid_Recommender_System/releases/tag/v0.2-alpha) - Django Support

## References

### Recommender Systems Basics

- [A PRACTICAL GUIDE TO BUILDING RECOMMENDER SYSTEMS](https://buildingrecommenders.wordpress.com/)

- [Hybridization: Collaborative Via Content Based](http://recommender-systems.org/hybrid-recommender-systems/)

### SVD: 
- [A Gentle Introduction to Singular-Value Decomposition for Machine Learning](https://machinelearningmastery.com/singular-value-decomposition-for-machine-learning/)

- [Singular Value decomposition (SVD) in recommender systems for Non-math-statistics-programming wizards](https://medium.com/@m_n_malaeb/singular-value-decomposition-svd-in-recommender-systems-for-non-math-statistics-programming-4a622de653e9)

### For Faster Numerical Computations in Python
[NumPy Tutorial: Data analysis with Python](https://www.dataquest.io/blog/numpy-tutorial-python/)

[Numpy Cheatsheet](https://www.dataquest.io/blog/large_files/numpy-cheat-sheet.pdf)

[Pandas Tutorial: Data analysis with Python: Part 1](https://www.dataquest.io/blog/pandas-python-tutorial/)

[Pandas Tutorial: Data analysis with Python: Part 2](https://www.dataquest.io/blog/pandas-tutorial-python-2/)

[scipy.sparse.csr_matrix](https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.sparse.csr_matrix.html)

[sklearn.metrics.pairwise.cosine_similarity](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html)

## Things not implemented

1. [Thoughts on **Working with Larger Dataset**](https://github.com/ankschoubey/Hybrid_Recommender_System/wiki/Thoughts-on-Working-with-Larger-Dataset)
2. [Thoughts on **working with multi criteria dataset**](https://github.com/ankschoubey/Hybrid_Recommender_System/wiki/Thoughts-on-working-with-multi-criteria-dataset)
