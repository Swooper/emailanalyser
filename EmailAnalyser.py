# -*- coding: utf-8 -*-
# Haukur Jónasson
# Tryggvi Þór Guðmundsson

import xml.etree.cElementTree as ET

def main():
    fileName = 'messages.xml'

    print 'Building tree...'
    tree = ET.parse(fileName)
    print ' > Tree built.'
    print ''

    root = tree.getroot()

    # totalEmails(root)
    # reAndFwdCounts(root)
    # countByMonth(root)
    # countBySender(root)
    # mostCommonWords(root)
    mostCommonWordsByMonth(root)

def totalEmails(root):
    print 'Counting...'
    counter = 0
    for child in root.iter('message'):
        counter+=1
    print 'Total emails:',counter 

def reAndFwdCounts(root):
    subjects = []
    for child in root.iter('subject'):
        subjects.append(child.text)
        
    replyCounter = 0
    fwdCounter = 0
    
    for sub in subjects:
        if 'Re:' in sub:
            replyCounter+=1
        if 'Fwd:' in sub:
            fwdCounter+=1

    print 'Replies:',replyCounter
    print 'Forwards:',fwdCounter

def countByMonth(root):
    print 'Counting emails by month...'
    dates = {}
    for child in root.iter('date'):
        yyyymm = child.text[:6]
        if yyyymm not in dates:
            dates[yyyymm] = 1
        else:
            dates[yyyymm] += 1

    months = {'01': 'January',
              '02': 'February',
              '03': 'March',
              '04': 'April',
              '05': 'May',
              '06': 'June',
              '07': 'July',
              '08': 'August',
              '09': 'September',
              '10': 'October',
              '11': 'November',
              '12': 'December' }

    newyear = ''
    for key in sorted(dates):
        # Seperating year and month
        yyyy = str(key)[:4]
        mm = str(key)[4:6]
        if yyyy != newyear:
            print '\n'+yyyy+':'
        newyear = yyyy
        month = months[mm]
                
        print '\t'+month+':\t\t'+str(dates[key])
    print ''

def countBySender(root):
    print 'Counting emails by sender...'
    print ''
    senders = {}
    for child in root.iter('from'):
        email = child.find('email').text
        if email not in senders:
            senders[email] = 1
        else:
            senders[email] += 1
    print 'Top senders:'
    for k in sorted(senders, key=senders.get, reverse=True):
        if senders[k] >= 10:  #Only print if post count is at least 10
            padLen = 52-len(k)
            padding = ''.join([' ' for i in range(padLen)])
            print '',str(k)+':'+padding+str(senders[k])

def mostCommonWords(root):
    print 'Fifteen most common words:'

    words = {}
    for child in root.iter('message'):
        text = child.find('text').text.split()
        
        for word in text:
            word = word.encode('utf-8', 'ignore')
            if word not in words:
                words[word] = 1
            else:
                words[word] += 1

    i = 0
    for key in sorted(words, key=words.get, reverse=True):
        if i > 15:
            break
        print str(key)+':\t'+str(words[key])
        i += 1
    print ''

def mostCommonWordsByMonth(root):
    print 'Fifteen most common words by month:'
    
    dates = {}
    for child in root.iter('message'):
        yyyymm = child.find('received').find('date').text[:6]

        # Count the words for the current month
        date = {}
        text = child.find('text').text.split()

        for word in text:
            word = word.encode('utf-8', 'ignore')
            if word not in date:
                date[word] = 1
            else:
                date[word] += 1

        # Add the wordcount of the current month to the total
        if yyyymm not in dates:
            dates[yyyymm] = date
        else:
            dates[yyyymm].update(date)


    # Print the results in a readable manner
    months = {'01': 'January',
              '02': 'February',
              '03': 'March',
              '04': 'April',
              '05': 'May',
              '06': 'June',
              '07': 'July',
              '08': 'August',
              '09': 'September',
              '10': 'October',
              '11': 'November',
              '12': 'December' }

    for date in sorted(dates):
        i = 0

        yyyy = str(date)[:4]
        mm = str(date)[4:6]
        month = months[mm]

        print month,yyyy+':'

        for key in sorted(dates[date], key=dates[date].get, reverse=True):
            if i > 10:
                break

            # Separating year and month
            
                    
            print '\t'+key+':\t\t'+str(dates[date][key])
            i += 1
    print ''


def mostCommonWordsBySender(root):
    pass

### RUN PART ###
main()
