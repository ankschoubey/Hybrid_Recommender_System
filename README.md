## Load virtual environment and dependencies

Better to use [Anaconda](https://anaconda.org/)

Creation: ```conda env create -f conda_environment.yml```

Load Environment: ```source activate recommender```

## Download and extract

[MovieLens Dataset](http://files.grouplens.org/datasets/movielens/ml-latest-small.zip).

## For building database

Use MySQL. Create a empty database. Remember database name.

## Running

Make sure MySQL server is running.

Run ```recommender.py```

If you are setting up for the first time you will be asked for database details.

If you want to reset run ```generate_defaults.py``` or delete ```defaults.json``` file
