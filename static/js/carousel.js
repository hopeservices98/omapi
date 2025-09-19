document.addEventListener('DOMContentLoaded', function() {
    const slidesContainer = document.getElementById('slides');
    const slides = document.querySelectorAll('.slide');
    const bulletsContainer = document.getElementById('bullets');
    const bullets = document.querySelectorAll('.bullet');
    let currentIndex = 0;
    let slideInterval;

    function showSlide(index) {
        if (index >= slides.length) {
            currentIndex = 0;
        } else if (index < 0) {
            currentIndex = slides.length - 1;
        } else {
            currentIndex = index;
        }
        slidesContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
        bullets.forEach((bullet, i) => {
            if (i === currentIndex) {
                bullet.classList.add('active');
            } else {
                bullet.classList.remove('active');
            }
        });
    }

    function nextSlide() {
        showSlide(currentIndex + 1);
    }

    function startSlideShow() {
        slideInterval = setInterval(nextSlide, 5000); // Change slide every 5 seconds
    }

    function stopSlideShow() {
        clearInterval(slideInterval);
    }

    // Add click event listeners to bullets
    bullets.forEach((bullet, index) => {
        bullet.addEventListener('click', () => {
            stopSlideShow();
            showSlide(index);
            startSlideShow();
        });
    });

    // Start slideshow on load
    startSlideShow();

    // Optional: Pause slideshow on hover
    slidesContainer.addEventListener('mouseenter', stopSlideShow);
    slidesContainer.addEventListener('mouseleave', startSlideShow);
});