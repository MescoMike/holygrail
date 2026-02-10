import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def dateFormat(dateString):
    formattedString = dateString[:dateString.index(millisec_delimiter)]
    return datetime.strptime(formattedString, timeFormat)

def getRegex(word_list):
    reg = r'\b(?:'
    for w in word_list:
        reg += w + '|'
    reg = reg[:-1] + r')\b'
    return reg

# Dictionary of terms for each plot
targetWordDict = {
  "Birds": ["bird","birds", "swallow", "duck", "robin", 'chicken'],
  "Grail": ["grail", "grails"],
  "Ni": ["ni"]
}
# This is the interval in mins used to group incidences of a word
window_length_minutes = 2

y_axis = 'No. of times'
plot_title = 'Words in Monty Python\'s Holygrail'

counter=1
maxCount = 10000
timeFormat = '%H:%M:%S'
millisec_delimiter = ','
timeStampSeparator = " --> "

subtitleIndex = 0
subtitleString = ""
timeStampFrom = ""
timeStampTo = ""
lastLineEmpty = True

# this dataframe represents a series of time interval bins or length window_length_minutes. text column is the full transcript
# of dialogue delivered in that interval
timeline_df = pd.DataFrame(columns=['number', 'timeFrom', 'timeTo', 'text'])

# open the srt file and read in each line.
# IF the end of a subtitle is detected, set the "text" field as subtitleString, and reset subtitleString
# ELSE IF a timestamp is detected, set the timeFrom/To fields.
# ELSE append current line to subtitleString
with open("holyGrail.srt") as file:

    while (line := file.readline()) and counter<=maxCount:

        text = line.rstrip()
        if lastLineEmpty:
            if subtitleIndex > 0:
                timeline_df.loc[subtitleIndex - 1] = [subtitleIndex, timeStampFrom, timeStampTo, subtitleString]
            subtitleIndex += 1
            subtitleString = ""
        elif timeStampSeparator in text:
            timeStampFrom = dateFormat(text[:text.index(timeStampSeparator)])
            timeStampTo = dateFormat(text[text.index(timeStampSeparator) + len(timeStampSeparator):])
        else:
            subtitleString += " "
            subtitleString += text.lower()

        lastLineEmpty = len(line.rstrip()) == 0
        counter += 1

start_time = datetime.strptime("00:00:00", timeFormat)
end_time = timeline_df.iloc[-1]['timeFrom']
number_of_minutes = (timeline_df.iloc[-1]['timeTo'] - start_time).total_seconds() / 60
no_of_bins = round(number_of_minutes / window_length_minutes)


# for each key in the targetWordDict dictionary, add a count column to timeline_df
# build a regex for each list of words, and get the count for each regex
plot_list = []

for targetWord in targetWordDict.keys():
    plot_name = targetWord+'count'
    regex = getRegex(targetWordDict[targetWord])
    timeline_df[plot_name] =timeline_df['text'].str.count(regex)
    plot_list.append(plot_name)


# list of date/times that will be used to create a new df based on each bin
date_list = [start_time + timedelta(minutes=(x+1) * window_length_minutes) for x in range(no_of_bins)]
columnList = ['timeStamp', 'timeFrom', 'timeTo'] + plot_list
timestamps = pd.DataFrame(columns=columnList)

# populate the df for each timestamp, aggregating each count field
for idx, i in enumerate(date_list):
    begin = i - timedelta(minutes = window_length_minutes)
    end = i

    ts_rows = timeline_df[timeline_df['timeTo'].between(begin, end)]
    count_columns = []
    for targetWord in targetWordDict.keys():
        plot_name = targetWord+'count'
        targetCount = ts_rows[plot_name].sum()
        count_columns.append(targetCount)

    timestamps.loc[i] = [i, begin, end] + count_columns

# show a plot with the new timestamp dataframe
timestamps.plot(x='timeStamp', y=plot_list, kind='line', label=targetWordDict.keys())

plt.xlabel('Time')
plt.ylabel(y_axis)
plt.title(plot_title)

plt.show()