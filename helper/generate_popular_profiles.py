import json


class PopularSongProcessing:
    @staticmethod
    def generate_n_popular(n=100):
        with open(f"./../files/song_profiles-all.json", "r") as f:
            data = json.loads(f.read())

        lst = []
        for el in data:
            lst.append(data[el][5] * data[el][6])
        lst = sorted(lst)[-n:]

        popular = dict()
        for el in data:
            if data[el][5] * data[el][6] in lst:
                popular[el] = data[el]

        with open(f"./../files/song_profiles-popular{n}.json", "w") as f:
            f.write(json.dumps(popular, indent=4))


if __name__ == "__main__":
    PopularSongProcessing.generate_n_popular(100)