from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load dataset and model
dataset = pd.read_csv("dataset/stud.csv")
model = joblib.load("model .pkl")  # Ensure no space in the file name

# Label encoders for input transformation
label_encoders = {col: LabelEncoder().fit(dataset[col]) for col in dataset.columns if dataset[col].dtype == 'object'}

# Career descriptions
# Career descriptions
career_descriptions = {
    "Animation, Graphics and Multimedia": "A field focusing on creating visual content, animations, and multimedia presentations for entertainment, advertising, and education.",
    "B.Arch- Bachelor of Architecture": "A professional degree in architecture that equips students with the skills to design buildings and structures.",
    "B.Com- Bachelor of Commerce": "A foundational degree in commerce, focusing on accounting, finance, and business management.",
    "B.Ed.": "A professional teaching degree for individuals aspiring to become educators in schools.",
    "B.Sc- Applied Geology": "A science degree focused on the study of Earth's materials, processes, and history.",
    "B.Sc- Nursing": "A healthcare degree focusing on patient care, clinical practices, and medical ethics.",
    "B.Sc. Chemistry": "A degree exploring the properties, composition, and changes of matter at a molecular level.",
    "B.Sc. Mathematics": "An advanced study in mathematical theories, computations, and problem-solving techniques.",
    "B.Sc.- Information Technology": "A degree focusing on the application of IT in managing data, software, and systems.",
    "B.Sc.- Physics": "An exploration of the fundamental laws of nature, including matter, energy, and their interactions.",
    "B.Tech.-Civil Engineering": "An engineering degree focused on designing, constructing, and maintaining infrastructure projects.",
    "B.Tech.-Computer Science and Engineering": "A technical degree in programming, software development, and computer systems.",
    "B.Tech.-Electrical and Electronics Engineering": "A branch of engineering dealing with electrical systems, circuits, and power distribution.",
    "B.Tech.-Electronics and Communication Engineering": "An engineering degree focused on electronic devices, circuits, and communication technologies.",
    "B.Tech.-Mechanical Engineering": "A branch of engineering dealing with the design, construction, and operation of machinery.",
    "BA in Economics": "A social science degree exploring economic theories, policies, and their applications in society.",
    "BA in English": "A humanities degree focusing on English literature, language, and writing skills.",
    "BA in Hindi": "A degree in the Hindi language and literature, exploring its cultural and linguistic significance.",
    "BA in History": "A study of past events, civilizations, and their impact on the present and future.",
    "BBA- Bachelor of Business Administration": "A management degree focusing on business operations, leadership, and entrepreneurship.",
    "BBS- Bachelor of Business Studies": "A business-focused degree emphasizing strategic management and decision-making.",
    "BCA- Bachelor of Computer Applications": "A technical degree specializing in computer programming and application development.",
    "BDS- Bachelor of Dental Surgery": "A professional healthcare degree specializing in dental and oral health.",
    "BEM- Bachelor of Event Management": "A professional degree focusing on planning and organizing events and functions.",
    "BFD- Bachelor of Fashion Designing": "A creative degree focusing on designing clothing, accessories, and fashion trends.",
    "BJMC- Bachelor of Journalism and Mass Communication": "A professional degree in media, journalism, and mass communication practices.",
    "BPharma- Bachelor of Pharmacy": "A healthcare degree specializing in drug development, usage, and patient care.",
    "BTTM- Bachelor of Travel and Tourism Management": "A professional degree in managing travel, tourism, and hospitality industries.",
    "BVA- Bachelor of Visual Arts": "A creative degree focusing on painting, sculpture, and other visual arts.",
    "CA- Chartered Accountancy": "A professional certification focusing on financial accounting, auditing, and taxation.",
    "CS- Company Secretary": "A professional qualification in corporate law, governance, and compliance.",
    "Civil Services": "A prestigious career in public administration, governance, and policy implementation.",
    "Diploma in Dramatic Arts": "A professional course in acting, direction, and theatrical production.",
    "Integrated Law Course- BA + LL.B": "A dual degree in law and humanities, preparing students for a career in legal practice.",
    "MBBS": "A professional medical degree equipping students to become licensed doctors."
}


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommender.html", methods=["GET", "POST"])
def recommender():
    if request.method == "POST":
        try:
            # Collect user inputs from the form
            user_inputs = {feature: int(request.form.get(feature, 0)) for feature in dataset.columns[:-1]}
            user_df = pd.DataFrame([user_inputs])

            # Ensure column alignment
            missing_cols = set(dataset.columns[:-1]) - set(user_df.columns)
            for col in missing_cols:
                user_df[col] = 0

            # Predict career path
            prediction = model.predict(user_df)
            predicted_course = label_encoders['Courses'].inverse_transform([prediction[0]])[0]

            return redirect(url_for("results", result=predicted_course))
        except Exception as e:
            return f"Error in recommender: {e}"
    return render_template("/recommender.html", features=dataset.columns[:-1])

@app.route("/personality.html", methods=["GET", "POST"])
def personality():
    holland_questions = {
        "R": ["I enjoy working with machines and tools.", "I like practical tasks over abstract ones."],
        "I": ["I enjoy solving puzzles and brain teasers.", "I like conducting experiments."],
        "A": ["I enjoy drawing, painting, or creating visual art.", "I like writing poetry or stories."],
        "S": ["I enjoy helping people solve their problems.", "I enjoy teaching and educating others."],
        "E": ["I enjoy leadership roles and responsibilities.", "I like persuading others."],
        "C": ["I prefer working with numbers and data.", "I enjoy record-keeping and organizing."]
    }
    if request.method == "POST":
        try:
            scores = {ptype: sum([int(request.form.get(f"{ptype}_{i}", 0)) for i in range(len(questions))])
                      for ptype, questions in holland_questions.items()}
            dominant_personality = max(scores, key=scores.get)
            return redirect(url_for("results", result=dominant_personality))
        except Exception as e:
            return f"Error in personality: {e}"
    return render_template("/personality.html", questions=holland_questions)

@app.route("/results")
def results():
    result = request.args.get("result", "No result")
    description = career_descriptions.get(result, "No description available for this career.")
    return render_template("results.html", result=result, description=description)

if __name__ == "__main__":
    app.run(debug=True)
