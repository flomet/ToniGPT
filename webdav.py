# -*- coding: utf-8 -*-

from webdav3.client import Client

from pathlib import Path
import os
from dotenv import load_dotenv

def get_client()->Client:
    
    load_dotenv()

    # Verbindung zum WebDAV-Server herstellen
    options = {
        'webdav_hostname': os.getenv('WEBDAV_SERVER'),
        'webdav_login': os.getenv('WEBDDAV_USER'),
        'webdav_password': os.getenv('WEBDAV_PASSWORD')
    }
    client = Client(options)
    return client

def copy_file_to_webdav(local_file:Path)->None:
    remote_file = f"{local_file.name}"
    client = get_client()
    client.upload(remote_file, local_file)

def copy_file_to_server(local_file:Path)->None:
    copy_file_to_webdav(local_file)


# Herunterladen der Datei vom WebDAV-Server
def download_file_from_server(remote_path:str, local_path:str)->Path:
    client = get_client()
    #client.download(remote_path, local_path)
    print(f"Download {remote_path} to {local_path}")
    client.download_sync(remote_path=remote_path, local_path=local_path)
    return local_path


def get_full_path_if_filename_in_list_old(filename:str, filelist:list, webdav_server:str)->str:
    if filename in filelist:
        filename_with_path = f"{webdav_server}{filename}"
        #print(f"filename_with_path: {filename_with_path}")
        return filename_with_path
    return None

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
        file_number = file.split(".")[0]
        print(f"file_number: {file_number}")
        
        mp3_file = file
        text_file = get_full_path_if_filename_in_list(f"{file_number}.txt", txt_files, mp3_directory)    
        meta_file = get_full_path_if_filename_in_list(f"{file_number}.json", meta_files, mp3_directory)    
        return_dict[file_number] = {"mp3": mp3_file, "txt": text_file, "meta": meta_file}   
    return return_dict

# Funktion zum Abrufen der Dateien aus dem WebDAV-Speicher
def get_tonigpt_files_old()->dict:
    client = get_client()
    client.verify = False  # Falls der Server kein gültiges SSL-Zertifikat hat
    filelist = client.list('')  # Passe den Pfad entsprechend an

    webdav_server = os.getenv('WEBDAV_SERVER')
    filelist_with_path = [f"{webdav_server}{file}" for file in filelist]

    filelist_with_path.sort()
    
    return_dict = {}
    for file in filelist_with_path:
        file_number = file.replace(webdav_server, "").split(".")[0].replace("/", "")
        if not file_number in return_dict:
            mp3_file  = get_full_path_if_filename_in_list(f"{file_number}.mp3", filelist, webdav_server)
            text_file = get_full_path_if_filename_in_list(f"{file_number}.txt", filelist, webdav_server)    
            meta_file = get_full_path_if_filename_in_list(f"{file_number}.json", filelist, webdav_server)    
            return_dict[file_number] = {"mp3": mp3_file, "txt": text_file, "meta": meta_file}    
    return return_dict

if __name__ == "__main__":
    test_file = Path(os.getcwd()).joinpath("stories").joinpath("17.txt")
    if not test_file.exists():
        print(f"File {test_file} does not exist")
    else: 
        #copy_file_to_server(test_file)
        pass
    print(get_tonigpt_files())