crab<-read.table("R/STA 4164/STA 4164 Assignment 6 (Fall 2022).csv",header=TRUE,",")
crab$COLOR<-as.factor(crab$COLOR)
sapply(crab, class)
COLOR2<-ifelse(crab$COLOR == "2", 1, 0)
COLOR3<-ifelse(crab$COLOR == "3", 1, 0)
COLOR4<-ifelse(crab$COLOR == "4", 1, 0)
COLOR5<-ifelse(crab$COLOR == "5", 0, 0)

model1<-glm(formula = SATELLITES ~ WIDTH + COLOR2 + COLOR3 + COLOR4, family = "poisson")
summary(model1)

round(exp(coef(model1)),4)

round(exp(confint(model1)),4)

model2<-glm(formula = SATELLITES ~ WIDTH, family = "poisson")
anova(model2, model1, test='Chisq')
