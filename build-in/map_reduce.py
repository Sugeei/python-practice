a = ['1','2','3']

b = map(int, a)

originlist = ['1', '2', '3']
newlist = list(map(int, originlist))
newlist = [int(x) for x in originlist]

newlist = map(int, originlist)
for item in newlist:
    print(item)

print(b)


circle_areas = [3.56773, 5.57668, 4.00914, 56.24241, 9.01344, 32.00013]
result = list(map(round, circle_areas, range(1,7)))

print(result)

date = "2021-01-02"
# year = date.split[0]0
year = int(date[0:4])
month = int(date[5:7])
print(year)
print(month)
year, month, day = map(int, date.split('-'))
year = date.split('-')[0]
month = date.split('-')[1]
