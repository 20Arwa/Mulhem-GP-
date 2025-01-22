# This File To Run The Server
from website import create_app # نقدر نسوي امبورت بهذا الشكل لانه اي شي داخل مجلد الويبسايت يصير عبارة عن باكج

app = create_app()

if __name__ == '__main__': # يعني ما يسوي رن للبروجمت إلا إذا سوينا رن دايركت رن لهذا الملف
    app.run(debug=True)
    