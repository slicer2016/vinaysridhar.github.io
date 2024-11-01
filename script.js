// script.js

// Function to fetch and display the book reviews
fetch('books.json')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(books => {
        console.log("Fetched books.json data:", books); // Log the fetched data
        const bookList = document.getElementById('book-list');

        // Clear any existing content
        bookList.innerHTML = '';

        // Loop through each book and create an entry
        books.forEach((book, index) => {
            console.log("Processing book:", book); // Log each book being processed
            const bookItem = document.createElement('div');
            bookItem.className = 'book-item';
            bookItem.innerHTML = `<h2><a href="review.html?id=${index}">${book.title}</a></h2><p>by ${book.author}</p>`;
            bookList.appendChild(bookItem);
        });
    })
    .catch(error => {
        console.error('Error fetching the book data:', error);
    });
