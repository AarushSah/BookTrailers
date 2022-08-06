import requests, json, random, os, re, math, sys
from musicMetadata import metadata
from moviepy.editor import *
from pathlib import Path

vidDesc = ""


# Remove HTML Tags with REGEX
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub(' ', text).replace('  ', ' ').replace('\n', ' ')

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
clientID = "zPfxC4pX5v3jRMt69bPp52UnVgtHt0xNyJqJWSxuh3E"

# Get the title of the book
title = input("What is the title of the book?\n")
freshTitle = title
title = title.replace(" ", "_")

# Get Link to book from Google Books API
bookLink = requests.get("https://www.googleapis.com/books/v1/volumes?q=" + title).json()["items"][0]["selfLink"]
# Print bookLink
print(bookLink)
# Get title of the book
title = requests.get(bookLink).json()["volumeInfo"]["title"]
# Get author of the book
author = requests.get(bookLink).json()["volumeInfo"]["authors"][0]
# Get the description of the book
description = requests.get(bookLink).json()["volumeInfo"]["description"]
# Remove HTML Tags
description = remove_tags(description)
#Print title, author, and description of the book
print(title, "\n", author)
#Check if video project directory exists - if not, create it
if(os.path.exists("./Projects/" + title) == False):
    os.mkdir("./Projects/" + title)
    os.mkdir("./Projects/" + title + "/images")
    os.mkdir("./Projects/" + title + "/processed")
else:
    sys.exit("Project already exists. Please delete the project folder and try again.")
#Sentence Array
sentences = sentenceSplit(description)

# Get the image URL from Unsplash API
def requestImgURL(query):
    try:
        ran = random.randint(0,9)
        r = requests.get(f"https://api.unsplash.com/search/photos?query={query}&client_id={clientID}&orientation=landscape")
        if r.status_code == 200:
            
            return r.json()['results'][ran]['urls']['regular']
        else:
            return None
    except:
        return None

# Writes image to project directory
def writeQuery(query, index):
    try:
        url = requestImgURL(query)
        if url != None:
            response = requests.get(url)
            open(f"./Projects/{title}/images/{title}{index}.jpg", 'wb').write(response.content)
    except:
        print("Error")

# Queries Unsplash API for images using user inputted phrases
imgCount = 1
index = 0
remIndices = []
while(index<len(sentences)):
    print(sentences[index])
    command = input("What is this sentence about?\n")
    if(command == "exit"):
        break
    if(command == "skip"):
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

img_clips = []
path_list=[]


#accessing path of each image and appending it to path_list
for image in os.listdir(f'./Projects/{title}/images'):
    if image.endswith(".jpg"):
        path_list.append(os.path.join(f'./Projects/{title}/images', image))

ind = 0
ind2 = 0
for image in path_list:
    sentences[ind] = sentences[ind].split()
    n = 10
    sentences[ind] = [' '.join(sentences[ind][i:i+n]) for i in range(0,len(sentences[ind]),n)]
    for chunk in sentences[ind]:
        print(chunk)
        image_clip = ImageClip(image)
        text_clip = TextClip(txt=chunk,size=(.8*image_clip.size[0], 0),font="Calibri",color="black")
        text_clip = text_clip.set_position('center')
        im_width, im_height = text_clip.size
        color_clip = ColorClip(size=(int(im_width*1.1), int(im_height*1.4)),color=(255, 255, 255))
        color_clip = color_clip.set_opacity(.6)
        clip_to_overlay = CompositeVideoClip([color_clip, text_clip])
        clip_to_overlay = clip_to_overlay.set_position('center')
        final_clip = CompositeVideoClip([image_clip, clip_to_overlay])
        final_clip.save_frame(f"./Projects/{title}/processed/{title}{ind2+1}.png")
        ind2 += 1
    ind += 1
    

for image in os.listdir(f'./Projects/{title}/processed'):
    clippy = f'./Projects/{title}/processed/{image}'
    img_clips.append(ImageClip(clippy, duration=3))
    print(clippy)

#End Screen
end_screen = ImageClip('end_screen.png', duration=4)
image_clip = end_screen
text_clip = TextClip(txt=f'{title} by {author}',size=(.8*image_clip.size[0], 0),font="Calibri",color="black")
text_clip = text_clip.set_position('center')
im_width, im_height = text_clip.size
color_clip = ColorClip(size=(int(im_width*1.1), int(im_height*1.4)),color=(255, 255, 255))
color_clip = color_clip.set_opacity(.6)
clip_to_overlay = CompositeVideoClip([color_clip, text_clip])
clip_to_overlay = clip_to_overlay.set_position('center')
final_clip = CompositeVideoClip([image_clip, clip_to_overlay])
final_clip.save_frame(f"./Projects/{title}/processed/{title}{ind2+1}.png")
img_clips.append(ImageClip(f"./Projects/{title}/processed/{title}{ind2+1}.png", duration=5))

#concatenating slides
video_slides = concatenate_videoclips(img_clips, method="compose")


#If user doesn't want to add music, just save the video
if(music == "none"):
    video_slides.write_videofile(f"./Projects/{title}/{title}.mp4", fps=24)
# else, add music to the video
else:
    duration = video_slides.duration
    video_slides.audio = AudioFileClip(f"./MusicLibrary/{music}.mp3")

    video_slides = video_slides.subclip(0, duration)
    video_slides.write_videofile(f"./Projects/{title}/{title}.mp4", fps=24)

    vidDesc = vidDesc + f"\n\n{metadata[music]}"
    with open(f'./Projects/{title}/description.txt', 'a') as f:
        f.write(vidDesc)
    print(vidDesc)
    
# print(metadata)
