import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
from tkinter import Tk,Label,Button,Entry,StringVar,IntVar,PhotoImage

def SentimentAnalysis():

        # Authenticating
        consumerKey = 'xQIAFNKhUISz1N2y6RmOoU3jQ'
        consumerSecret = 'sBHCnteFa62HDdFDw8gM8RVQ8Ccn7Z5r8DNEtiWdHWWlRPW7P6'
        accessToken = '1162008861160591360-yxZ7Vc2wBySWTpQAoFBKqkUOqcXWVM'
        accessTokenSecret = 'ZV1OpRqBRUAHo9NWZQZEg4TMUldzgpTcK0HnFNFwtsb07'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        tweets = []
        tweetText=[]
        keyword=a.get()
        termss=b.get()


        tweets = tweepy.Cursor(api.search, q=keyword, lang = "en").items(termss)

        csvFile = open('result.csv', 'a')


        csvWriter = csv.writer(csvFile)

        # Variables
        polarity = 0
        positive = 0
        negative = 0
        neutral = 0


        # Iterating Through Fetched Tweets
        for tweet in tweets:

            tweetText.append(cleanTweet(tweet.text).encode('utf-8'))

            analysis = TextBlob(tweet.text)

            polarity += analysis.sentiment.polarity  # Adding Polarities To Find The Average

            if (analysis.sentiment.polarity == 0):
                neutral += 1

            elif (analysis.sentiment.polarity > 0):
                positive += 1

            elif (analysis.sentiment.polarity < 0):
                negative += 1
            
        csvWriter.writerow(tweetText)
        csvFile.close()

        positive = percentage(positive, termss)
        negative = percentage(negative, termss)
        neutral = percentage(neutral, termss)

        # Finding Average Reaction
        polarity = polarity / termss

        print()
        print("General Reaction Of People")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0):
            print("Positive")
        elif (polarity <0):
            print("Negative")

        print()
        print("Detailes: ")
        print(str(positive) + "% T='Number Of Tweets To Search :')weets were Positive")
        print(str(negative) + "% Tweets Were Negative")
        print(str(neutral) + "% Tweets Were Neutral")

        plotPieChart(positive,negative, neutral, keyword, termss)

def cleanTweet(tweet):
        # Remove Links, Special Characters etc From Tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # Function To Calculate Percentage
def percentage(part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

def plotPieChart(positive, negative, neutral, keyword, noOfkeywords):
        labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]','Negative [' + str(negative) + '%]']
        sizes = [positive, neutral, negative]
        colors = ['yellowgreen','gold', 'darkred']
        explode = (0.1, 0, 0)
        patches,texts = plt.pie(sizes, colors=colors, labels=labels,explode=explode,startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')
        plt.tight_layout()
        plt.show()



if __name__== "__main__":
    window=Tk()
    window.title("Sentimental Analysis")
    window.geometry('900x300+10+10')

    lbl1=Label(window, text='KeyWord To Search About :')
    lbl1.place(x=100, y=50)
    a=StringVar()
    t1=Entry(window,textvariable=a)
    t1.place(x=400, y=50)
    

    lbl2=Label(window, text='Number Of Tweets To Search :')
    lbl2.place(x=100, y=100)
    b=IntVar()
    t2=Entry(window,textvariable=b)
    t2.place(x=400, y=100)
    
   
    btn=Button(window,text="Submit", command=SentimentAnalysis)
    btn.place(x=100, y=150)
    window.mainloop()
