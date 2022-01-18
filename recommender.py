import json
from colab_filtering.cold_start import PopularRecommender
from colab_filtering.item_based import ItemBasedColaborativeFiltering
from colab_filtering.user_based import UserBasedColaborativeFiltering


class SpotifyRecommender:
    def __init__(self, target_playlist):
        self.__target = target_playlist

    def generate_recommendations(self):
        if self.__target["num_tracks"] <= 5:
            recommender = PopularRecommender(self.__target)
            return recommender.generate_recommendations()
        else:
            user_based_recommender = UserBasedColaborativeFiltering(self.__target, 2)
            user_based = user_based_recommender.generate_recommendations()

            item_based_recommender = ItemBasedColaborativeFiltering(self.__target)
            item_based = item_based_recommender.generate_recommendations()

            return user_based + item_based


if __name__ == "__main__":
    # with open("./files/sample_playlist.json", "r") as f:
    #     playlist = json.loads(f.read())
    #
    # recommender = SpotifyRecommender(playlist)
    # result = recommender.generate_recommendations()
    # print(result)

    with open("./files/cold_start_playlist.json", "r") as f:
        small_playlist = json.loads(f.read())

    small_recommender = SpotifyRecommender(small_playlist)
    small_result = small_recommender.generate_recommendations()
    print(small_result)
