##################################
# filesToIncludeInBuild.py
# michael murphy 2015
##################################
# delete all files that are not 
# referenced in package.xml
##################################

from lxml import etree
import sys, os, re, argparse

_debug = False

def parseXml(rootdir, packagexml, configxml):
    ''' parse the XML file '''
    global _debug
    
    if _debug:
        print("parsing: {0}".format(packagexml))

    typememberdict = {}
    typefileextdict = {}
    typefilepathdict = {}

    root = etree.XML(removeNamespaceReturnRoot(packagexml))
    packageroot = etree.XML(removeNamespaceReturnRoot(packagexml))
    configroot = etree.XML(removeNamespaceReturnRoot(configxml))
    
    # create a dict of name->members
    for i in packageroot.iter("types"):
        # get the name tag
        name = i.find("name").text
        members = [x.text for x in i.findall("members")]

        if _debug:
            print("typememberdict[{0}] = {1}".format(name, members))

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
            
            typefilepathdict[name] = os.path.join(rootdir, folder)
            typefileextdict[name] = extension

            if _debug:
                print("Join paths: {0} + {1} = {2}"   \
                      .format(rootdir, folder, os.path.join(rootdir, folder)))
                print("File extension for {0} is {1}" \
                      .format(name, extension))
        except Exception as e:
            sys.exit("Error reading file: {0}".format(e.args))
    
    #for each type get contents of folder as map
    typefoldercontentsdict = getFolderContents(typememberdict
                                               , typefilepathdict)

        
    if _debug:
        print("typefilepathdict: {0}"       \
              .format(typefilepathdict.items()))
        print("typefoldercontentsdict: {0}" \
              .format(typefoldercontentsdict.items()))
        print("typememberdict: {0}"	    \
              .format(typememberdict.items()))
        print("typefileextdict: {0}"	    \
              .format(typefileextdict.items()))

    # delete the ones that do not match
    removeFiles(typefoldercontentsdict, typememberdict, typefilepathdict, typefileextdict)

def getFolderContents(typememberdict, typefilepathdict):
    ''' using the typememberdict keyset as a hook
        for each type, get the contents of the folder
        specified for this type by the typefilepathdict '''
    
    typefoldercontentsdict = {}
    
    for k, v in typememberdict.items():
        try:
            filepath = typefilepathdict[k]
            if "*" not in filepath:
                if _debug:
                    print("filepath: {0}".format(filepath))
                    typefoldercontentsdict[k] = os.listdir(filepath)
        except KeyError as e:
            ''' we could save these and use them later
                probably for something else like knowing
                that they can be deleted... hooray '''
            print("No key: {0} for type member dict".format(e.args))

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


def removeFiles(typefoldercontentsdict, typememberdict, typefilepathdict, typefileextdict):
    ''' remove files from filesystem 
        first check for each key whether the value list is the same size
        if it isnt then sort both value lists so they are ordered sets
        then iterate through and compare each value
        if a != b then delete b from the filesystem '''

    for k, v in typefoldercontentsdict.items():
        if _debug:
            print("key: {0}, value: {1}".format(k, v))

        if k not in typememberdict.keys():
            if _debug:
                print("key: {0} not in {1}".format(k, typememberdict.keys()))

            # delete all files in the directory
            pass 
        else:
            # if the members contain the element * 
            # then we want to keep everything dont we
            if "*" not in typememberdict[k]:
                # otherwise sort the lists
                typefolderlist = v                
                typememberlist = [i + "." + typefileextdict[k] for i in typememberdict[k]]
                typemetalist = [i + "-meta.xml" for i in typememberlist]
                
                typefolderlist.sort()
                typememberlist.sort()

                if _debug:
                    print('''typefolderlist: {0}
                    	     \ntypememberlist: {1}
                    	     \ntypemetalist: {2}''' \
                          .format(typefolderlist
                                  , typememberlist
                                  , typemetalist))

                print("typefolderlist: {0}, typememberlist: {1}" \
                      .format(typefolderlist, typememberlist))

                # if a file is not in the package xml but
                # is in the filesystem, it should be deleted
                # so it does not appear in the build
                for i in typefolderlist:
                    if i not in typememberlist and i not in typemetalist:
                        try:
                            print("deleting: {0}/{1}".format(typefilepathdict[k], i))

                            # actually do the delete
                            os.remove(typefilepathdict[k], i)
                        except Exception as e:
                            sys.exit("typefilepathdict exception: {0}".format(e.args))
                            

def usage():
    ''' print usage info to command line '''
    print("usage")

def filesToIncludeInBuild(argv):
    ''' main function, get args and start doing stuff '''
    global _debug
    _debug = True
    packagexml = None
    configxml = None
    rootdir = None
    
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
                        , default=True)
    args = parser.parse_args()
    
    if args.package == None or args.config == None or args.root == None:
        sys.exit("you forgot package, config, or root directory parameters")
    
    if not os.path.exists(args.package):
        sys.exit("the package file doesnt exist")
    if not os.path.exists(args.config):
        sys.exit("the config file doesnt exist")
    if not os.path.exists(args.root):
        sys.exit("the root folder doesnt exist")

    parseXml(args.root, args.package, args.config)

        
if __name__ == "__main__":
    ''' should have one argument for the location
        of the package.xml file for us to parse
        if this is not present then assume in same dir '''

    filesToIncludeInBuild(sys.argv[1:])
