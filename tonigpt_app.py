# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, send_file, redirect, url_for
from tonigpt import tonigpt
from pathlib import Path
import os
import json
from dotenv import load_dotenv
import threading

app = Flask(__name__)

load_dotenv()

# Pfad zum Verzeichnis mit den MP3-Dateien
story_storage = os.getenv("STORIES_DIR")
#mp3_directory = Path('./stories')


# Definiere die Dropdown-Optionen für das Genre und die Keywords
genre_options = [
    "Detektivgeschichte",
    "Geschichte zum Zählen zu lernen",
    "Abenteuergeschichte",
    "pädagogisch wertvolle Geschichte",
    "Geschichte im Reimform", 
    "Spaßgeschichte",
    "Märchengeschichte", 
    "Historische Geschichte",
    "Gute Nacht Geschichte",
]

keywords_options = [
    "Mama", "Papa", "Kinder", "Kindergarten", "Feuerwehr", "Schwimmbad",
    "Essen", "Sommer", "Winter", "Regen", "Schnee", "Polizei", "Urlaub", "Einhorn", "Pferd", "Hund", "Katze",
    "Zoowärter", "Zoo", "Bauernhof", "Bauer", "Bäuerin", "Kuh", "Schwein", "Huhn", "Hase", "Oma", "Opa", "Schule",
    "Pony", "Doktor", "Krankenwagen"
]


voice_options = [
    "Alloy", "Echo", "Fable", "Onyx", "Nova", "Shimmer"
]



def get_full_path_if_filename_in_list(filename:str, filelist:list, mp3_directory:Path)->str:
    if filename in filelist:
        #filename_with_path = mp3_directory.joinpath(filename)
        filename_with_path = f"{mp3_directory}/{filename}"
        #print(f"filename_with_path: {filename_with_path}")
        return filename_with_path
    return None


def get_tonigpt_files(mp3_directory:Path)->dict:
        
    mp3_files = [f for f in os.listdir(mp3_directory) if f.endswith('.mp3')]
    txt_files = [f for f in os.listdir(mp3_directory) if f.endswith('.txt')]
    meta_files = [f for f in os.listdir(mp3_directory) if f.endswith('.json')]

    return_dict = {}
    for file in mp3_files:
        print(f"File: {file}")
        file_name_stem = file.split(".")[0]
        print(f"file_number: {file_name_stem}")
        
        mp3_file = file
        text_file = get_full_path_if_filename_in_list(f"{file_name_stem}.txt", txt_files, mp3_directory)    
        meta_file = get_full_path_if_filename_in_list(f"{file_name_stem}.json", meta_files, mp3_directory)    
        return_dict[file_name_stem] = {"mp3": mp3_file, "txt": text_file, "meta": meta_file}   
    return return_dict

def load_json(outfn)->dict:
    with open(str(outfn)) as f:
        data = json.load(f)
        return data


@app.route('/', methods=['GET', 'POST'])
def index():
    mp3_file = None

    if request.method == 'POST':
        # Hole die eingegebenen Werte aus dem Formular
        alter_von = int(request.form['alter_von'])
        alter_bis = int(request.form['alter_bis'])
        wortlimit = int(request.form['wortlimit'])
        genre = request.form['genre']
        voice = request.form['voice']

        # Hole die Keywords aus dem Formular (variable Anzahl)
        keywords = []
        for i in range(1, 10):  # Hier könnten bis zu 9 Keywords hinzugefügt werden (kann angepasst werden)
            keyword = request.form.get(f'keyword_{i}')
            if keyword:
                keywords.append(keyword)

        # Run create_story function as a thread
        thread = threading.Thread(target=create_story, args=({
            'alter_von': alter_von,
            'alter_bis': alter_bis,
            'wortlimit': wortlimit,
            'genre': genre,
            'keywords': keywords, 
            'voice': voice
        },))
        thread.start()

        # Weiterleiten zur Erfolgsseite oder zur gleichen Seite
        # Hier kannst du entscheiden, wohin du nach dem Absenden des Formulars weiterleiten möchtest

    # Wenn es ein GET-Request ist, zeige das Formular an
    toni_files_dict = get_tonigpt_files(story_storage)
    toni_files_dict_sorted = dict(sorted(toni_files_dict.items(), reverse=True))

    # Lese den Inhalt der 'meta'-Datei und füge ihn zum Dictionary hinzu
    for key, value in toni_files_dict_sorted.items():
        meta_content = None
        if value['meta']:
            # TODO umstellen und request oder ähnliches statt webdav download verwenden (am besten async)
            #meta_dict = _get_meta_json_content(Path(value['meta']).name)
            meta_dict = load_json(value['meta'])
            if meta_dict.get('keywords'):
                value['keywords'] = meta_dict.get('keywords')
            if meta_dict.get('genre'):
                value['genre'] = meta_dict.get('genre')
            if meta_dict.get('age'):    
                value['age'] = meta_dict.get('age') 
            if meta_dict.get('wordlimit'):    
                value['wordlimit'] = meta_dict.get('wordlimit')
            if meta_dict.get('voice'):    
                value['voice'] = meta_dict.get('voice')
            if meta_dict.get('prompt'):
                value['prompt'] = meta_dict.get('prompt')                

    return render_template('formular.html', genre_options=genre_options, voice_options=voice_options, keywords_options=keywords_options, toni_files_dict=toni_files_dict_sorted)

@app.route('/play/<filename>')
def play(filename):
    # Den Pfad zur ausgewählten MP3-Datei erstellen
    file_path = os.path.join(story_storage, filename)
    # Die MP3-Datei abspielbar machen
    return send_file(file_path)

@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    # Den Pfad zur ausgewählten MP3-Datei erstellen
    mp3_file = Path(os.path.join(story_storage, filename))
    txt_file = mp3_file.parent.joinpath(Path(mp3_file).stem + ".txt")
    json_file = mp3_file.parent.joinpath(Path(mp3_file).stem + ".json")

    try:
        # Stroyfiles löschen
        os.remove(str(mp3_file))
        os.remove(str(txt_file))
        os.remove(str(json_file))
    except OSError as e:
        # Fehlerbehandlung, wenn die Datei nicht gelöscht werden kann
        print("Error:", e)
    return redirect(url_for('index'))


def create_story(form_data:dict)->Path:
    # Hier kannst du die Daten aus dem Formular verarbeiten
    # Hier als Beispiel, wie du sie ausdrucken könntest:
    age = (form_data.get("alter_von"), form_data.get("alter_bis"))
    wordlimit = form_data.get("wortlimit")
    keywords = form_data.get("keywords")
    genre = form_data.get("genre")
    voice = form_data.get("voice")
    story_path = Path(story_storage)
    mp3_file = tonigpt(keywords, genre, age, wordlimit, voice, story_path, os.getenv("OPENAI_API_KEY"))
    return mp3_file

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)