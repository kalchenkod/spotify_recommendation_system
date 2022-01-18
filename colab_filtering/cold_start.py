import json


class PopularRecommender:
    def __init__(self, target_playlist):
        self.__target = target_playlist

    def get_popular_songs(self):
        with open("./files/song_profiles-popular100.json", "r") as f:
            popular = json.loads(f.read())
        return popular

    def generate_recommendations(self):
        top_popular = self.get_popular_songs()

        artists = set()
        for track in self.__target["tracks"]:
            artists.add(track["artist_name"])

        recommendations = list()
        for track in top_popular:
            if top_popular[track][2] in artists:
                recommendations.append(track)

        if not recommendations:
            recommendations = top_popular.keys()

        return recommendations


if __name__ == "__main__":
    with open("./../files/cold_start_playlist.json", "r") as f:
        playlist = json.loads(f.read())

    recommender = PopularRecommender(playlist)
    result = recommender.generate_recommendations()
    print(result)