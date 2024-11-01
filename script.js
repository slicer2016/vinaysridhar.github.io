// script.js
document.addEventListener('DOMContentLoaded', function() {
    // Fetch and display the book reviews
    fetch('books.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(books => {
            const bookList = document.getElementById('book-list');
            
            // Clear any existing content
            bookList.innerHTML = '';
            
            // Loop through each book and create an entry
            books.forEach((book, index) => {
                const li = document.createElement('li');
                
                const link = document.createElement('a');
                link.href = `review.html?id=${index}`;
                link.className = 'book-link';
                link.textContent = book.title;
                
                const date = document.createElement('span');
                date.className = 'date';
                date.textContent = book.dateRead || '';
                
                li.appendChild(link);
                li.appendChild(date);
                bookList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            const bookList = document.getElementById('book-list');
            bookList.innerHTML = '<li>Error loading books</li>';
        });
});