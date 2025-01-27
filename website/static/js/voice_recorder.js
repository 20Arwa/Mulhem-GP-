// عنصر العرض وعناصر التحكم
const display = document.querySelector('.display-voice-record');
const controllerWrapper = document.querySelector('.controllers-voice-record');

// الحالة الافتراضية
const State = ['Initial', 'Record', 'Download'];
let stateIndex = 0;
let mediaRecorder, chunks = [], audioURL = '';

// استلام البيانات من الخادم (إذا كان الصوت موجودًا)
const existingAudioSrc = display.getAttribute('data-audio-src');

// الوظيفة الرئيسية للتحكم في الواجهة
const application = (index) => {
    switch (State[index]) {
        case 'Initial':
            clearDisplay();
            clearControls();

            addButton('record', 'record()', 'سجل القصة بصوتك');
            break;

        case 'Record':
            clearDisplay();
            clearControls();

            addMessage('يتم التسجيل...');
            addButton('stop', 'stopRecording()', 'أوقف التسجيل');
            break;

        case 'Download':
            clearControls();
            clearDisplay();

            addAudio();
            addButton('record', 'record()', 'سجل مرة أخرى');
            break;

        default:
            clearControls();
            clearDisplay();

            addMessage('المتصفح الخاص بك لا يدعم هذه الخاصية');
            break;
    }
};

// الوظائف المساعدة
const clearDisplay = () => {
    display.textContent = '';
};

const clearControls = () => {
    controllerWrapper.textContent = '';
};

const addButton = (id, funString, text) => {
    const btn = document.createElement('button');
    btn.id = id;
    btn.setAttribute('onclick', funString);

    const icon = document.createElement('i');
    icon.className = 'fa-solid fa-microphone mic-icon';
    btn.appendChild(icon);

    const textNode = document.createTextNode(text);
    btn.appendChild(textNode);

    controllerWrapper.append(btn);
};

const record = () => {
    if (stateIndex === 2) { // Check if we're in the "Download" state
        // Sweet Alert
        Swal.fire({
            title: 'إعادة تسجيل الصوت',
            text: 'هل أنت متأكد أنك تريد إعادة تسجيل الصوت؟ سيؤدي هذا إلى استبدال التسجيل الحالي.',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'نعم، أعد التسجيل',
            cancelButtonText: 'إلغاء',
            reverseButtons: true, // Swaps the position of confirm and cancel buttons
        }).then((result) => {
            if (result.isConfirmed) {
                // Proceed with recording logic
                stateIndex = 1;
                mediaRecorder.start();
                application(stateIndex);
                console.log('User confirmed and recording started.');
            } else {
                console.log('User canceled.');
            }
        });
    } else {
        // If not in "Download" state, proceed directly
        stateIndex = 1;
        mediaRecorder.start();
        application(stateIndex);
    }
};

const stopRecording = () => {
    stateIndex = 2
    mediaRecorder.stop()
    application(stateIndex)
}

const addMessage = (text) => {
    const msg = document.createElement('p');
    msg.textContent = text;
    display.append(msg);
};

const addAudio = () => {
    const audio = document.createElement('audio');
    audio.controls = true;
    audio.src = audioURL;
    display.append(audio);
};

// بدء التطبيق بالحالة الافتراضية
application(stateIndex);

// التحقق إذا كان هناك صوت موجود مسبقًا
if (existingAudioSrc && existingAudioSrc !== '""') {
    audioURL = existingAudioSrc; // تعيين مصدر الصوت الحالي
    stateIndex = 2; // تحويل الحالة إلى "Download"
    application(stateIndex);
} else {
    // إذا لم يكن هناك صوت موجود، ابدأ في الحالة الافتراضية
    application(stateIndex);
}

// إعداد mediaRecorder لتسجيل الصوت
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = (e) => {
            chunks.push(e.data);
        };
        mediaRecorder.onstop = async () => {
            const blob = new Blob(chunks, { type: 'audio/ogg; codecs=opus' });
            chunks = [];
            audioURL = window.URL.createObjectURL(blob);
            try {
                const formData = new FormData();
                formData.append('audio', blob, 'recorded_audio.ogg');

                const response = await fetch('http://127.0.0.1:5000/save-recorded-audio', {
                    method: 'POST',
                    body: formData,
                });
                if (!response.ok) {
                    throw new Error('فشل الاتصال بالخادم. حاول مرة أخرى.');
                }
                const result = await response.json();
                if (result.success) {
                    console.log('تم رفع الصوت بنجاح:', result.file_path);
                    audioURL = '../../'+result.file_path;
                    application(2); // التبديل إلى حالة "Download" بعد رفع الصوت
                } else {
                    console.error('فشل رفع الصوت:', result.message);
                }
            } catch (error) {
                console.error('حدث خطأ أثناء رفع الصوت:', error);
            }
        };
    }).catch((error) => {
        console.log('حدث خطأ:', error);
    });
} else {
    stateIndex = '';
    application(stateIndex);
}









// right https://github.com/davidsproject/VRecorder