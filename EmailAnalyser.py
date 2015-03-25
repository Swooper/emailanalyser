# -*- coding: utf-8 -*-
# Haukur Jónasson
# Tryggvi Þór Guðmundsson

import xml.etree.cElementTree as ET
import os

def main():
    location = '..'+os.sep+'bluecloak3'
    fileName = 'messages.xml'

    print 'Building tree...'
    tree = ET.parse(location+os.sep+fileName)
    print ' > Tree built.'

    root = tree.getroot()

    totalEmails(root)
    reAndFwdCounts(root)
    countByMonth(root)
    countBySender(root)

def totalEmails(root):
    print 'Counting...'
    counter = 0
    for child in root.iter('subject'):
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

    for key in sorted(dates):
        # Seperating year and month
        yyyy = str(key)[:4]
        mm = str(key)[4:6]
        month = months[mm]
                
        print month,yyyy+':\t\t'+str(dates[key])

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

### RUN PART ###
main()
