import json


class ItemBasedColaborativeFiltering:
    def __init__(self, target_playlist):
        self.__target = target_playlist

    def generate_target_profile(self):
        pass

    def generate_recommendations(self):
        pass


if __name__ == "__main__":
    with open("./../files/sample_playlist.json", "r") as f:
        playlist = json.loads(f.read())

    recommender = ItemBasedColaborativeFiltering(playlist)
    result = recommender.generate_recommendations()
    print(result)

