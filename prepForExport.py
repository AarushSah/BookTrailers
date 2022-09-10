import requests, os

libraries = {
    "Union Public Library": {
        "socials": """FACEBOOK: https://www.facebook.com/UnionPublicLibraryNJ/
INSTAGRAM: https://www.instagram.com/unionpubliclibrarynj/"""
    },
    "Delray Library": {
        "socials": """FACEBOOK: https://www.facebook.com/DelrayBeachPublicLibrary
INSTAGRAM: https://www.instagram.com/delraybeachpubliclibrary/
TWITTER: https://twitter.com/Delray_Library
LINKEDIN: https://www.linkedin.com/company/delraybeachpubliclibrary/
GOODREADS: https://www.goodreads.com/user/show/17236968-delray-beach-public-library"""
    }

}
def finalProcess(title, musicCredits, path):

    # Gets and writes the book cover from Google Books API
    with open("cover.jpg", "wb") as f:
        f.write(requests.get("https://books.google.com/books/content?id=" + title + "&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api").content)
    # Gets the google books description
    GBdescription = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + title).json()['items'][0]['volumeInfo']['description']
    
    for library in libraries:
        # Gets the library's socials
        socials = libraries[library]["socials"]
        # Writes the description
        description = f"""
Check {title} out at the {library}!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
OUR SOCIALS:
{socials}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Trailer made by AARUSH SAH
AARUSH'S WEBSITE:  https://aarushsah.github.io
AARUSH'S INSTAGRAM: @aarushaaditsah
AARUSH'S TWITTER: @AarushSah_

~~~~~~~~~~~~~~~~~~~~~~~~~~~~
BOOK DESCRIPTION:
{GBdescription}

~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Music Credits: 
{musicCredits}

Images from Unsplash
The internet's source of freely-usable images.
Powered by creators everywhere.
"""
        # Writes the file
        with open(path + title + library + ".txt", "x") as f:
           f.write(description)

# finalProcess("Warbreaker", "", "C:/Users/Aarush/Desktop/BookTrailers/")

#folders = os.listdir("C:/Users/aarus/Desktop/BookTrailers/Trailers/")
#for folder in folders:
#    try:
#        for file in os.listdir("C:/Users/aarus/Desktop/BookTrailers/Trailers/" + folder):
#                if file.endswith(".txt"):
#                    with open("C:/Users/aarus/Desktop/BookTrailers/Trailers/" + folder + '/description.txt') as f:
#                        music = f.readlines()
#                        print(music)
#                if file.endswith(".mp4"):
#                    file = file.replace(".mp4", "")
#                    print(file)
#                   finalProcess(file, music, "C:/Users/aarus/Desktop/BookTrailers/Trailers/" + folder + "/")
#    except:
#        print("FAILED" + folder)
#