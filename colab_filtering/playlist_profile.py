import csv
import json


class PlaylistProfile:
    def __init__(self, target_playlist):
        self.__danceability = 0
        self.__energy = 0
        self.__loudness = 0
        self.__mode = 0
        self.__speechiness = 0
        self.__acousticness = 0
        self.__instrumentalness = 0
        self.__artists = set()
        self.__track_names = set()

        track_genres = self.get_genres()
        num_appearances = 0
        for track in target_playlist["tracks"]:
            self.__artists.add(track["artist_name"])
            self.__track_names.add(track["track_name"])
            if track["track_uri"] in track_genres:
                self.__danceability += track_genres[track["track_uri"]][0]
                self.__energy += track_genres[track["track_uri"]][1]
                self.__loudness += track_genres[track["track_uri"]][2]
                self.__mode += track_genres[track["track_uri"]][3]
                self.__speechiness += track_genres[track["track_uri"]][4]
                self.__instrumentalness += track_genres[track["track_uri"]][5]
                num_appearances += 1

        self.__danceability /= num_appearances
        self.__energy /= num_appearances
        self.__loudness /= num_appearances
        self.__mode /= num_appearances
        self.__speechiness /= num_appearances
        self.__instrumentalness /= num_appearances
        self.__profile_features = [self.__danceability, self.__energy, self.__loudness, self.__mode, self.__speechiness,
                                   self.__acousticness, self.__instrumentalness]

    @staticmethod
    def get_genres():
        track_genres = dict()
        with open("./files/genres.csv", "r", encoding="utf-8") as f:
            genres_dataset = csv.reader(f, delimiter=',')
            for record in genres_dataset:
                track_uri = record[-9]
                track_genres[track_uri] = []

                for i in [0, 1, 3, 4, 5, 6, 7]:
                    try:
                        track_genres[track_uri].append(float(record[i]))
                    except ValueError:
                        track_genres[track_uri].append(0)
        return track_genres

    def song_difference(self, song_profile):
        difference = 0
        song_features = song_profile[7:]

        for i in range(len(song_features)):
            if i == 2:
                difference += ((song_features[i] - self.__profile_features[i]) ** 2) / 100
            else:
                difference += (song_features[i] - self.__profile_features[i]) ** 2

        if song_profile[3] in self.__artists:
            difference -= 0.5
        if song_profile[0] in self.__track_names:
            difference -= 1
        return difference


if __name__ == "__main__":
    with open("./../files/sample_playlist.json", "r") as f:
        playlist = json.loads(f.read())

    song_profile = [
        "Mercury: Retrograde",
        "Hexada",
        "Ghostemane",
        124538,
        7096.7957868303565,
        107,
        306,
        0.831,
        0.8140000000000001,
        -7.364,
        1,
        0.42,
        0.0598,
        0.013
    ]

    profile = PlaylistProfile(playlist)
    result = profile.song_difference(song_profile)
    print(result)
