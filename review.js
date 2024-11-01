// review.js
console.log("review.js is loading");

// Get the URL parameters
const params = new URLSearchParams(window.location.search);
const bookId = params.get('id');
console.log("Got book ID:", bookId);

// Fetch the book data from the JSON file
fetch('books.json')
    .then(response => {
        console.log("Got response from fetch:", response.status);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("Successfully parsed JSON data:", data);
        // Find the book based on the bookId
        const book = data[bookId];
        console.log("Found book:", book);
        
        if (book) {
            // Populate the HTML with book details
            document.getElementById('book-title').textContent = book.title;
            document.getElementById('author').textContent = `by ${book.author}`;
            document.getElementById('date-read').textContent = `Read on: ${book.dateRead}`;
            document.getElementById('review-text').innerHTML = book.review;
            console.log("Populated page with book details");
        } else {
            console.error('Book not found');
        }
    })
    .catch(error => {
        console.error('Error fetching the book data:', error);
    });