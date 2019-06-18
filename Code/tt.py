import datetime
import calendar
x= str(datetime.datetime.utcnow()).replace("-", "").replace(":", "").replace(".", "").replace(" ", "")


dob = datetime.datetime.strptime("1946-07-01", '%Y-%m-%d')
print(dob)

dobtimestamp = calendar.timegm(dob.utctimetuple())

print(dobtimestamp)

# date_text = "13SEP2014"
# date = datetime.datetime.strptime(date_text, "%d%b%Y")
# print(date)
# timestamp =calendar.timegm(date.utctimetuple())
# print(timestamp)


# readable = datetime.datetime.fromtimestamp(timestamp).isoformat()
# print(readable)

# #print(int(x))

# print(hex('MOhit'))
#print(type('0x68656c6c6f0000000000000000000000'))