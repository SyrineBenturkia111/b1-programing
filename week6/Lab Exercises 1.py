# Exercise 1: Personal Music Library Manager

# Step 1: Create empty data structures
songs = []          # list to store tuples of (song_name, genre)
genre_count = {}    # dictionary to count songs per genre

print("Welcome to Music Library Manager!\n")

# Step 2: Collect 5 songs from user & store Data
for i in range(1, 6):
    print(f"Enter Song {i}:")
    name = input("Song name: ")
    genre = input("Genre: ")

    songs.append((name, genre))
    
    genre_count[genre] = genre_count.get(genre, 0) + 1
    print()

# Step 3: Display the music library
print("\n==== YOUR MUSIC LIBRARY ====")
for idx, (song, genre) in enumerate(songs, start=1):
    print(f"{idx}. {song} ({genre})")

# Step 4: Display genre statistics
print("\n==== GENRE STATISTICS ====")
for genre, count in genre_count.items():
    print(f"{genre}: {count} songs")

most_popular = max(genre_count, key=genre_count.get)
print(f"\nMost popular genre: {most_popular}")