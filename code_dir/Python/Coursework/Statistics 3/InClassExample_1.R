library(readr)
#import data
football<-read.csv("R/STA 4164/Unit I EX 3 Football.csv",header=T)
#access variables w/o calling
attach(football)
#separates numerical
sapply(Games.Played, class)

#(A) Contruct a scatterplot for predicting touchdowns from the number of games played. Does there appear to be a linear relationship between
#plotting games played against touchdowns (x,y)
plot(Games.Played,Touchdowns,main="2020 Offensive Statistics")
#positive linear relationship with moderate relationship

#fit line (y~x)
fbmodel<-lm(Touchdowns~Games.Played)

#least squares regression line
print(fbmodel)
print("y hat is -2.267 + 4.892x")
print("touchdowns hat is -2.267 + 4.892(games played)")

#interpret slope
print("For each additional game played, we expect the mean number of touchdowns to increase by 4.892")

#interpret y-intercept
print("When a team plays 0 games, we expect the football team to have -2.267 touchdowns
      This has no practical interpretation")

#test if positive linear relationship between games and touchdowns
summary(fbmodel)

#(L) Construct the confidence and prediction bands for the situations in parts


#Example 8
#Model 2
summary(fbmodel2<-lm(Touchdowns~Games.Played+Field.Goals))#more parisomonious model

#Model 3
summary(fbmodel3<-lm(Touchdowns~Games.Played+Field.Goals+X2.Point.Conversions))

#(A) Which model would you choose using R^2 and model simplicity
print("Picking model 1 or 2 since they yield similiar scores but with less variables")

#(B) 
#predict(fbmodel3,list(Games.Played=10,Field.Goals))



#Example 9


