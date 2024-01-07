rush<-read.table("R/STA 4164/STA 4164 Assignment 4 (Fall 2022).csv",header=TRUE,",")
attach(rush)

complete.model<-lm(YDS ~ ATT + AVG + LNG + TD,data=rush)

library(olsrr)
ols_step_forward_p(complete.model)

ols_step_backward_p(complete.model)

ols_step_both_p(complete.model)

ols_step_all_possible(complete.model)

final.model <-lm(YDS ~ ATT + AVG + LNG ,data=rush)
summary(final.model)

plot(fitted.values(final.model), rstudent(final.model))

library(moments)
skewness(rstudent(final.model))
kurtosis(rstudent(final.model))

plot(final.model)

library(car)
vif(final.model)

cooks.distance(final.model)
hatvalues(final.model)

qt(df=50-3-2, 0.95)
rstudent(final.model)
