mydata <- read.csv(file.choose())

data_filtered <- mydata[mydata$likes<100,]
x <- data_filtered$status_published

ll <- c()
amnt <- 0
for (i in x) {
  amnt <- amnt + 1
  tt <- strptime(i, format="%Y-%m-%d %H:%M:%S")
  t <- format(round(tt, units="hours"), format="%H:%M")
  ll[[paste0("element", amnt)]] <- t
}

ggplot(data=mydata[mydata$likes<100,], aes(x=ll, y=likes, colour=status_type)) + 
  geom_point(alpha=0.2, size=2) + 
  ylim(0, 75) +
  ggtitle("Facebook Feedback nach Uhrzeit des Posts") +
  xlab("Uhrzeit") +
  ylab("Anzahl Likes") +
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

