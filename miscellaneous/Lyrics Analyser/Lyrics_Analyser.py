text = """
Her name was Lola, she was a showgirl
With yellow feathers in her hair and a dress cut down to there
She would merengue and do the cha-cha
And while she tried to be a star
Tony always tended bar
Across the crowded floor, they worked from eight til four
They were young and they had each other
Who could ask for more?
At the copa (co) Copacabana (Copacabana)
The hottest spot north of Havana (here)
At the copa (co) Copacabana
Music and passion were always the fashion
At the copa they fell in love
Copa, Copacabana
His name was Rico
He wore a diamond
He was escorted to his chair, he saw Lola dancing there
And when she finished, he called her over
But Rico went a bit to far
Tony sailed across the bar
And then the punches flew and chairs were smashed in two
There was blood and a single gun shot
But just who shot who?
At the copa (co) Copacabana (Copacabana)
The hottest spot north of Havana (here)
At the copa (co) Copacabana
Music and passion were always the fashion
At the copa, she lost her love
(Copa, Copacabana)
(Copa, Copacabana)
(Copacabana)
like in Havana
(Copa, banana)
Music and passion were always in fashion
Her name is Lola, she was a showgirl
But that was thirty years ago, when they used to have a show
Now it's a disco, but not for Lola
Still in dress she used to wear
Faded feathers in her hair
She sits there so refined, and drinks herself half-blind
She lost her youth and she lost her Tony
Now she's lost her mind
At the copa (co) Copacabana (Copacabana)
The hottest spot north of Havana (here)
At the copa (co) Copacabana
Music and passion were always in fashion
At the copa don't fall in love
don't fall in love
(Copacabana)
(Copacabana)
"""

word_count = {}

for word in text.lower().split():
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

print(word_count)
print(text.split())  # Prints a list of all of the words in a string. Includes repetition.
