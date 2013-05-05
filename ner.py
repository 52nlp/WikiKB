import re
import sys

def initPattern(): 
  pattern5 = re.compile("(.)(0[1-9]|[12][0-9]|3[01])(\\ )(January|February|March|April|May|June|July|August|September|October|November|December)(\\ )(19|20)(\\d\\d)(.)");
  pattern4 = re.compile("((January|February|March|April|May|June|July|August|September|October|November|December)(\\ )*(\\t)*(1|2|3|4|5|6|7|8|9)*(0[1-9]|[12][0-9]|3[01])(\\ )*(,)*(\\ )*(\\t)*(19|20)(\\d\\d)(\\n)*)");
  pattern = re.compile("(0[1-9]|1[012])([- /.])(0[1-9]|[12][0-9]|3[01])([- /.])(19|20)(\\d\\d)")
  #email
  pattern2 = re.compile("([A-Za-z0-9])(([_\\.\\-]?[a-zA-Z0-9]+){0,15})(@)([A-Za-z0-9]+)(([\\.\\-]?[a-zA-Z0-9]+){0,14})(\\.)([A-Za-z]{2,})")
  #time
  pattern3 = re.compile("(20|21|22|23|[01]\\d|\\d)(([:][0-5]\\d){1,2}[ ]*(pm|PM|am|AM))")
  #url
  #pattern11 = re.compile("(https?:\\/\\/)?([\\da-z\\.-]+)\\.([a-z\\.]{2,6})([\\/\\w \\.-]*)*\\/?");
  #distance
  pattern6 = re.compile("(([0-9]){1,3}(,)*([0-9]){0,4}(,)*([0-9]){0,4}(\\ )*(million|billion|thousand|hundred thousand)*(\\ )*(meter|ft|feet|foot|miles|mile|kilometer|m)+)(\\W)") 
  #area
  pattern7 = re.compile("(([0-9]){1,4}(,)*([0-9]){0,4}(,)*([0-9]){0,4}(\\ )*(million|billion|thousand|hundred thousand)*(\\ )*(sq kilometer|square kilometer|sq ft|m2)+)") 
  #volume
  pattern8 = re.compile("(([0-9]){0,4}(,)*([0-9]){0,4}(,)*([0-9]){0,4}(\\ )*(million|billion|thousand|hundred thousand)*(\\ )*(oz|cubic meter|cc|ounce|fl. oz|fl oz)+)") 
  #currency
  pattern9 = re.compile("(([0-9]){0,4}(,)*([0-9]){0,4}(,)*([0-9]){0,4}(\\ )*(million|billion|thousand|hundred thousand)*(\\ )*(Dollars|\\$)+)") 
  pattern10 = re.compile("((US)*(\\$)(\\ )*(dollar)*([0-9]){1,4}(,)*([0-9]){0,4}(,)*([0-9]){0,4}(\\ )*(million|billion|thousand|hundred thousand)*(\\ )*)") 

  #just year
  year = re.compile("(([0-9]{4})|([0-9]+ (B.C.|BC|A.D.|AD)))")
  height = re.compile("")

  #August 14, 2003 -- August 14th, 2003
  date1 = re.compile("(([J|j]anuary|[F|f]ebruary|[m|M]arch|[a|A]pril|[m|M]ay|[j|J]une|[j|J]uly|[a|A]ugust|[s|S]eptember|[o|O]ctober|[n|N]ovember|[d|D]ecember) ([0-9]{2}|[0-9]{1})[ ]?[,]?[ ]?(([0-9]{4})|([0-9]+ (B.C.|BC|A.D.|AD))))")

  #14th August, 1956
  date2 = re.compile("(([0-9]{2}|[0-9]{1})([a-zA-Z]{2})? ([J|j]anuary|[F|f]ebruary|[m|M]arch|[a|A]pril|[m|M]ay|[j|J]une|[j|J]uly|[a|A]ugust|[s|S]eptember|[o|O]ctober|[n|N]ovember|[d|D]ecember)[ ]?[,]?[ ]?(([0-9]{4})|([0-9]+ (B.C.|BC|A.D.|AD))))")

  pats = {"DISTANCE":[pattern6],"TIME":[pattern3],"AREA":[pattern7],"VOLUME":[pattern8],"CURRENCY":[pattern9,pattern10],"DATE":[date1,date2,pattern,pattern4,pattern5,year],"EMAIL":[pattern2]}#,"URL":[pattern11]}
  return pats


def findPattern(sent,pat,st):
  res = []
  try:
    pats = pat[st]
    for p in pats:
      m = re.search(p,sent)
      if m:
        return [m.group()]
  except:
    print "no pattern class found"

  return res

if __name__ == "__main__":
  pat = initPattern()
  print findPattern("dfsdfsdf 14 August 1897 dfssf",pat,"DATE")