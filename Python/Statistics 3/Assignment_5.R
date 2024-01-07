purchase<-read.table("R/STA 4164/STA 4164 Assignment 5 (Fall 2022).csv",header=TRUE,",")
attach(purchase)

model1<-glm(SUV ~ AGE + SAL + GEN, data=purchase, family="binomial")
summary(model1)

round(exp(coef(model1)),3)

library(lmtest)
waldtest(model1, test="Chisq", terms=3)

model2<-glm(SUV ~ AGE + SAL, data=purchase, family="binomial")
summary(model1)
summary(model2)

pchisq(q=1.21, df=1, lower.tail=F)

model3<-glm(SUV ~ AGE + SAL + GEN + AGE*GEN, data=purchase, family="binomial")
summary(model3)

round(vcov(model3),3)
