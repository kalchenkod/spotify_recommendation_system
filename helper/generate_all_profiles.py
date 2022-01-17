import json
import codecs
import datetime


class AllSongProcessing:
    def __init__(self, start, end):
        self.pretty = True
        self.compact = False
        self.cache = {}
        self.songs = {}
        try:
            istart = int(start)
            iend = int(end)
            if 0 <= istart <= iend <= 1000000:
                for pid in range(istart, iend):
                    self.show_playlist(pid, print=False)
                for song in self.songs:
                    self.songs[song][4] = self.songs[song][4] / self.songs[song][5]
                print(len(self.songs))
                self.write_song_profiles(istart, iend)
        except ValueError:
            print("bad pid")

    def print_playlist(self, playlist):
        if self.pretty:
            print("===", playlist["pid"], "===")
            print(playlist["name"])
            print("  followers", playlist["num_followers"])
            print(
                "  modified",
                datetime.datetime.fromtimestamp(playlist["modified_at"]).strftime(
                    "%Y-%m-%d"
                ),
            )
            print("  edits", playlist["num_edits"])
            print()
            if not self.compact:
                for track in playlist["tracks"]:
                    print(
                        "%3d %s - %s"
                        % (track["pos"], track["track_name"], track["album_name"])
                    )
                print()
        else:
            print(json.dumps(playlist, indent=4))

    def show_playlist(self, pid, print):
        if 0 <= pid < 1000000:
            low = 1000 * int(pid / 1000)
            high = low + 999
            offset = pid - low
            path = "./data/mpd.slice." + str(low) + "-" + str(high) + ".json"
            if path not in self.cache:
                f = codecs.open(path, "r", "utf-8")
                js = f.read()
                f.close()
                playlist = json.loads(js)
                self.cache[path] = playlist

            playlist = self.cache[path]["playlists"][offset]
            if print:
                self.print_playlist(playlist)
            self.generate_song_profiles(playlist)

    def generate_song_profiles(self, playlist):
        for track in playlist["tracks"]:
            if track["track_uri"] not in self.songs:
                self.songs[track["track_uri"]] = [track["track_name"],
                                                  track["album_name"],
                                                  track["artist_name"],
                                                  track["duration_ms"],
                                                  track["pos"],
                                                  1,
                                                  playlist["num_followers"]]
            else:
                self.songs[track["track_uri"]][5] += 1
                self.songs[track["track_uri"]][6] += playlist["num_followers"]
                self.songs[track["track_uri"]][4] += track["pos"]

    def write_song_profiles(self, istart, iend):
        with open(f"./../files/song_profiles.{istart}-{iend}.json", "w") as f:
            f.write(json.dumps(self.songs, indent=4))



if __name__ == "__main__":
    s = AllSongProcessing(900000, 1000000)
