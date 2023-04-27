import requests, json, random, os, re, math, sys
from moviepy.editor import *
from pathlib import Path
import imageio

metadata = {
    "aggressive": '''Aggressive Gaming Sport by Alex-Productions | https://www.youtube.com/channel/UCx0_M61F81Nfb-BRXE-SeVA
Music promoted by https://www.free-stock-music.com
Creative Commons Attribution 3.0 Unported License
https://creativecommons.org/licenses/by/3.0/deed.en_US''',
    "adventurous": '''Dragonquest by Alexander Nakarada | https://www.serpentsoundstudios.com
Music promoted by https://www.free-stock-music.com
Attribution 4.0 International (CC BY 4.0)
https://creativecommons.org/licenses/by/4.0/''',
    "action": '''Epic Cinematic Trailer | ELITE by Alex-Productions | https://www.youtube.com/channel/UCx0_M61F81Nfb-BRXE-SeVA
Music promoted by https://www.free-stock-music.com
Creative Commons Attribution 3.0 Unported License
https://creativecommons.org/licenses/by/3.0/deed.en_US''',
    "bizarre": '''Executioner by Alexander Nakarada | https://www.serpentsoundstudios.com
Music promoted by https://www.free-stock-music.com
Attribution 4.0 International (CC BY 4.0)
https://creativecommons.org/licenses/by/4.0/''',
    "bouncy": '''Vibin’ 53 by Peyruis | https://soundcloud.com/peyruis
Music promoted by https://www.free-stock-music.com
Creative Commons Attribution 3.0 Unported License
https://creativecommons.org/licenses/by/3.0/deed.en_US''',
    "bright": '''Vibin’ 53 by Peyruis | https://soundcloud.com/peyruis
Music promoted by https://www.free-stock-music.com
Creative Commons Attribution 3.0 Unported License
https://creativecommons.org/licenses/by/3.0/deed.en_US''',
    "calm": '''Workation by Jay Someday | https://soundcloud.com/jaysomeday
Music promoted by https://www.free-stock-music.com
Creative Commons Attribution 3.0 Unported License
https://creativecommons.org/licenses/by/3.0/deed.en_US''',
    "cool": '''Kinetics by | e s c p | https://escp-music.bandcamp.com
Music promoted by https://www.free-stock-music.com
Attribution 4.0 International (CC BY 4.0)
https://creativecommons.org/licenses/by/4.0/''',
    "criminal": '''He's Changing The Game by Darren-Curtis | https://soundcloud.com/desperate-measurez
Music promoted by https://www.free-stock-music.com
Creative Commons Attribution 3.0 Unported License
https://creativecommons.org/licenses/by/3.0/deed.en_US''',
    "dark": '''100 Seconds by Punch Deck | https://soundcloud.com/punch-deck
Music promoted by https://www.free-stock-music.com
Creative Commons Attribution 3.0 Unported License
https://creativecommons.org/licenses/by/3.0/deed.en_US''',
    "dramatic": '''Epic Cinematic Dramatic Music | Tragedy by Alex-Productions | https://www.youtube.com/channel/UCx0_M61F81Nfb-BRXE-SeVA
Music promoted by https://www.free-stock-music.com
Creative Commons Attribution 3.0 Unported License
https://creativecommons.org/licenses/by/3.0/deed.en_US''',
    "dreamy": '''How I Travel At Night by Enlia | https://enliamusic.com
Music promoted by https://www.free-stock-music.com
Creative Commons Attribution 3.0 Unported License
https://creativecommons.org/licenses/by/3.0/deed.en_US''',
    "driving": '''Paradox by | e s c p | https://escp-music.bandcamp.com
Music promoted by https://www.free-stock-music.com
Attribution 4.0 International (CC BY 4.0)
https://creativecommons.org/licenses/by/4.0/''',
    "emotional": '''Under The Sun by Keys of Moon | https://soundcloud.com/keysofmoon
Music promoted by https://www.free-stock-music.com
Attribution 4.0 International (CC BY 4.0)
https://creativecommons.org/licenses/by/4.0/''',
    "energetic": '''Aggressive Electro Cyberpunk Midtempo | Hidden by Alex-Productions | https://www.youtube.com/channel/UCx0_M61F81Nfb-BRXE-SeVA
Music promoted by https://www.free-stock-music.com
Creative Commons Attribution 3.0 Unported License
https://creativecommons.org/licenses/by/3.0/deed.en_US''',
    "epic": '''Juggernaut by Scott Buckley | https://soundcloud.com/scottbuckley
Music promoted by https://www.free-stock-music.com
Attribution 4.0 International (CC BY 4.0)
https://creativecommons.org/licenses/by/4.0/'''

}

# input decorator that calls input. If user input is "exit", and if it is, exits the program
def input(prompt):
    userInput = __builtins__.input(prompt)
    if userInput == "terminate":
        print("Hard Exit Initiated. Would you like to exit? (y/n)")
        if __builtins__.input("> ") == "y":
            print("Continuing...")
            sys.exit()
        else:
            input(prompt)
    return userInput


class Datum:
    def __init__(self, title, author, sentences, music, realTitle, imageList):
        self.title = title
        self.author = author
        self.sentences = sentences
        self.music = music
        self.realTitle = realTitle
        self.imageList = imageList
musicCredits = ""
data = []

# Get the image URL from Unsplash API
def requestImgURL(query):
    try:
        ran = random.randint(0,9)
        r = requests.get(f"https://api.unsplash.com/search/photos?query={query}&client_id={UNSPLASHKEY}&orientation=landscape")
        if r.status_code == 200:
            
            return r.json()['results'][ran]['urls']['regular']
        else:
            return None
    except:
        return None

# Remove HTML Tags with REGEX
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub(' ', text).replace('  ', ' ').replace('\n', ' ')

# Remove all characters illegal in file names
def cleanFileName(text):
    text = text.replace("/", "")
    text = text.replace("\\", "")
    text = text.replace(":", "")
    text = text.replace("*", "")
    text = text.replace("?", "")
    text = text.replace("\"", "")
    text = text.replace("<", "")
    text = text.replace(">", "")
    text = text.replace("|", "")
    return text

# Split the text into sentences using REGEX
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"


def sentenceSplit(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    if "..." in text: text = text.replace("...","<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

#Unsplash API Client ID
UNSPLASHKEY = "zPfxC4pX5v3jRMt69bPp52UnVgtHt0xNyJqJWSxuh3E"

while True:

    # Raw images    
    preProcessedImages = []

    # Get the title of the book
    title = input("What is the title of the book?\n")
    #if title == "exit" or title == "Exit" or title == "EXIT" or title == "e":
    #    break
    if requests.get("https://www.googleapis.com/books/v1/volumes?q=" + title).json()["totalItems"] == 0:
        print("Book not found. Please try again.")
        continue
    
    # Get Link to book from Google Books API
    bookLink = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + title).json()["items"][0]["selfLink"]

    # Get title of the book
    realTitle = requests.get(bookLink).json()["volumeInfo"]["title"]

    # Clean the title of the book
    title = cleanFileName(realTitle)
    # Get author of the book
    author = requests.get(bookLink).json()["volumeInfo"]["authors"][0]
    # Get the description of the book
    description = requests.get(bookLink).json()["volumeInfo"]["description"]
    # Remove HTML Tags
    description = remove_tags(description)
    #Print title and author of the book
    print(title, "\n", author)
    if(os.path.exists("./Trailers/") == False):
        os.mkdir("./Trailers/")
    if(os.path.exists("./Trailers/" + title) == False):
        os.mkdir("./Trailers/" + title)

    #Sentence Array
    sentences = sentenceSplit(description)

    # Writes image to preProcessedImages array
    def writeQuery(query, index):
        try:
            url = requestImgURL(query)
            if index < 10:
                ind = "0" + str(index)
            else:
                ind = str(index)
            if url != None:
                # response = requests.get(url)
                # open(f"./Projects/{title}/images/{title}.jpg", 'wb').write(response.content)
                # print(response.text)
                image = imageio.imread(url)
                preProcessedImages.append(ImageClip(image))
                
        except:
            print("Error", sys.exc_info()[0], "occured.")

    # Queries Unsplash API for images using user inputted phrases
    imgCount = 1
    index = 0
    remIndices = []
    while(index<len(sentences)):
        print(sentences[index])
        command = input("What is this sentence about?\n")
        if(command == "exit"):
            break
        if(command == "skip" or command == "s"):
            remIndices.append(index)
        else:
            writeQuery(command, imgCount)
            imgCount += 1
        index += 1

    while(len(remIndices) > 0):
        index = remIndices.pop(len(remIndices)-1)
        sentences.pop(index)

    #Ask user for Music preference
    music = input(f"What music would you like to add? (Enter 'none' if you don't want to add music) \n{list(metadata.keys())}\n")
    
    cont = input("Would you like to  create the file? (y/n)\n")
    if(cont == "y"):
        data.append(Datum(title, author, sentences, music, realTitle, preProcessedImages))
        # FIXXXXXX
    cont = input("Would you like to add a trailer? (y/n)\n")
    if(cont == "n"):
        break


for datum in data:
    title = datum.title
    sentences = datum.sentences
    music = datum.music
    author = datum.author
    realTitle = datum.realTitle
    img_clips = []
    preProcessedImages = datum.imageList
    processedImages = []
    print("PreProcessedImages: ", preProcessedImages)

    print(f"Processing {title} images...\n")

    ind = 0
    for image in preProcessedImages:
        sentences[ind] = sentences[ind].split()
        n = 10
        sentences[ind] = [' '.join(sentences[ind][i:i+n]) for i in range(0,len(sentences[ind]),n)]
        for chunk in sentences[ind]:
            image_clip = image
            text_clip = TextClip(txt=chunk,size=(.8*image_clip.size[0], 0),font="Calibri",color="black")
            text_clip = text_clip.set_position('center')
            im_width, im_height = text_clip.size
            color_clip = ColorClip(size=(int(im_width*1.1), int(im_height*1.4)),color=(255, 255, 255))
            color_clip = color_clip.set_opacity(.6)
            clip_to_overlay = CompositeVideoClip([color_clip, text_clip])
            clip_to_overlay = clip_to_overlay.set_position('center')
            final_clip = CompositeVideoClip([image_clip, clip_to_overlay])
            # check if width is even, if not, add 1 to width
            if(final_clip.size[0] % 2 != 0):
                final_clip.size = (final_clip.size[0] + 1, final_clip.size[1])
            # check if height is even, if not, add 1 to height
            if(final_clip.size[1] % 2 != 0):
                final_clip.size = (final_clip.size[0], final_clip.size[1] + 1)
            img_clips.append(final_clip.set_duration(3))
        ind += 1
        




    print("Processing finished.\n Processing end screen...\n")

    #End Screen
    end_screen = ImageClip('end_screen.png', duration=5)
    image_clip = end_screen
    text_clip = TextClip(txt=f'{realTitle} by {author}',size=(.8*image_clip.size[0], 0),font="Calibri",color="black")
    text_clip = text_clip.set_position('center')
    im_width, im_height = text_clip.size
    color_clip = ColorClip(size=(int(im_width*1.1), int(im_height*1.4)),color=(255, 255, 255))
    color_clip = color_clip.set_opacity(.6)
    clip_to_overlay = CompositeVideoClip([color_clip, text_clip])
    clip_to_overlay = clip_to_overlay.set_position('center')
    final_clip = CompositeVideoClip([image_clip, clip_to_overlay])
    img_clips.append(final_clip.set_duration(5))

    print("Concatenating clips...\n")

    #concatenating slides
    video_slides = concatenate_videoclips(img_clips, method="compose")

    print("Concatenating finished.\n")

    #If user doesn't want to add music, just save the video
    print(f"Saving {title}...\n")
    if(music == "none"):
        video_slides.write_videofile(f"./Trailers/{title}/{title}.mp4", fps=24)
    # else, add music to the video
    else:
        print(f"Adding {music} to {title}...\n")
        duration = video_slides.duration
        video_slides.audio = AudioFileClip(f"./MusicLibrary/{music}.mp3")
        print("Adding finished.\n")

        print(f"Saving {title}...\n")
        video_slides = video_slides.subclip(0, duration)
        video_slides.write_videofile(f"./Trailers/{title}/{title}.mp4", fps=24)

        musicCredits = metadata[music]
        # finalProcess(title, musicCredits, f"./Trailers/{title}/")
        
    print(f"{title} trailer created successfully.\n")
