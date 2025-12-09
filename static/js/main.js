document.addEventListener('DOMContentLoaded', function () {
    // Mood Selection Logic in Dashboard
    const moodBtns = document.querySelectorAll('.mood-btn');
    const moodInput = document.getElementById('mood-score');

    moodBtns.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            moodBtns.forEach(b => b.classList.remove('selected'));
            this.classList.add('selected');
            moodInput.value = this.dataset.score;
        });
    });

});
