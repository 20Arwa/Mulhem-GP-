// collect DOMs
const display = document.querySelector('.display-voice-record')
const controllerWrapper = document.querySelector('.controllers-voice-record')

const State = ['Initial', 'Record', 'Download']
let stateIndex = 0
let mediaRecorder, chunks = [], audioURL = ''

// mediaRecorder setup for audio
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
    console.log('mediaDevices supported..')

    navigator.mediaDevices.getUserMedia({
        audio: true
    }).then(stream => {
        mediaRecorder = new MediaRecorder(stream)

        mediaRecorder.ondataavailable = (e) => {
            chunks.push(e.data)
        }

        mediaRecorder.onstop = () => {
            const blob = new Blob(chunks, {'type': 'audio/ogg; codecs=opus'})
            chunks = []
            audioURL = window.URL.createObjectURL(blob)
            document.querySelector('audio').src = audioURL

        }
    }).catch(error => {
        console.log('Following error has occured : ',error)
    })
}else{
    stateIndex = ''
    application(stateIndex)
}

const clearDisplay = () => {
    display.textContent = ''
}

const clearControls = () => {
    controllerWrapper.textContent = ''
}
const record = () => {
    if (stateIndex === 2) { // Check if we're in the "Download" state
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

const downloadAudio = () => {
    const downloadLink = document.createElement('a')
    downloadLink.href = audioURL
    downloadLink.setAttribute('download', 'audio')
    downloadLink.click()
}

const addButton = (id, funString, text) => {
    const btn = document.createElement('button');
    btn.id = id;
    btn.setAttribute('onclick', funString);
    // إنشاء الأيقونة
    const icon = document.createElement('i');
    icon.className = 'fa-solid fa-microphone mic-icon'; // تعيين الفئات للأيقونة
    // إضافة الأيقونة أولاً
    btn.appendChild(icon);
    // إضافة النص بعد الأيقونة
    const textNode = document.createTextNode(text);
    btn.appendChild(textNode);
    // إضافة الزر إلى العنصر المطلوب
    controllerWrapper.append(btn);
};



const addMessage = (text) => {
    const msg = document.createElement('p')
    msg.textContent = text
    display.append(msg)
}

const addAudio = () => {
    const audio = document.createElement('audio')
    audio.controls = true
    audio.src = audioURL
    display.append(audio)
}

const application = (index) => {
    switch (State[index]) {
        case 'Initial':
            clearDisplay()
            clearControls()

            addButton('record', 'record()', 'سجل القصة بصوتك')
            break;

        case 'Record':
            clearDisplay()
            clearControls()

            addMessage('يتم التسجيل...')
            addButton('stop', 'stopRecording()', 'أوقف التسجيل')
            break

        case 'Download':
            clearControls()
            clearDisplay()

            addAudio()
            addButton('record', 'record()', 'سجل مرة أخرى')
            break

        default:
            clearControls()
            clearDisplay()

            addMessage('المتصفح الخاص بك لا يدعم هذه الخاصية')
            break;
    }

}

application(stateIndex)

// Copyright https://github.com/davidsproject/VRecorder