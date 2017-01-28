mydata <- read.csv(file.choose())

x <- mydata$created_at

ll <- c()
amnt <- 0
for (i in x) {
  amnt <- amnt + 1
  tt <- strptime(i, format="%Y-%m-%d %H:%M:%S")
  t <- format(round(tt, units="hours"), format="%H:%M")
  ll[[paste0("element", amnt)]] <- t
}

ggplot(data=mydata, aes(x=ll, y=retweet_count)) + 
  geom_point(alpha=0.05, size=8, colour="red") + 
  ylim(0, 15) +
  ggtitle("Twitter Feedback nach Uhrzeit des Tweets") +
  xlab("Uhrzeit") +
  ylab("Anzahl Retweets") +
  scale_x_discrete(limits=c("05:00",
                            "06:00",
                            "07:00",
                            "08:00",
                            "09:00",
                            "10:00",
                            "11:00",
                            "12:00",
                            "13:00",
                            "14:00",
                            "15:00",
                            "16:00",
                            "17:00",
                            "18:00",
                            "19:00",
                            "20:00",
                            "21:00"))

