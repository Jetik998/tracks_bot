def words_similarity(base, target, threshold=0.6):
    base_words = base.lower().split()
    target_words = target.lower().split()

    matches = sum(1 for w in base_words if w in target_words)
    similarity = matches / len(base_words)

    return similarity >= threshold

track_name = "Adam Ten"
found_text = "Adam Ten & Rhye - 3 Days Later"

if words_similarity(track_name, found_text):
    print("Совпадение по словам найдено")
else:
    print("Совпадение не найдено")

