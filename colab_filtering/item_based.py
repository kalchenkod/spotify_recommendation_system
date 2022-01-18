import json
from colab_filtering.playlist_profile import PlaylistProfile


class ItemBasedColaborativeFiltering:
    def __init__(self, target_playlist):
        self.__target = target_playlist
        self.__profile = PlaylistProfile(target_playlist)

    def generate_recommendations(self):
        with open("./files/reduced_song_profiles.json", "r") as f:
            song_profiles = json.loads(f.read())

        song_difference = dict()
        for track in song_profiles:
            profile = song_profiles[track]
            for i in range(7, 14):
                try:
                    profile[i] = float(profile[i])
                except ValueError:
                    profile[i] = 0
            song_difference[track] = self.__profile.song_difference(profile)

        diffs_100 = sorted(song_difference.values())[100:]
        recommendations = list()
        for song in song_difference:
            if song_difference[song] in diffs_100:
                recommendations.append(song)

        return recommendations


if __name__ == "__main__":
    with open("./../files/sample_playlist.json", "r") as f:
        playlist = json.loads(f.read())

    recommender = ItemBasedColaborativeFiltering(playlist)
    result = recommender.generate_recommendations()
    print(result)
