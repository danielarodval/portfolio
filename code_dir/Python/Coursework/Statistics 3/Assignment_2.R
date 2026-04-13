hurricanes<-read.table("R/STA 4164/Hurricanes.csv",header=TRUE,",")
attach(hurricanes)
sapply(Max.Winds,class)

plot(Central.Pressure,Max.Winds,main="1980-2021 Continental US Hurricanes")


#negative linear relationship exists

hmodel<-lm(Max.Winds ~ Central.Pressure)
hmodel

(cor(Central.Pressure,Max.Winds))^2

summary(hmodel)

predict(hmodel,data.frame(Central.Pressure=941),interval = "prediction",level=.98)

library(HH)
ci.plot(hmodel, conf.level = .98)

cor.test(Central.Pressure,Max.Winds,conf.level = .90)
