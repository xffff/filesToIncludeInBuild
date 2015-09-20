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
    
    # get all types
    for child in root:
        for subchild in child:
            print(subchild.tag, subchild.text)


    # look up the file extension
    # look up the file path
    # for the current type name

    # create array of members that should exist

    # iterate through and create list of files
    # that actually exist on the file system

    # if members do not exist, delete
    # the files that should not be there

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
