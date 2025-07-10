# Mulhem (مُلهم)

Mulhem is an interactive, AI-powered storytelling platform designed for Arabic-speaking children aged 8–10. Built with Flask and integrating ALLaM (an Arabic language model by SDAIA), Mulhem helps kids learn storytelling fundamentals through AI-assisted writing, visuals, and speech.

## 🌐 Live Website

The Mulhem website is deployed on [Render](https://render.com/) and can be accessed here:

🔗 [https://mulhem.onrender.com](https://mulhem.onrender.com)

⚠️ The app is currently configured to use a local MySQL database. As a result, the live version deployed on Render will not work unless a remote database is connected. For full functionality, run the project locally with MySQL installed.


> Note: The source code is hosted on GitHub, while the live version runs on Render for full Flask server functionality.


## 🌟 Features

- ✍️ Story Generator: Generates stories based on child-provided elements.
- 📝 Independent Writing: Offers real-time AI feedback and corrections.
- 📚 Story Library: Pre-written stories children can modify and explore.
- 🖼️ Image Generation: AI-generated illustrations for stories.
- 🔊 Voice Narration: AI-based text-to-speech support.

## ⚙️ Environment

- Backend: Python, Flask
- Database: MySQL (local)
- Frontend: HTML, CSS
- Text-to-Image: Google Colab
- Text-to-Voice: ElevenLabs

## 📄 Third-Party Credits and Licenses

* Drag and Drop Question  
  © 2024 by Coran Spicer  
  [View original](https://codepen.io/cgspicer/pen/AXjZxa)

* Small Confetti Animation  
  © 2024 by Michael Hobizal  
  [View original](https://codepen.io/mikehobizal/pen/gOdmmr)

* Big Confetti Animation  
  © 2024 by Chris Coyier  
  [View original](https://codepen.io/chriscoyier/pen/vYKvEQx)

* Book Shape Animation  
  © 2024 by Timo Hausmann  
  [View original](https://codepen.io/timohausmann/pen/AaJWvo)

* Bubble Shape  
  [View original](https://codepen.io/quadbaup/pen/rKOKQv)

* Wavy Shape Generator  
  [View original](https://css-generators.com/wavy-shapes/)

* Voice Recorder  
  Used under the [MIT License](https://github.com/davidsproject/VRecorder/blob/main/LICENSE)  
  [View project](https://github.com/davidsproject/VRecorder)

* ALLaM Model  
  *M Saiful Bari et al., 2024. ALLaM: Large Language Models for Arabic and English. arXiv:2407.15390*  
  [Read paper](https://arxiv.org/abs/2407.15390)

* Dreamlike Anime 1.0  
  © dreamlike-art, used under [LICENSE]  
  [View model](https://huggingface.co/dreamlike-art/dreamlike-anime-1.0)

* Text-to-Speech  
  Powered by ElevenLabs (for demo purposes only)  
  [Website](https://elevenlabs.io/)

## 🔑 Environment Variables

> 💡 Create a .env file in the root of your project and add the following variables:

- SECRET_KEY=your-secret-key
- DB_USER=your-db-user
- DB_PASSWORD=your-db-password
- DB_HOST=localhost
- DB_NAME=mulhem
- MAIL_USERNAME=your-email@gmail.com
- MAIL_PASSWORD=your-email-app-password
- ELEVENLABS_API_KEY=your-elevenlabs-api-key
- IBM_API_KEY=your-ibm-api-key
- PROJECT_ID=your-ibm-project-id
`
## 👥 Contributors

* [Arwa Hussain Mohammad] (https://github.com/20Arwa)
* [Kholoud Othman Alzahrani] (https://github.com/kholoud-lzahrani)
* [Wejdan Riyad Alsharif] (https://github.com/wejdanxxx)
* [Eatzaz Mousa Hafiz] (https://github.com/Eatzaz-Hafiz)
``
