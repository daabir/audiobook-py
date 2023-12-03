import PyPDF2
import pyttsx3
import threading
import sys

class SpeakerThread(threading.Thread):
    def __init__(self, speaker, pages):
        super().__init__()
        self.speaker = speaker
        self.pages = pages
        self.stop_event = threading.Event()
    
    def run(self):
        for page_num in range(len(self.pages)):
            if self.stop_event.is_set():
                break
            text = self.pages[page_num].extract_text()
            self.speaker.say(text)
            self.speaker.runAndWait()
    
    def stop(self):
        self.stop_event.set()

def listen_for_stop(speaker_thread):
    input("Press Enter to stop..")
    speaker_thread.stop()

def main():
    book = input('Please enter the name of the book you want to be played(eg. "book.pdf"):\t')
    pdfReader = PyPDF2.PdfReader(open(book,'rb'))
    speaker = pyttsx3.init()

    prompt = input('Do you want to:\n\t 1. start listening to the book right away or\n\t 2. just have the audio file created?\n')

    if (prompt=="1"):
        speaker_thread = SpeakerThread(speaker, pdfReader.pages)
        speaker_thread.start()
        
        stop_thread = threading.Thread(target=listen_for_stop, args=(speaker_thread,))
        stop_thread.start()
        # stop_thread.join()
        # speaker_thread.join()
    else:
        full_text = ""
        for page_num in range(len(pdfReader.pages)):
            full_text += pdfReader.pages[page_num].extract_text()
        
        speaker.save_to_file(full_text, 'audio.mp3')
        speaker.runAndWait()
    
    speaker.stop()

if __name__ == "__main__":
    main()