# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class NormalisedContentbasedfilteringData(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    action = models.BigIntegerField(db_column='Action', blank=True, null=True)  # Field name made lowercase.
    adventure = models.BigIntegerField(db_column='Adventure', blank=True, null=True)  # Field name made lowercase.
    animation = models.BigIntegerField(db_column='Animation', blank=True, null=True)  # Field name made lowercase.
    children = models.BigIntegerField(db_column='Children', blank=True, null=True)  # Field name made lowercase.
    comedy = models.BigIntegerField(db_column='Comedy', blank=True, null=True)  # Field name made lowercase.
    crime = models.BigIntegerField(db_column='Crime', blank=True, null=True)  # Field name made lowercase.
    documentary = models.BigIntegerField(db_column='Documentary', blank=True, null=True)  # Field name made lowercase.
    drama = models.BigIntegerField(db_column='Drama', blank=True, null=True)  # Field name made lowercase.
    fantasy = models.BigIntegerField(db_column='Fantasy', blank=True, null=True)  # Field name made lowercase.
    film_noir = models.BigIntegerField(db_column='Film_Noir', blank=True, null=True)  # Field name made lowercase.
    horror = models.BigIntegerField(db_column='Horror', blank=True, null=True)  # Field name made lowercase.
    musical = models.BigIntegerField(db_column='Musical', blank=True, null=True)  # Field name made lowercase.
    mystery = models.BigIntegerField(db_column='Mystery', blank=True, null=True)  # Field name made lowercase.
    romance = models.BigIntegerField(db_column='Romance', blank=True, null=True)  # Field name made lowercase.
    sci_fi = models.BigIntegerField(db_column='Sci_Fi', blank=True, null=True)  # Field name made lowercase.
    thriller = models.BigIntegerField(db_column='Thriller', blank=True, null=True)  # Field name made lowercase.
    war = models.BigIntegerField(db_column='War', blank=True, null=True)  # Field name made lowercase.
    western = models.BigIntegerField(db_column='Western', blank=True, null=True)  # Field name made lowercase.
    unknown = models.BigIntegerField(blank=True, null=True)
    normalised_key = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Normalised_ContentBasedFiltering_data'


class NormalisedContentbasedfilteringMap(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    normalised_key = models.BigIntegerField(blank=True, null=True)
    movieid = models.BigIntegerField(db_column='movieId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Normalised_ContentBasedFiltering_map'


class NormalisedContentbasedfilteringSimilarity(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    number_0 = models.BigIntegerField(db_column='0', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_1 = models.BigIntegerField(db_column='1', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_2 = models.BigIntegerField(db_column='2', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_3 = models.BigIntegerField(db_column='3', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_4 = models.BigIntegerField(db_column='4', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_5 = models.BigIntegerField(db_column='5', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_6 = models.BigIntegerField(db_column='6', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_7 = models.BigIntegerField(db_column='7', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_8 = models.BigIntegerField(db_column='8', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_9 = models.BigIntegerField(db_column='9', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    movieid = models.BigIntegerField(db_column='movieId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Normalised_ContentBasedFiltering_similarity'


class Popularitybasedfiltering(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    number_0 = models.BigIntegerField(db_column='0', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_1 = models.BigIntegerField(db_column='1', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_2 = models.BigIntegerField(db_column='2', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_3 = models.BigIntegerField(db_column='3', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_4 = models.BigIntegerField(db_column='4', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_5 = models.BigIntegerField(db_column='5', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_6 = models.BigIntegerField(db_column='6', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_7 = models.BigIntegerField(db_column='7', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_8 = models.BigIntegerField(db_column='8', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_9 = models.BigIntegerField(db_column='9', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    categories = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'PopularityBasedFiltering'


class SimpleCollaborativefilteringItemRecommendation(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    number_0 = models.BigIntegerField(db_column='0', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_1 = models.BigIntegerField(db_column='1', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_2 = models.BigIntegerField(db_column='2', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_3 = models.BigIntegerField(db_column='3', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_4 = models.BigIntegerField(db_column='4', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_5 = models.BigIntegerField(db_column='5', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_6 = models.BigIntegerField(db_column='6', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_7 = models.BigIntegerField(db_column='7', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_8 = models.BigIntegerField(db_column='8', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_9 = models.BigIntegerField(db_column='9', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    movieid = models.BigIntegerField(db_column='movieId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Simple_CollaborativeFiltering_item_recommendation'


class SimpleCollaborativefilteringSimilarUser(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    number_0 = models.BigIntegerField(db_column='0', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_1 = models.BigIntegerField(db_column='1', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_2 = models.BigIntegerField(db_column='2', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_3 = models.BigIntegerField(db_column='3', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_4 = models.BigIntegerField(db_column='4', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_5 = models.BigIntegerField(db_column='5', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_6 = models.BigIntegerField(db_column='6', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_7 = models.BigIntegerField(db_column='7', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_8 = models.BigIntegerField(db_column='8', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_9 = models.BigIntegerField(db_column='9', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    userid = models.BigIntegerField(db_column='userId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Simple_CollaborativeFiltering_similar_user'


class SimpleCollaborativefilteringUserRecommendation(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    number_0 = models.BigIntegerField(db_column='0', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_1 = models.BigIntegerField(db_column='1', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_2 = models.BigIntegerField(db_column='2', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_3 = models.BigIntegerField(db_column='3', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_4 = models.BigIntegerField(db_column='4', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_5 = models.BigIntegerField(db_column='5', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_6 = models.BigIntegerField(db_column='6', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_7 = models.BigIntegerField(db_column='7', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_8 = models.BigIntegerField(db_column='8', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    userid = models.BigIntegerField(db_column='userId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Simple_CollaborativeFiltering_user_recommendation'


class SimpleContentbasedfiltering(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    number_0 = models.BigIntegerField(db_column='0', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_1 = models.BigIntegerField(db_column='1', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_2 = models.BigIntegerField(db_column='2', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_3 = models.BigIntegerField(db_column='3', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_4 = models.BigIntegerField(db_column='4', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_5 = models.BigIntegerField(db_column='5', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_6 = models.BigIntegerField(db_column='6', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_7 = models.BigIntegerField(db_column='7', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_8 = models.BigIntegerField(db_column='8', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_9 = models.BigIntegerField(db_column='9', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    movieid = models.BigIntegerField(db_column='movieId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Simple_ContentBasedFiltering'


class Links(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    movieid = models.BigIntegerField(db_column='movieId', blank=True, null=True)  # Field name made lowercase.
    imdbid = models.BigIntegerField(db_column='imdbId', blank=True, null=True)  # Field name made lowercase.
    tmdbid = models.FloatField(db_column='tmdbId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'links'


class MovieInfo(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    backdrop = models.TextField(blank=True, null=True)
    backdrop_path = models.TextField(blank=True, null=True)
    movieid = models.TextField(db_column='movieId', blank=True, null=True)  # Field name made lowercase.
    original_language = models.TextField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    poster = models.TextField(blank=True, null=True)
    poster_path = models.TextField(blank=True, null=True)
    production_countries = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    video = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'movie_info'


class Movies(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    movieid = models.BigIntegerField(db_column='movieId', blank=True, null=True)  # Field name made lowercase.
    title = models.TextField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)
    action = models.BigIntegerField(db_column='Action', blank=True, null=True)  # Field name made lowercase.
    adventure = models.BigIntegerField(db_column='Adventure', blank=True, null=True)  # Field name made lowercase.
    animation = models.BigIntegerField(db_column='Animation', blank=True, null=True)  # Field name made lowercase.
    children = models.BigIntegerField(db_column='Children', blank=True, null=True)  # Field name made lowercase.
    comedy = models.BigIntegerField(db_column='Comedy', blank=True, null=True)  # Field name made lowercase.
    crime = models.BigIntegerField(db_column='Crime', blank=True, null=True)  # Field name made lowercase.
    documentary = models.BigIntegerField(db_column='Documentary', blank=True, null=True)  # Field name made lowercase.
    drama = models.BigIntegerField(db_column='Drama', blank=True, null=True)  # Field name made lowercase.
    fantasy = models.BigIntegerField(db_column='Fantasy', blank=True, null=True)  # Field name made lowercase.
    film_noir = models.BigIntegerField(db_column='Film_Noir', blank=True, null=True)  # Field name made lowercase.
    horror = models.BigIntegerField(db_column='Horror', blank=True, null=True)  # Field name made lowercase.
    musical = models.BigIntegerField(db_column='Musical', blank=True, null=True)  # Field name made lowercase.
    mystery = models.BigIntegerField(db_column='Mystery', blank=True, null=True)  # Field name made lowercase.
    romance = models.BigIntegerField(db_column='Romance', blank=True, null=True)  # Field name made lowercase.
    sci_fi = models.BigIntegerField(db_column='Sci_Fi', blank=True, null=True)  # Field name made lowercase.
    thriller = models.BigIntegerField(db_column='Thriller', blank=True, null=True)  # Field name made lowercase.
    war = models.BigIntegerField(db_column='War', blank=True, null=True)  # Field name made lowercase.
    western = models.BigIntegerField(db_column='Western', blank=True, null=True)  # Field name made lowercase.
    unknown = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'movies'


class MoviesMapped(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    movieid = models.BigIntegerField(db_column='movieId', blank=True, null=True)  # Field name made lowercase.
    original_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'movies_mapped'


class Ratings(models.Model):
    index = models.BigIntegerField(blank=True, null=True)
    userid = models.BigIntegerField(db_column='userId', blank=True, null=True)  # Field name made lowercase.
    movieid = models.BigIntegerField(db_column='movieId', blank=True, null=True)  # Field name made lowercase.
    rating = models.BigIntegerField(blank=True, null=True)
    timestamp = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ratings'
