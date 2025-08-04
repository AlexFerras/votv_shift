link = "https://drive.google.com/file/d/1AZj8QfBOWG6GO-SAuGh_YsraBGjSyqTF/view?usp=drive_link"
fr = link.index("/d/") + 3
to = link.rindex("/")
fileId = link[fr:to]
#downloadLink = f"https://drive.google.com/uc?export=download&id={fileId}&confirm=t";
downloadLink = f"https://www.googleapis.com/drive/v3/files/{fileId}?alt=media&key=AIzaSyDVCNpmfKmJ0gPeyZ8YWMca9ZOKz0CWdgs"
import webbrowser
webbrowser.open(downloadLink)