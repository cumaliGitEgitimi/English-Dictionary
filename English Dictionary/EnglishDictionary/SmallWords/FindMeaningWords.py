import math
from textblob import TextBlob as tb

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

document1 = tb("""<MAINTITILE>The Basics of Archery  </MAINTITLE>
<TITLE>Anatomy of a Bow and Arrow</TITLE>
Abow is made up from several parts:
The Riser - The riser of a bow is the handle. It is where you hold the bow and most accessories, such as sights or stabilizers, attach to it.
The Limbs - The limbs of the bow are where the energy is stored when you draw the bow and are attached to either side of the Riser.
The String - The string runs between the tips of the two limbs and is where the arrow attaches. It is what you draw to shoot.
The Sight - The sight is what you use to aim the bow. It attaches to the riser.
Stabilizers - These help reduce the vibrations to produce a smooth shot.

An arrow also consists of several parts:

The Pile - This is the point of the arrow.
The Shaft - This is the main length of the arrow.
The Nock - The grove on the back of the arrow that allows it to attach to the string.
The Fletchings - These are the flights or feathers as most people know them, towards the back of the shaft. They cause drag on the back of the arrow to keep it straight during flight.

<TITLE>Types of bow</TITLE>
<P>There are three main types of bow used for archery: the longbow, the recurve and the compound.</P> 
<P>Longbows are what most people envision when you say the word archery. It is the most basic type of bow used and is made in one piece from either a single piece of wood or a composite of different woods. Longbows have been around for thousands of years in one form or another and were used for hunting and warfare.  A longbow is usually around about the same height as the shooter and on average has a draw weight of about 40 pounds, although this may be more or less depending on the strength of the shooter.</P>

<P>Recurve bows are so called because of their shape, as the tips of the bow curve away from the archer. This enables the limbs of the bow to store more energy than an equivalent straight bow and so gives the potential for a faster, more powerful shot from a shorter bow. Recurve bows have been used throughout history by many cultures, usually for the purpose of horseback archery where a shorter bow is more preferable. Modern recurves are the most widely shot bows in target archery and are the bow type used in the Olympic Games.</P>

<P>Compound bows are the most modern type of bow, only being around since the middle of the 1960s. They are usually much shorter than other types of bow and consist of a levering system of cables and pulleys to help draw the bow. The use of this system creates a draw-force curve which increases to a point and then lets off (usually to around 60%-80% of peak weight) as you approach full draw. This means that the force required to hold the bow is reduced so the archer can take more time to aim. Compound bows produce a faster shooting velocity than other bows and are more accurate.</P>

<TITLE>Types of Archery<TITLE>
<P>Target - Target archery is probably the most common form of archery shot. It involves shooting a set number of arrows at a standard target at a known distance. It is the type of archery shot in the Olympics. </P>
<P>Field - Field archery involves following a set course, usually around a woodland area, and shooting at a series of targets at either a known or unknown distance. </P>
<P>Flight - Flight archery is the art of shooting an arrow as far as possible. Flight bows are usually designed purely for speed, although there are sections within the competition for normal target bows as well. The distances are measured from a pre-determined line, so the idea is to stay as close to that line as possible while aiming for maximum distance. </P>
""")

document2 = tb("""Python, from the Greek word (πύθων/πύθωνας), is a genus of
nonvenomous pythons[2] found in Africa and Asia. Currently, 7 species are
recognised.[2] A member of this genus, P. reticulatus, is among the longest
snakes known.""")

document3 = tb("""The Colt Python is a .357 Magnum caliber revolver formerly
manufactured by Colt's Manufacturing Company of Hartford, Connecticut.
It is sometimes referred to as a "Combat Magnum".[1] It was first introduced
in 1955, the same year as Smith & Wesson's M29 .44 Magnum. The now discontinued
Colt Python targeted the premium revolver market segment. Some firearm
collectors and writers such as Jeff Cooper, Ian V. Hogg, Chuck Hawks, Leroy
Thompson, Renee Smeets and Martin Dougherty have described the Python as the
finest production revolver ever made.""")

bloblist = [document1, document2, document3]
for i, blob in enumerate(bloblist):
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:3]:
        print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))