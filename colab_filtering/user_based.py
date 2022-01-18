import json


class UserBasedColaborativeFiltering:
    def __init__(self, target_playlist, num_chunks=1000):
        self.__target = target_playlist
        self.__num_chunks = num_chunks

    def calculate_similarity(self, other_playlist):
        track_uris = []
        for track in other_playlist["tracks"]:
            track_uris.append(track["track_uri"])

        size = len(self.__target["tracks"])
        num_similar = 0
        for track in self.__target["tracks"]:
            if track["track_uri"] in track_uris:
                num_similar += 1

        return num_similar * 100 / size

    def find_non_present(self, other_playlist):
        track_uris = []
        for track in self.__target["tracks"]:
            track_uris.append(track["track_uri"])

        non_present = []
        for track in other_playlist["tracks"]:
            if track["track_uri"] not in track_uris:
                non_present.append((track["track_uri"], track["pos"]))

        return non_present

    def find_most_similar_playlists(self):
        similarities_playlists = dict()
        max_sim = 0
        for i in range(self.__num_chunks):
            with open(f"./data/mpd.slice.{i * 1000}-{i * 1000 + 999}.json", "r") as f:
                chunk = json.loads(f.read())["playlists"]
            for j in range(1000):
                playlist = chunk[j]
                similarity_percent = self.calculate_similarity(playlist)
                if similarity_percent > max_sim:
                    max_sim = similarity_percent
                if similarity_percent > 0:
                    similarities_playlists[i * 1000 + j] = similarity_percent

        max_sim_playlists = list()
        for ind in similarities_playlists:
            if similarities_playlists[ind] + 5 >= max_sim:
                max_sim_playlists.append(ind)

        return max_sim_playlists

    def generate_recommendations(self):
        similar_playlists_indexes = self.find_most_similar_playlists()

        similar_playlists = []
        for ind in similar_playlists_indexes:
            chunk_ind = ind // 1000
            offset = ind - (ind // 1000)*1000
            with open(f"./data/mpd.slice.{chunk_ind * 1000}-{chunk_ind * 1000 + 999}.json", "r") as f:
                playlist = json.loads(f.read())["playlists"][offset]
                similar_playlists.extend(self.find_non_present(playlist))

        similar_playlists = sorted(similar_playlists, key=lambda x: x[1])
        similar_playlists = [i[0] for i in similar_playlists]
        return similar_playlists


if __name__ == "__main__":
    with open("./../files/sample_playlist.json", "r") as f:
        playlist = json.loads(f.read())

    recommender = UserBasedColaborativeFiltering(playlist, 2)
    result = recommender.generate_recommendations()
    print(result)
