from typing import List, Dict, Optional, Set
from dataclasses import dataclass

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.genre = None

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.genre = word
    
    def search_prefix(self, prefix: str) -> List[str]:
        node = self.root
        results = []
        
        # Traverse to the last node of the prefix
        for char in prefix.lower():
            if char not in node.children:
                return results
            node = node.children[char]
        
        # Use DFS to find all words with the prefix
        self._dfs(node, results)
        return results
    
    def _dfs(self, node: TrieNode, results: List[str]) -> None:
        if node.is_end:
            results.append(node.genre)
        for child in node.children.values():
            self._dfs(child, results)

@dataclass
class Movie:
    title: str
    year: int
    rating: float
    director: str
    description: str
    genres: Set[str]
    box_office: float  # in millions of dollars
    oscar_wins: int
    oscar_nominations: int

class MovieRecommender:
    def __init__(self):
        self.movies: Dict[str, Movie] = {}
        self.genres_trie = Trie()
        self.genres: Dict[str, Set[str]] = {}
        self._load_data()
    
    def _load_data(self) -> None:
        """Initialize with sample movie data"""
        sample_movies = {
            "The Shawshank Redemption": Movie(
                "The Shawshank Redemption",
                1994,
                9.3,
                "Frank Darabont",
                "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
                {"Drama"},
                58.8,  # Box office in millions
                0,     # Oscar wins
                7      # Oscar nominations
            ),
            "The Dark Knight": Movie(
                "The Dark Knight",
                2008,
                9.0,
                "Christopher Nolan",
                "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
                {"Action", "Crime", "Drama"},
                1004.6,  # Box office in millions
                2,       # Oscar wins
                8        # Oscar nominations
            ),
            "Pulp Fiction": Movie(
                "Pulp Fiction",
                1994,
                8.9,
                "Quentin Tarantino",
                "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
                {"Crime", "Drama"},
                213.9,   # Box office in millions
                1,       # Oscar wins
                7        # Oscar nominations
            ),
            "The Hangover": Movie(
                "The Hangover",
                2009,
                7.7,
                "Todd Phillips",
                "Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing.",
                {"Comedy"},
                469.3,   # Box office in millions
                0,       # Oscar wins
                0        # Oscar nominations
            ),
            "Titanic": Movie(
                "Titanic",
                1997,
                7.9,
                "James Cameron",
                "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
                {"Drama", "Romance"},
                2201.6,  # Box office in millions
                11,      # Oscar wins
                14       # Oscar nominations
            ),
            "The Godfather": Movie(
                "The Godfather",
                1972,
                9.2,
                "Francis Ford Coppola",
                "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                {"Crime", "Drama"},
                245.1,   # Box office in millions
                3,       # Oscar wins
                11       # Oscar nominations
            ),
            "Avengers: Endgame": Movie(
                "Avengers: Endgame",
                2019,
                8.4,
                "Anthony and Joe Russo",
                "After the devastating events of Infinity War, the universe is in ruins. The Avengers assemble once more to reverse Thanos' actions and restore balance to the universe.",
                {"Action", "Adventure", "Drama"},
                2797.5,  # Box office in millions
                0,       # Oscar wins
                1        # Oscar nominations
            ),
            "Parasite": Movie(
                "Parasite",
                2019,
                8.6,
                "Bong Joon Ho",
                "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
                {"Drama", "Thriller"},
                258.8,   # Box office in millions
                4,       # Oscar wins
                6        # Oscar nominations
            ),
            "The Matrix": Movie(
                "The Matrix",
                1999,
                8.7,
                "Lana and Lilly Wachowski",
                "A computer programmer discovers that reality as he knows it is a simulation created by machines, and joins a rebellion to break free.",
                {"Action", "Sci-Fi"},
                463.5,   # Box office in millions
                4,       # Oscar wins
                4        # Oscar nominations
            ),
            "Inception": Movie(
                "Inception",
                2010,
                8.8,
                "Christopher Nolan",
                "A thief who enters the dreams of others to steal their secrets is offered a chance to regain his old life in exchange for a task considered impossible.",
                {"Action", "Adventure", "Sci-Fi"},
                836.8,   # Box office in millions
                4,       # Oscar wins
                8        # Oscar nominations
            ),
            "Forrest Gump": Movie(
                "Forrest Gump",
                1994,
                8.8,
                "Robert Zemeckis",
                "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.",
                {"Drama", "Romance"},
                678.2,   # Box office in millions
                6,       # Oscar wins
                13       # Oscar nominations
            ),
            "The Grand Budapest Hotel": Movie(
                "The Grand Budapest Hotel",
                2014,
                8.1,
                "Wes Anderson",
                "A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy in the hotel's glorious years under an exceptional concierge.",
                {"Adventure", "Comedy", "Crime"},
                174.8,   # Box office in millions
                4,       # Oscar wins
                9        # Oscar nominations
            )
        }
        
        # Store movies and build genre index
        for title, movie in sample_movies.items():
            self.movies[title] = movie
            for genre in movie.genres:
                if genre not in self.genres:
                    self.genres[genre] = set()
                    self.genres_trie.insert(genre)
                self.genres[genre].add(title)
    
    def autocomplete_genre(self, prefix: str) -> List[str]:
        """Return genres that start with the given prefix"""
        return self.genres_trie.search_prefix(prefix)
    
    def get_recommendations(self, genre: str, limit: int = 5) -> List[Movie]:
        """Return movie recommendations for a given genre"""
        if genre not in self.genres:
            return []
        
        # Get all movies in the genre
        genre_movies = [self.movies[title] for title in self.genres[genre]]
        
        # Sort by different criteria
        by_rating = sorted(genre_movies, key=lambda x: x.rating, reverse=True)
        by_box_office = sorted(genre_movies, key=lambda x: x.box_office, reverse=True)
        by_oscars = sorted(genre_movies, key=lambda x: (x.oscar_wins, x.oscar_nominations), reverse=True)
        
        # Combine recommendations ensuring no duplicates
        recommendations = []
        used_titles = set()
        
        def add_unique_movies(movie_list, count):
            added = 0
            for movie in movie_list:
                if movie.title not in used_titles and added < count:
                    recommendations.append(movie)
                    used_titles.add(movie.title)
                    added += 1
                if added == count:
                    break
        
        # Add top rated
        add_unique_movies(by_rating, 2)
        # Add highest grossing
        add_unique_movies(by_box_office, 2)
        # Add most Oscar wins
        add_unique_movies(by_oscars, 2)
        
        return recommendations[:limit]
    
    def display_movie(self, movie: Movie) -> None:
        """Print formatted movie information"""
        print(f"\n{'='*50}")
        print(f"Title: {movie.title}")
        print(f"Year: {movie.year}")
        print(f"Rating: {movie.rating}/10")
        print(f"Director: {movie.director}")
        print(f"Genres: {', '.join(movie.genres)}")
        print(f"Box Office: ${movie.box_office:.1f}M")
        print(f"Oscar Wins: {movie.oscar_wins}")
        print(f"Oscar Nominations: {movie.oscar_nominations}")
        print(f"Description: {movie.description}")
        print(f"{'='*50}")
    
    def run(self) -> None:
        """Main interaction loop"""
        print("\nWelcome to the Movie Recommendation System!")
        print("Start typing a genre (e.g., action, comedy, drama)")
        
        while True:
            user_input = input("\nEnter genre prefix (or 'quit' to exit): ").strip()
            
            if user_input.lower() == 'quit':
                print("\nThank you for using the Movie Recommendation System!")
                break
            
            matching_genres = self.autocomplete_genre(user_input)
            
            if not matching_genres:
                print("No genres found starting with that prefix.")
                print("Available genres:", ", ".join(self.genres.keys()))
                continue
            
            print("\nMatching genres:")
            for i, genre in enumerate(matching_genres, 1):
                print(f"{i}. {genre}")
            
            if len(matching_genres) == 1:
                genre_choice = matching_genres[0]
            else:
                while True:
                    choice = input("\nSelect a genre number (or press Enter to try again): ")
                    if not choice:
                        break
                    try:
                        idx = int(choice) - 1
                        if 0 <= idx < len(matching_genres):
                            genre_choice = matching_genres[idx]
                            break
                        else:
                            print("Invalid selection. Please try again.")
                    except ValueError:
                        print("Please enter a valid number.")
                
                if not choice:
                    continue
            
            recommendations = self.get_recommendations(genre_choice)
            if recommendations:
                print(f"\nTop recommendations for {genre_choice}:")
                for movie in recommendations:
                    self.display_movie(movie)
            else:
                print(f"\nNo movies found for genre: {genre_choice}")

if __name__ == "__main__":
    recommender = MovieRecommender()
    recommender.run()