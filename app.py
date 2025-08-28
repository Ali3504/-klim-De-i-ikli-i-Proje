# İçe Aktarma
from flask import Flask, render_template, request, redirect, url_for
import os
#from model import get_class

app = Flask(__name__)

def result_calculate(arac, gd, dus, verimlilik):
    # Elektrikli cihazların enerji tüketimini hesaplamaya olanak tanıyan değişkenler
    home_coef = 100
    light_coef = 0.04
    duss_coef = 5   
    return arac * home_coef + gd * light_coef + dus * duss_coef 

# İlk sayfa
@app.route('/')
def index():
    return render_template('index.html')
# İkinci sayfa
@app.route('/<arac>')
def gd(arac):
    return render_template(
                            'gd.html', 
                            arac=arac
                           )

# Üçüncü sayfa
@app.route('/<arac>/<gd>')
def dus(arac, gd):
    return render_template(
                            'dus.html',                           
                            arac = arac, 
                            gd = gd                           
                            )
@app.route('/<arac>/<gd>/<dus>')
def soru(arac, gd, dus):
    return render_template(
                            'soru.html',                           
                            arac = arac, 
                            gd = gd,
                            dus = dus                           
                            )

# Hesaplama
@app.route('/<arac>/<gd>/<dus>/<verimlilik>')
def end(arac, gd, dus, verimlilik):
    return render_template('end.html', 
                            result=result_calculate(int(arac),
                                                    int(gd), 
                                                    int(dus),
                                                    int(verimlilik)
                                                    )
                        )
# Form
@app.route('/form')
def form():
    return render_template('form.html')

#Formun sonuçları
@app.route('/submit', methods=['POST'])
def submit_form():
    # Veri toplama için değişkenleri tanımlayın
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']
    date = request.form['date']

      # Verileri bir dosyaya yazma
    with open('form.txt', 'a', encoding='utf-8') as f:
        f.write(f"Name: {name}\nEmail: {email}\nAddress: {address}\nDate: {date}\n\n")
   

    # Verilerinizi kaydedebilir veya e-posta ile gönderebilirsiniz
    return render_template('form_result.html', 
                           # Değişkenleri buraya yerleştirin
                           name=name,
                           email=email,
                           address=address,
                           date=date,
                           )

# Yüklenen dosyaların kaydedileceği dizin
UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# İzin verilen dosya uzantıları
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Dosyanın izin verilen bir uzantıya sahip olup olmadığını kontrol eden fonksiyon
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/ai')
def index():
    return render_template('indexai.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Görseli model ile analiz et
       # class_name, confidence = get_class(file_path)
        
        # Sonuçları kullanıcıya göster
        #return render_template('result.html', class_name=class_name, confidence=confidence, filename=filename)

    return 'Geçersiz dosya tipi'


app.run(debug=True,port=8080)
