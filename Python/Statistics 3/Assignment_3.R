chickfila<-read.table("R/STA 4164/Chick Fil A Data.csv",header=TRUE,",")
attach(chickfila)

# (A)
print(round(cor(chickfila),3))

# (C)
pairs(chickfila)

# (D)
model1<-lm(Calories ~ Fat + Carbs)
summary(model1)

# (E)
library('ppcor')
pcor.test(Calories, Protein, Fat)

# (G)
library('ppcor')
pcor.test(Calories, Protein, chickfila[c("Fat","Carbs")])

# (H) Calories, Protein|Fat, Carbs
complete.model<-lm(Calories ~ Protein + Fat + Carbs)
anova(complete.model)

reduced.model<-lm(Calories ~ Protein)
anova(reduced.model)

pf(q=683.973,df1=2,df2=31,lower.tail=F)

# (I)
