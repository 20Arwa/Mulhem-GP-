// Make Flash Message Dissapear After Seconds
  setTimeout(() => {
    const flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
      flashMessages.style.transition = "opacity 0.5s ease"; // تأثير اختفاء سلس
      flashMessages.style.opacity = "0"; // اجعل الرسائل شفافة
      setTimeout(() => flashMessages.remove(), 500); // أزل الرسائل من DOM بعد اختفائها
    }
}, 3000); // 5000 ميلي ثانية (5 ثوانٍ)


// Drag And Drop Quiz
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

                        // Remove Animation From Buttons
                        quizWrapper.querySelectorAll(".drag-options button").forEach(btn => {
                            btn.style.animation = "none"; // يوقف الأنيميشن فقط عن الخيارات في نفس السؤال
                        });

                        
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
                        targetEle.style.background = "var(--gradient-button)"; // Change background
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


const arabicRegex = /^[\u0600-\u06FF\s.,،؟!:؛()«»"'\-—_…\[\]{}<>*+\/\\|~`^%$#@&0-9\u0660-\u0669]+$/; // التحقق من ان النص عربي
const symbolsRegex = /[\u0600-\u06FF]/; // التحقق من أن النص يحتوي على أحرف مفهومة وليس رموزًا فقط
const gibberishPattern = /^[^a-zA-Z0-9\u0600-\u06FF\s]+$/; // نص غير مفهوم
const repeatedPattern = /(.)\1{2,}/; // حرف مكرر أكثر من مرتين


// Forbidden Words
// قائمة الكلمات السيئة
const forbiddenWords = [
    "كافر", "متخلف", "إرهابي", "عنصري", "فاشل", "قذر", "ملعون", 
    "زفت", "الله يلعنك", "الله يقلعك", "منافق", "منحرف", "زق", 
    "كل زق", "خرا", "كل خرا", "خسيس", "سافل", "منحط","الخرا","الزق"
];
// دالة للتحقق من الكلمات السيئة
function checkForbiddenWords(text) {
    // البحث عن الكلمة المحظورة المستخدمة في النص
    const foundWord = forbiddenWords.find((word) => text.includes(word));
    // إذا وجدت كلمة ممنوعة
    if (foundWord) {
        Swal.fire({
            title: 'كلمات غير لطيفة!',
            text: `لقد استخدمت الكلمة "${foundWord}". دعنا نحاول استخدام كلمات أجمل! 😊`,
            icon: 'warning',
            confirmButtonText: 'موافق'
        });
        return true;
    }
    return false;
}



// تفعيل الشرح اللي يطلع عند الهوفر على الأزرار
document.addEventListener("DOMContentLoaded", () => {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
});

// تفعيل الشرح اللي يطلع عند الضغط على الأزرار
document.addEventListener('DOMContentLoaded', function () {
    // تهيئة كل عناصر الـ popover في الصفحة
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        var popover = new bootstrap.Popover(popoverTriggerEl);

        // إضافة حدث عند النقر لإخفاء البوبوفر بعد ثوانٍ
        popoverTriggerEl.addEventListener('click', function () {
            setTimeout(function () {
                popover.hide(); // إخفاء البوبوفر
            }, 3000); // 3000 مللي ثانية = 3 ثوانٍ
        });

        return popover;
    });
});



