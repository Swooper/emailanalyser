# -*- coding: utf-8 -*-
# Haukur Jónasson
# Tryggvi Þór Guðmundsson

import xml.etree.cElementTree as ET

def main():
    fileName = 'messages.xml'
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

    print 'Building tree...'
    tree = ET.parse(fileName)
    print ' > Tree built.'
    print ''

    
    
    root = tree.getroot()

    totalEmails(root)
    totalWords(root)
    reAndFwdCounts(root)
    countByMonth(root, months)
    countBySender(root)
    mostCommonWords(root)
    mostCommonWordsByMonth(root, months)
    mostCommonWordsNoYear(root, months)

def totalEmails(root):
    print ''
    print 'Counting...'
    counter = 0
    for child in root.iter('message'):
        counter+=1
    print 'Total emails:',counter 

def totalWords(root):
    count = 0
    for child in root.iter('message'):
        text = child.find('text').text.split()
        for word in text:
            count += 1
    print ''
    print 'Total words:',count

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
    print ''
    print 'Replies:',replyCounter
    print 'Forwards:',fwdCounter

def countByMonth(root, months):
    print ''
    print 'Counting emails by month...'
    dates = {}
    for child in root.iter('date'):
        yyyymm = child.text[:6]
        if yyyymm not in dates:
            dates[yyyymm] = 1
        else:
            dates[yyyymm] += 1

    newyear = ''
    for key in sorted(dates):
        # Seperating year and month
        yyyy = str(key)[:4]
        mm = str(key)[4:6]
        if yyyy != newyear:
            print '\n'+yyyy+':'
        newyear = yyyy
        month = months[mm]
        padLen = 15-len(month)
        padding = ''.join([' ' for x in range(padLen)])
        print '\t'+month+':'+'\t\t'+str(dates[key])
    print ''

def countBySender(root):
    print ''
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
            print str(k)+':'+'\t\t'+str(senders[k])

def mostCommonWords(root):
    print ''
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
        if i >= 15:
            break
        print str(key)+':\t'+str(words[key])
        i += 1
    print ''

def mostCommonWordsByMonth(root, months):
    print ''
    print 'Ten most common words by month:'
    
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
    for date in sorted(dates):
        # Seperating month and year
        yyyy = str(date)[:4]
        mm = str(date)[4:6]
        month = months[mm]

        print month,yyyy+':'
        i = 0
        for key in sorted(dates[date], key=dates[date].get, reverse=True):
            if i >= 1:
                break

            padLen = 52-len(key)
            padding = ''.join([' ' for x in range(padLen)])
            print '\t'+key+': '+'\t\t'+str(dates[date][key])
            i += 1
    print ''

def mostCommonWordsNoYear(root, months):
    print 'Ten most common words by month, no year:'
    
    mons = {}
    for child in root.iter('message'):
        mm = child.find('received').find('date').text[4:6]

        # Count the words for the current month
        mon = {}
        text = child.find('text').text.split()

        for word in text:
            word = word.encode('utf-8', 'ignore')
            if word not in mon:
                mon[word] = 1
            else:
                mon[word] += 1

        # Add the wordcount of the current month to the total
        if mm not in mons:
            mons[mm] = mon
        else:
            for m in mons:
                for word in mon:
                    if word not in mons[mm]:
                        mons[mm][word] = 1
                    else:
                        mons[mm][word] += 1


    # Print the results in a readable manner
    for m in sorted(mons):
        i = 0

        mm = str(m)
        month = months[mm]
        print month+':'

        for key in sorted(mons[m], key=mons[m].get, reverse=True):
            if i >= 10:
                break
            
            # Separating year and month
            padLen = 52-len(key)
            padding = ''.join([' ' for x in range(padLen)])
            print '\t'+key+':'+'\t\t'+str(mons[m][key])
            i += 1
    print ''

### RUN PART ###
main()
