#Question 1
println("Question 1 Output:")
#Suppose the cover price of a book is $24.95
cover_price = 24.95
#bookstores get a 40% discount
discount = 0.40
discounted_price = cover_price * (1 - discount)

#Shipping costs $3 for the first copy and 75 cents for each additional copy
number_of_copies = 60
shipping_cost = 3 + (number_of_copies - 1) * 0.75

#What is the total wholesale cost for 60 copies
total_cost = discounted_price * number_of_copies + shipping_cost
println("Total wholesale cost for ",number_of_copies," copies: \$", total_cost)

#Question 2
println("Question 2 Output:")
#convert time to minutes
function time_to_seconds(hours,minutes,seconds)
  return hours * 3600 + minutes * 60 + seconds
end

#convert minutes back into time
function seconds_to_time(seconds)
  hours = div(seconds, 3600)
  remaining_seconds = seconds % 3600
  minutes = div(remaining_seconds, 60)
  seconds = remaining_seconds % 60
  return (hours, minutes, seconds)
end

#If I leave my house at 6:52 a.m.
start_time = time_to_seconds(6,52,0)

#and run 1 mile at an easy pace (8:15 per mile) then 3 miles at tempo (7:12 per mile) and 1 mile at easy pace again
easy_pace = time_to_seconds(0,8,15)
tempo_pace = time_to_seconds(0,7,12)
total_run_time = 2 * easy_pace + 3 * tempo_pace

#what time do I get home for breakfast?
end_time = start_time + total_run_time

(hours, mins) = seconds_to_time(end_time)
println("Return time for breakfast: ", hours, ":", mins, " AM")

#Question 3
println("Question 3 Output:")
#The function time returns the current Greenwich Mean Time in seconds since “the epoch,”
current_time = time()
seconds_in_a_day = 24 * 60 * 60

#Write a script that reads the current time and converts it to a time of day in hours, minutes, and seconds,
days_since_epoch = div(current_time,seconds_in_a_day)
remaining_seconds = current_time % seconds_in_a_day

hours = div(remaining_seconds,3600)
minutes = div(remaining_seconds % 3600, 60)
seconds = remaining_seconds % 60

println("Current time: ",hours, ":",minutes, ":",seconds, " and ",days_since_epoch, " days since the epoch")
