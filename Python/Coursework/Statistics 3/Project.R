#import and view data
pizza<-read.csv("R/STA 4164/Data/Pizza Restaurant Sales/Data Model - Pizza Sales.csv",header=T,",")
attach(pizza)
View(pizza)
print(sapply(pizza,class))
class(pizza)
#prepping data
#dropping user dictated no significant columns
pizza=subset(pizza,select=-c(order_details_id, order_id,pizza_id,order_date,pizza_name,pizza_category))

#counting commas in a string
library(stringr)

#replaces ingredients with count of ingredients
pizza$pizza_ingredients[]<-(str_count(pizza_ingredients,',')+1)#replaces
ingredients<-as.numeric(pizza$pizza_ingredients)#stores as numeric to avoid categorical data confusion
pizza$pizza_ingredients<-ingredients#reinstates as numeric rather than characters
#time of day categories
#prep data
library(chron)#time package in R
pizza$order_time<-chron(times=pizza$order_time)#converts existing data into time data
x=as.POSIXct(strptime(c("050000","105959","110000","155959","160000","185959"),"%H%M%S"),"UTC")#determines time intervals

tod <- cut(chron::times(pizza$order_time) , breaks = (1/24) * c(0,5,11,16,19,24))#breaks order times into intervals
pizza$order_time<-cut(chron::times(pizza$order_time) , breaks = (1/24) * c(0,5,11,16,19,24), labels = c("night", "morning", "afternoon", "evening", "night"))#labels intervals determined earlier

#data has been prepped can now go to a linear model
model1<-lm("total_price ~ .",data=pizza)#fits with all data remaining in pizza
summary(model1)

write.csv(pizza,"R/STA 4164/Data/Pizza Restaurant Sales/Clean Data.csv", row.names = FALSE)

#find best model
library(olsrr)
ols_step_forward_p(model1)
ols_step_backward_p(model1)
ols_step_all_possible(model1)
ols_step_both_p(model1)

bestmodel<-lm("total_price ~ quantity + order_time + unit_price + pizza_size",data=pizza)
summary(bestmodel)
#diagnostic plots (QQ, Fitted vs Residuals, Scale-Location, Residuals vs Leverage)
par(mfrow=c(2,2)) # Change the panel layout to 2 x 2
plot(bestmodel)
par(mfrow=c(1,1)) # Change back to 1 x 1

#cooks.distance(bestmodel) yields too many so we automate a little
cooksD <- cooks.distance(bestmodel)#cooks distance of outliers
influential <- cooksD[(cooksD > (3 * mean(cooksD, na.rm = TRUE)))]#finds significant outliers from cooks distance
influential#shows

library(dplyr)
names_of_influential <- names(influential)#gets row names for outliers
outliers <- pizza[names_of_influential,]#outliers are marked from dataset
pizza_without_outliers <- pizza %>% anti_join(outliers)#remove outliers
bestmodel2 <- lm(total_price ~ . -pizza_ingredients, data = pizza_without_outliers)#fit new model without outliers and with ingredients(from best fit)
summary(bestmodel2)

write.csv(best_cat,"R/STA 4164/Data/Pizza Restaurant Sales/Best Cat.csv", row.names = FALSE)

#testing new model after cooks.distances removal
par(mfrow=c(2,2)) # Change the panel layout to 2 x 2
plot(bestmodel2)
par(mfrow=c(1,1)) # Change back to 1 x 1
#normality
library(moments)
skewness(rstudent(bestmodel))
kurtosis(rstudent(bestmodel))
skewness(rstudent(bestmodel2))
kurtosis(rstudent(bestmodel2))

#prep data to be fitted in model (dummies & interactions)
#onehotencoder for categorical
library(caret)
#encoder attempts to encode number of ingredients, we removed and will add back
noNames <- dummyVars(" ~ .",data=pizza_without_outliers)
cat_pizza <- data.frame(predict(noNames, newdata=pizza_without_outliers))

#collinearity
best_cat  = subset(cat_pizza, select = -c(pizza_ingredients) )
pairs(best_cat)
round(cor(best_cat),4)#nothing close to .9 besides unit_price and total_price
library(car)
vif(bestmodel2)
ols_vif_tol(bestmodel2)
library(mctest)
eigprop(bestmodel2)
#testing (predicting time of day pricing)