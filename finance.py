import configparser
import csv

def dateHeader(month, year):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return f'{months[month-1]} {year}'

def calculate(
        csvWriter=None,
        startingYear=2000,
        endingYear=2100,
        startingMonth=1,
        endingMonth=12,
        startingAmount=0,
        monthlyContribution=0,
        yearlyContribution=0,
        interest=0,
        monthlyContributionIncreasePerYear=0,
        yearlyContributionIncrease=0):
    cMonth = startingMonth
    cYear = startingYear
    cBalance = startingAmount
    cMonthlyContrib = monthlyContribution
    cYearContrib = yearlyContribution
    totalInterestGained = 0
    while(endingYear*100+endingMonth >= cYear*100+cMonth):
        initialBalance = cBalance
        contribution = 0
        if cMonth == 1:
            contribution += cYearContrib
        contribution += cMonthlyContrib
        cBalance += contribution
        interestValue = round(cBalance * (interest/12.0), 2)
        cBalance += interestValue
        totalInterestGained += interestValue
        csvWriter.writerow([dateHeader(cMonth, cYear),
                           f'{initialBalance:.2f}',
                           f'{contribution:.2f}',
                           f'{interestValue:.2f}',
                           f'{totalInterestGained:2f}',
                           f'{cBalance:.2f}'])
        cMonth += 1
        if cMonth == 13:
            cMonth = 1
            cYear += 1
            cMonthlyContrib += monthlyContributionIncreasePerYear
            cYearContrib += yearlyContributionIncrease
    return

def aggregate(writer, general, data):
    calculate(
        csvWriter=writer,
        startingYear=int(general['startingyear']),
        endingYear=int(general['endingyear']),
        startingMonth=int(general['startingmonth']),
        endingMonth=int(general['endingmonth']),
        startingAmount=float(data['startingamount']),
        monthlyContribution=float(data['monthlycontribution']),
        yearlyContribution=float(data['yearlycontribution']),
        interest=float(data['interest']),
        monthlyContributionIncreasePerYear=float(data['monthlycontributionincreaseperyear']),
        yearlyContributionIncrease=float(data['yearlycontributionincrease']))
    return


config = configparser.RawConfigParser()
config.read('data.txt')

generalDict = dict(config.items('General'))
sections = config.sections().copy()
sections.remove('General')

f = open('output.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(f)
headers = ['Initial Balance', 'Contribution', 'Interest Gained', 'Total Interest Gained', 'Ending Balance']

for section in sections:
    writer.writerow([section] + headers)
    data = dict(config.items(section))
    aggregate(writer, generalDict, data)

print("Complete! Open output.csv to view results.")
