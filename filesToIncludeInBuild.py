##################################
# filesToIncludeInBuild.py
# michael murphy 2015
##################################
# delete all files that are not 
# referenced in package.xml
##################################

from lxml import etree
import sys, os, getopt, re

_debug = False

def setup():
    ''' method to set up all global vars used '''
    
    global _debug
    _debug = False

def parseXml(xmlfile):
    ''' parse the XML file '''
    
    root = etree.XML(removeNamespaceReturnRoot(xmlfile))
    memberdict = {}

    # create a dict of name->members
    for i in root.iter("types"):
        # get the name tag
        name = i.find("name").text
        
        # get all members and add to dict
        memberdict[name] = [x.text for x in i.findall("members")]

    # look up the file extension (potentially can be omitted)
    # and the relative file path
    # for the current type name

    # for each type get contents of
    # folder as a list. if the list is
    # bigger than the dictionary list
    
    # delete the ones that do not match
    # a simple regex

def removeNamespaceReturnRoot(xmlfile):
    ''' read to string and remove the xmlns 
        because it just causes loads of issues '''

    xmldata = ""

    with open(xmlfile, "r") as myfile:
        xmldata = myfile.read()

    xmldata = re.sub('xmlns=".*"', '', xmldata, count=1)
    xmldata = re.sub('<\?.*\?>', '', xmldata, count=1)

    return xmldata


def removeFiles():
    ''' remove files from filesystem '''


def usage():
    ''' print usage info to command line '''
    
    print("usage")

def filesToIncludeInBuild(argv):
    ''' main function, get args and start doing stuff '''
    
    try:
        opts, args = getopt.getopt(argv, "-hp:d", ["help", "package="])
    except getopt.GetoptError:
        if _debug:
            print("getopt error")
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == "-d":
            global _debug
            _debug = True
        elif opt in ("-p", "--package"):
            if _debug:
                print("package arg found")
            if os.path.exists(arg):
                if _debug:
                    print("file found")
                parseXml(arg)
            else:
                print("file not found")

if __name__ == "__main__":
    ''' should have one argument for the location
        of the package.xml file for us to parse
        if this is not present then assume in same dir '''

    setup()

    if len(sys.argv) > 1:
        filesToIncludeInBuild(sys.argv[1:])
    else:
        if _debug:
            print("not enough args")
        usage()
