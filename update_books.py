import json

def count_words(text):
    return len(text.split())

# Load the JSON data
with open('books.json', 'r') as f:
    books = json.load(f)

# Filter books
filtered_books = [
    book for book in books 
    if book['category'] != 'Fiction' 
    and 'review' in book 
    and book['review'] 
    and count_words(book['review']) >= 200
]

# Sort by date read (if available)
filtered_books.sort(key=lambda x: x.get('dateRead', ''), reverse=True)

# Write the filtered data back to a new file
with open('books_filtered.json', 'w') as f:
    json.dump(filtered_books, f, indent=4)

# Print statistics
print(f"Original number of books: {len(books)}")
print(f"Number of books after filtering: {len(filtered_books)}")
print("\nRemoved books:")
print(f"Fiction books: {sum(1 for book in books if book['category'] == 'Fiction')}")
print(f"Short reviews: {sum(1 for book in books if book['category'] != 'Fiction' and 'review' in book and book['review'] and count_words(book['review']) < 200)}")