# Welcome to Alexandria, the world's biggest library!

This project was started because I could not find a program/website that could track my reading history the way I wanted, and many times they could not find books I was reading. So I created this project instead. You start now with an empty library, but fill it up with all your beloved books on various shelves! 

Two search engines have been implemented so far, Google Books (wide variety of books, mostly in English) and Moly.hu, a Hungarian website (I always found every hungarian book there). But let me know if you want more languages!

# Quick installation

Simply clone the current repository, enter it, and then run:

```pip install .```

This will install all necessary packages and the main program. Then run `master.py`, 
and enjoy your own little library! Note that at first, you have to include two API keys for the whole thing to work:
- [Google Books API key](https://console.cloud.google.com/apis/credentials)
- [Gemini API key](https://aistudio.google.com/api-keys)

(*I haven't figured out yet how to make it in a way that you don't need this data... Sorry*)

Detailed installation guide can be found in the  [Wiki](https://github.com/LeventeOrha/Alexandria/wiki/Setup), with additional notes on useage and the Hungarian version.

# Features

- Pick the exact book you are reading, including the passing cover
- Track your starting and finishing dates
- Add new books in English or in Hungarian
- Use the system in both languages
- Chat with the AI librarian, who can manage your library for you
