document.addEventListener('DOMContentLoaded', function() {
    renderReviewCarousel();
});

function renderReviewCarousel() {
    fetch('/reviews')
    .then(response => response.json())
    .then(data => {
        reviews = document.querySelector('.reviews');
        carousel = document.querySelector('#review-carousel');
        carouselIndicators = document.querySelector('.carousel-indicators');
        if (reviews !== null) {
            for (i = 0; i < data.length; i++) {
                modelFields = data[i].fields;
                user = modelFields.user;
                description = modelFields.description;
                stars = modelFields.stars;
                reviewDiv = createReview(user, description, stars);
                reviewDiv.classList.add('carousel-item');
                indicator = createCarouselIndicator(carousel, i);
                if (i == 0) {
                    btn.classList.add('active');
                    reviewDiv.classList.add('active');
                }
                reviews.appendChild(reviewDiv);
                carouselIndicators.appendChild(indicator);
            }
        }
    });
}

function createReview(user, description, stars) {
    reviewDiv = document.createElement('div');
    reviewDiv.classList.add('review');

    userSpan = document.createElement('span');
    descriptionPara = document.createElement('p');
    starsSpan = document.createElement('span');
    userSpan.textContent = user;
    descriptionPara.textContent = description;
    starsSpan.textContent = createStarRating(stars);

    reviewDiv.append(userSpan, descriptionPara, starsSpan);
    return reviewDiv
}

function createCarouselIndicator(carousel, slideNumber) {
    btn = document.createElement('button');
    btn.dataset.bsTarget = `#${carousel.id}`;
    btn.dataset.bsSlideTo = slideNumber;
    return btn;
}

function createStarRating(starCount) {
    switch (starCount) {
        case 1:
            return '★☆☆☆☆'
        case 2:
            return '★★☆☆☆'
        case 3:
            return '★★★☆☆'
        case 4:
            return '★★★★☆'
        case 5:
            return '★★★★★'
    }
}