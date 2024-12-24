document.addEventListener('DOMContentLoaded', function () {
    // Select all quiz wrappers (for multiple questions)
    const quizWrappers = document.querySelectorAll('.quiz-wrapper');

    quizWrappers.forEach(function (quizWrapper) {
        const answersLeft = [];
        const options = quizWrapper.querySelectorAll('li.option');

        options.forEach(function (option) {
            const answerValue = option.getAttribute('data-target');
            const target = quizWrapper.querySelector('.answers .target[data-accept="' + answerValue + '"]');
            const labelText = option.innerHTML;

            option.draggable = true; // Make option draggable

            option.addEventListener('dragstart', function (event) {
                event.dataTransfer.setData('text/plain', answerValue);
            });

            if (target) {
                // Make target droppable
                target.addEventListener('dragover', function (event) {
                    event.preventDefault(); // Necessary to allow drop
                });

                target.addEventListener('drop', function (event) {
                    event.preventDefault();

                    const droppedValue = event.dataTransfer.getData('text/plain');
                    const targetEle = target;

                    // If Answer Is Correct
                    if (droppedValue === answerValue) {
                        // Play Right Answer Sound
                        const audio = document.getElementById('confetti-sound-right');
                        audio.currentTime = 0; // Reset audio to the start
                        audio.play();

                        // Confetti Class
                        setTimeout(() => {
                            targetEle.parentElement.classList.add('active'); // Spread confetti
                        }, 200);

                        // Remove Confetti Class After 2 Seconds
                        setTimeout(() => {
                            targetEle.classList.remove('active');
                        }, 1000);

                        targetEle.classList.remove("active-wrong"); // Remove wrong reaction
                        targetEle.classList.add("active-right"); // Correct reaction
                        targetEle.style.backgroundColor = "var(--main-dark)"; // Change background
                        option.draggable = false;
                        targetEle.removeEventListener('dragover', null);
                        targetEle.removeEventListener('drop', null);
                        option.innerHTML = '&nbsp;';
                        targetEle.innerHTML = labelText;

                        // Remove from answersLeft
                        const index = answersLeft.indexOf(answerValue);
                        if (index !== -1) {
                            answersLeft.splice(index, 1);
                        }
                    } else {
                        targetEle.classList.add("active-wrong"); // Wrong answer reaction
                        
                        // Play Wrong Answer Sound
                        const audio = document.getElementById('sound-wrong');
                        audio.currentTime = 0; // Reset audio to the start
                        audio.play();
                    }
                });

                answersLeft.push(answerValue);
            }
        });
    });
});
// Copyright (c) 2024 by Coran Spicer (https://codepen.io/cgspicer/pen/AXjZxa)


// Right Answer Effect 
document.querySelectorAll('.confetti-right.confetti-click').forEach(element => {
    element.addEventListener('click', function () {
        const audio = document.getElementById('confetti-sound-right');
        audio.currentTime = 0; // Return Voice To The Start
        audio.play();
        
        setTimeout(() => {
            this.classList.add('active'); // This Will Spread The Party
        }, 200);
        
        // Remove Class After 2 Seconds, So When Click Again , Effect Will Happen Again
        setTimeout(() => {
            this.classList.remove('active');
        }, 1000);
    });
});
// Copyright (c) 2024 by Michael Hobizal (https://codepen.io/mikehobizal/pen/gOdmmr)

// Wrong Answer Effect 
document.querySelectorAll('.wrong-button').forEach(element => {
    element.addEventListener('click', function () {
        const audio = document.getElementById('sound-wrong');
        audio.currentTime = 0; // Return Voice To The Start
        audio.play();
    });
});






