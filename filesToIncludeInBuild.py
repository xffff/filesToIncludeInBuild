##################################
# filesToIncludeInBuild.py
# michael murphy 2015
##################################
# delete all files that are not 
# referenced in package.xml
##################################

from lxml import etree
import sys, os, getopt, re

def setup():
    ''' method to set up all global vars used '''
    global _debug
    _debug = False

def parseXml(xmlfile):
    ''' parse the XML file '''
    
    if _debug:
        print("parsing: {0}".format(xmlfile))

    root = etree.XML(removeNamespaceReturnRoot(xmlfile))
    typememberdict = {}

    # create a dict of name->members
    for i in root.iter("types"):
        # get the name tag
        name = i.find("name").text
        members = [x.text for x in i.findall("members")]

        if _debug:
            print("typememberdict[{0}] : {1}".format(name, members))
              
        # get all members and add to dict
        typememberdict[name] = members

    # look up the file extension (potentially can be omitted)
    # and the relative file path for the current type name
    # from the XML config file specified in the argument... 
    pass # @TODO


    # for each type get contents of
    # folder as map
    typefoldercontentsdict = getFolderContents()

    # delete the ones that do not match
    removeFiles()

def getFolderContents(typememberdict, typefilepathdict):
    ''' using the typememberdict keyset as a hook
        for each type, get the contents of the folder
        specified for this type by the typefilepathdict '''
    

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
    ''' remove files from filesystem 
        first check for each key whether the value list is the same size
        if it isnt then sort both value lists so they are ordered sets
        then iterate through and compare each value
        if a != b then delete b from the filesystem'''


def usage():
    ''' print usage info to command line '''
    print("usage")

def filesToIncludeInBuild(argv):
    ''' main function, get args and start doing stuff '''

    try:
        opts, args = getopt.getopt(argv, "-hp:d", ["help", "package="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        print(opt, arg)
        
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == "-d":
            _debug = True
        elif opt in ("-p", "--package"):
            if _debug:
                print("package arg found")
            if os.path.exists(arg):
                if _debug:
                    print("file found: {0}".format(arg))
                    
                parseXml(arg)
            else:
                print("file not found")
        else:
            print("package xml path not specified")

if __name__ == "__main__":
    ''' should have one argument for the location
        of the package.xml file for us to parse
        if this is not present then assume in same dir '''

    setup()

    if len(sys.argv) > 1:
        filesToIncludeInBuild(sys.argv[1:])
    else:
        usage()
