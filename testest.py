num = 5

search_tracks_dict = {
    1: "Track One",
    2: "Track Two",
    3: "Track Three",
    4: "Track Four",
    5: "Track Five",
}

for track_id, track_name in list(search_tracks_dict.items())[:num]:
    print(track_id)
    print(track_name)
