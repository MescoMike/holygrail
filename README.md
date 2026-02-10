Have you ever wondered how often certain words appear in comedy movies at various points in it's run time?

What do you mean "No"? Anyway ...

This script takes a subtitle file (holyGrail.srt), which contains the closed captioning data for the movie Monty Python's Holy Grail, and builds a Pandas dataframe mapping the text in each subtitle.

Then we take a dictionary containing the words we wish to plot (including any synonyms we provide) and produces a plot.

The initial dictionary in this script is:

targetWordDict = {
  "Birds": ["bird","birds", "swallow", "duck", "robin", 'chicken'],
  "Grail": ["grail", "grails"],
  "Ni": ["ni"]
}

Using matplotlib.pyplot, this gives us the plot:

<img width="633" height="485" alt="Screenshot 2026-02-10 at 18 25 36" src="https://github.com/user-attachments/assets/57ac789a-5db0-461a-8359-d28970b22615" />



