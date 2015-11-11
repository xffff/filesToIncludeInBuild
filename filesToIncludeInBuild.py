##################################
# filesToIncludeInBuild.py
# michael murphy 2015
##################################
# delete all files that are not 
# referenced in package.xml
##################################

from lxml import etree
import sys, os, re, argparse

def parseXml(rootdir, packagexml, configxml):
    ''' parse the XML file '''
    global _debug
    
    if _debug:
        print("parsing: {0}".format(packagexml))

    typememberdict = {}
    typefileextdict = {}
    typefilepathdict = {}
    root = etree.XML(removeNamespaceReturnRoot(packagexml))
    configroot = etree.XML(removeNamespaceReturnRoot(configxml))

    # create a dict of name->members
    for i in root.iter("types"):
        # get the name tag
        name = i.find("name").text
        members = [x.text for x in i.findall("members")]
        typememberdict[name] = members

    # look up the file extension (potentially can be omitted)
    # and the relative file path for the current type name
    # from the XML config file specified in the argument...
    for i in configroot.iter("types"):
        # get the tag for the file extension
        try:
            name = i.find("name").text
            extension = i.find("extension").text
            folder = i.find("folder").text
        except Exception as e:
            sys.exit("Error reading file: {0}".format(e.args))

        typefilepathdict[name] = os.path.join(rootdir, folder)
        typefileextdict[name] = extension
        
    # for each type get contents of folder as map
    typefoldercontentsdict = getFolderContents(typememberdict, \
                                               typefilepathdict)

    if _debug:
        print("typefoldercontentsdict: {0}" \
              .format(typefoldercontentsdict.items()))
        print("typememberdict: {0}" \
              .format(typememberdict.items()))
        print("typefileextdict: {0}" \
              .format(typefileextdict.items()))
    
    # delete the ones that do not match
    removeFiles()

def getFolderContents(typememberdict, typefilepathdict):
    ''' using the typememberdict keyset as a hook
        for each type, get the contents of the folder
        specified for this type by the typefilepathdict '''
    
    typefoldercontentsdict = {}
    
    for k, v in typememberdict.items():
        try:
            filepath = typefilepathdict[k]
            if _debug:
                print("filepath: {0}".format(filepath))
        
            typefoldercontentsdict[k] = os.listdir(filepath)
        except KeyError as e:
            print("Failed to get key: {0}".format(e.args))

    return typefoldercontentsdict
    

def removeNamespaceReturnRoot(packagexml):
    ''' read to string and remove the xmlns 
        because it just causes loads of issues '''

    xmldata = ""

    with open(packagexml, "r") as myfile:
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
    global _debug
    _debug = False
    packagexml = configxml = rootdir = None
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-p"                                              
                        , "--package"                                     
                        , type=str                                        
                        , help="the package xml file")
    parser.add_argument("-c"                                              
                        , "--config"                                      
                        , type=str                                        
                        , help="the config xml file")
    parser.add_argument("-r"                                              
                        , "--root"                                        
                        , type=str                                        
                        , help="the root directory")
    parser.add_argument("-d"                                              
                        , "--debug"
                        , dest="_debug"
                        , action="store_true"                             
                        , help="turn on debug mode, this is very verbose" 
                        , default=False)
    args = parser.parse_args()

    if args.package == None or args.config == None or args.root == None:
        sys.exit("you forgot package, config, or root directory parameters")
    
    if not os.path.exists(args.package):
        sys.exit("the package file doesnt exist")
    if not os.path.exists(args.config):
        sys.exit("the config file doesnt exist")
    if not os.path.exists(args.root):
        sys.exit("the root folder doesnt exist")


if __name__ == "__main__":
    ''' should have one argument for the location
        of the package.xml file for us to parse
        if this is not present then assume in same dir '''

    filesToIncludeInBuild(sys.argv[1:])
