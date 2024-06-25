document.addEventListener('DOMContentLoaded', () => {
    // Загрузка фильмов на главной странице
    if (document.querySelector('.movies-grid')) {
        fetchMovies();
    }

    // Обработчик формы добавления фильма
    const form = document.getElementById('add-movie-form');
    if (form) {
        form.addEventListener('submit', addMovie);
    }
});

// Функция для получения списка фильмов
function fetchMovies() {
    fetch('api/movies')
        .then(response => response.json())
        .then(data => {
            const moviesGrid = document.querySelector('.movies-grid');
            moviesGrid.innerHTML = '';
            data.forEach(movie => {
                const movieCard = document.createElement('div');
                movieCard.className = 'movie-card';
                movieCard.innerHTML = `
                    <h2>${movie.title}</h2>
                    <p><strong>Режиссер:</strong> ${movie.director}</p>
                    <p><strong>Год:</strong> ${movie.year}</p>
                    <p><strong>Жанр:</strong> ${movie.genre}</p>
                `;
                movieCard.addEventListener('click', () => {
                    window.location.href = `details.html?id=${movie.id}`;
                });
                moviesGrid.appendChild(movieCard);
            });
        });
}

// Функция для добавления нового фильма
function addMovie(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const movieData = Object.fromEntries(formData.entries());
    fetch('api/movies', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(movieData)
    })
        .then(response => response.json())
        .then(data => {
            alert('Фильм успешно добавлен!');
            window.location.href = 'catalog.html';
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при добавлении фильма.');
        });
}
