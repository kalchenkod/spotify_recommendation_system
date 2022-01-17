import json
import csv


class ReducedSongProcessing:
    @staticmethod
    def generate_reduced_profiles():
        reduced_song_profile = dict()
        with open("./../files/song_profiles-all.json", "r") as f:
            song_profiles = json.loads(f.read())
        with open("./../files/genres.csv", "r", encoding="utf-8") as f:
            genres_dataset = csv.reader(f, delimiter=',')
            for record in genres_dataset:
                track_uri = record[-9]
                danceability = record[0]
                energy = record[1]
                loudness = record[3]
                mode = record[4]
                speechiness = record[5]
                acousticness = record[6]
                instrumentalness = record[7]
                try:
                    song_profile = song_profiles[track_uri]
                    if len(song_profile) == 7:
                        song_profile.extend(
                            [danceability, energy, loudness, mode, speechiness, acousticness, instrumentalness])
                        reduced_song_profile[track_uri] = song_profile
                except KeyError:
                    pass
        with open(f"./../files/reduced_song_profiles.json", "w") as f:
            f.write(json.dumps(reduced_song_profile, indent=4))
        print(len(reduced_song_profile))


if __name__ == "__main__":
    ReducedSongProcessing.generate_reduced_profiles()
