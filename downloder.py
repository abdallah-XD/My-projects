from tkinter import *
from tkinter import filedialog
from pytube import YouTube, Playlist
from threading import Thread

root = Tk()
root.title('YouTube Downloader')
root.geometry('600x350')
root.resizable(False, False)
root.configure(bg='#164863')
def browse():
    directory = filedialog.askdirectory(title='Save Video')
    folderlink.delete(0, END)
    folderlink.insert(0, directory)

def download_yt():
    status.config(text='Status: Downloading...')
    link = yt_link.get()
    folder = folderlink.get()
    quality = quality_var.get()
    yt = YouTube(link)
    if quality == 'Highest':
        stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
    else:
        stream = yt.streams.filter(progressive=True, file_extension="mp4", res=quality).first()
    stream.download(folder)
    finish()

def download_playlist():
    status.config(text='Status: Downloading Playlist...')
    playlist_link = playlist_link_entry.get()
    folder = folderlink.get()
    quality = quality_var.get()
    pl = Playlist(playlist_link)
    for video in pl.videos:
        if quality == 'Highest':
            stream = video.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
        else:
            stream = video.streams.filter(progressive=True, file_extension="mp4", res=quality).first()
        stream.download(folder)
        finish()
def threaded_download():
    thread = Thread(target=download_yt)
    thread.start()
    download_button.config(text="Downloading...", state="disabled")

def threaded_download_playlist():
    thread = Thread(target=download_playlist)
    thread.start()
    download_playlist_button.config(text="Downloading Playlist...", state="disabled")

def finish():
    status.config(text='Status: ......Finished')

# YouTube logo
yt_logo = PhotoImage(file='youtube.png').subsample(1)
logo = Label(root, image=yt_logo)
logo.place(relx=0.5, rely=0.25, anchor='center')

# YouTube link label and entry
yt_label = Label(root, text='YouTube Link:', font=('Arial', 13, 'bold'), fg='#FFCB42', bg="#164863")
yt_label.place(x=10, y=148)
yt_link = Entry(root, width=60)
yt_link.place(x=143, y=150)

# Download folder label and entry
folder_label = Label(root, text='Download Folder:', font=('Arial', 12, 'bold'), fg='#FFCB42', bg="#164863")
folder_label.place(x=1, y=183)
folderlink = Entry(root, width=50)
folderlink.place(x=143, y=185)

# Playlist link label and entry
playlist_label = Label(root, text='Playlist Link:', font=('Arial', 13, 'bold'), fg='#FFCB42', bg="#164863")
playlist_label.place(x=10, y=218)
playlist_link_entry = Entry(root, width=60)
playlist_link_entry.place(x=143, y=220)

# Quality selection dropdown
quality_label = Label(root, text='Select Quality:', font=('Arial', 12, 'bold'), fg='#FFCB42', bg="#164863")
quality_label.place(x=10, y=258)
quality_var = StringVar(root)
quality_choices = ['Highest', '1440p', '1080p', '720p', '480p', '360p', '240p']
quality_var.set(quality_choices[0])  # set the default option
quality_menu = OptionMenu(root, quality_var, *quality_choices)
quality_menu.config(width=10, fg='#FFCB42', bg="#164863")
quality_menu.place(x=143, y=255)

# Browse button
browse_button = Button(root, text='Browse', command=browse,bg="#FFB200", fg="#06283D")
browse_button.place(x=455, y=180)

# Download buttons
download_button = Button(root, text='Download Video', command=threaded_download,bg="#FFB200", fg="#06283D")
download_button.place(x=300, y=300)
download_playlist_button = Button(root, text='Download Playlist', command=threaded_download_playlist,bg="#FFB200", fg="#06283D")
download_playlist_button.place(x=150, y=300)

# Status bar
status = Label(root, text='Status: Ready', font='calibre 12 italic', fg='#79DAE8', bg='#1A374D', anchor='w')
status.place(rely=1, anchor='sw', relwidth=1)

root.mainloop()
