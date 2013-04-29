#!/bin/python

# change above line to point to local 
# python executable
#
#dependencies: Python
#
import sys
from pprint import pprint, pformat

def ensuredir(dir):
    import os
    if not os.path.exists(dir):
        os.makedirs(dir)

def main():
    import email, imaplib, os
    from email.parser import HeaderParser
    detach_dir = '/Users/username/Desktop/DEPOT' # directory where to save attachments (default: current)
    ensuredir(detach_dir)
    user = "YourGmailAccount@gmail.com"
    pwd = "PutYourPasswordHere"
    
    # connecting to the gmail imap server
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login(user,pwd)
    m.select("INBOX") # here you a can choose a mail box like INBOX instead
    # use m.list() to get all the mailboxes
    
    _, items = m.search(None, "ALL") # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
    items = items[0].split() # getting the mails id
    for emailid in items:
            mess, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
            email_body = data[0][1] # getting the mail content
            mail = email.message_from_string(email_body) # parsing the mail content to get a mail object
            headers = HeaderParser().parsestr(email_body, True)
            emaildate = email.Utils.parsedate(headers["date"])
            yearmonthfolder = str(emaildate[0]) + '-' + str(emaildate[1])
            
            
            #Check if any attachments at all
            if mail.get_content_maintype() != 'multipart':
                continue
            
            print emailid +  ": ["+mail["From"]+"] :" + mail["Subject"]
        
            # we use walk to create a generator so we can iterate on the parts and forget about the recursive headach
            for part in mail.walk():
                
                
                try:
                    # multipart are just containers, so we skip them
                    if part.get_content_maintype() == 'multipart':
                        continue
            
                    # is this part an attachment ?
                    if part.get('Content-Disposition') is None:
                        continue
            
                    filename = part.get_filename()
                    counter = 1
            
                    # if there is no filename, we create one with a counter to avoid duplicates
                    if not filename:
                        filename = 'part-%03d%s' % (counter, 'bin')
                        counter += 1
                    
                    dirpath = os.path.join(detach_dir, yearmonthfolder)
                    ensuredir(dirpath)
                    att_path = os.path.join(dirpath, filename)
                    
                    #Check if its already there
                    if not os.path.isfile(att_path) :
                        # finally write the stuff
                        body = part.get_payload(decode=True)
                        if body:
                            fp = open(att_path, 'wb')
                            fp.write(body)
                            fp.close()
                            if str(att_path).lower().endswith('.rar'):
#                                UnRAR2.RarFile(att_path).extract(overwrite=True, path=dirpath)
				unrar.RarFile(att_path).extract(overwrite=True, path=dirpath)
                                os.remove(att_path)
                        else:
                            print filename + " in " + mail["Subject"] + " is empty"
                except Exception, _:
                    print "error at message: " + mail["Subject"]

if __name__ == '__main__':
    main()

