#! /usr/local/bin/python3
#! /usr/bin/python3

import os
import subprocess
import difflib
import argparse

#
#  Argument Parser
#

parser = argparse.ArgumentParser(
    "A test driver for the DataMgr and Grid classes"
)
parser.add_argument( 
    '--makeBaseline', 
    nargs=1,
    type=str,
    default=False, 
    required=False,
    metavar='false',
    help='Boolean that makes these test results the baseline on which future'
    + ' tests will be compared.  If no baseline file exists, this will automatically '
    + ' be set to true.'
)
parser.add_argument( 
    '--testDataRoot', 
    nargs=1,
    type=str,
    default="/Users/pearse/Data/smokeTestData/", 
    required=False,
    metavar='/path/to/data',
    help='Directory where DataMgr test data is stored.'
)
parser.add_argument( 
    '--binaryRoot', 
    nargs=1,
    type=str,
    default="/Users/pearse/VAPOR/build/bin", 
    required=False,
    metavar='/path/to/binaries',
    help='Directory where binary test programs (testGrid, testDataMgr) are stored.'
)
args = parser.parse_args()

#
#  Default directories and test data
#

gridSizes = [
    "1x1x1",
    "1x8x8",
    "8x1x8",
    "8x8x1",
    "7x7x7",
    "8x8x8"
]

resultsDir = "testResults/"

dataMgrs = {
    #"mpas" : (args.testDataRoot + "hist.mpas-o.0001-01-01_00.00.00.nc")
    "wrf"  : (args.testDataRoot + "wrfout_d02_2005-08-29_05"),
    "cf"   : (args.testDataRoot + "24Maycontrol.04000.000000.nc"),
    "vdc"  : (args.testDataRoot + "katrina_1timeStep.vdc"),
}

gridProgram        = args.binaryRoot + "/testGrid"
dataMgrProgram     = args.binaryRoot + "/testDataMgr"
gridResultsFile    = resultsDir + "gridResults.txt"
dataMgrResultsFile = resultsDir + "dataMgrResults.txt"

#
#  Tests
#


def testGrid( grid ):
    print( "Testing " + grid + " grid" )

    print( gridProgram + " -dims " + grid )
    #programOutput  = subprocess.check_output( [ gridProgram, " -dims ", grid ] )
    #programOutput  = subprocess.run( [ gridProgram, " -dims ", grid ], encoding="utf-8" )
    programOutput  = subprocess.run( 
        [ gridProgram, " -dims ", grid ], 
        stdout=subprocess.PIPE,  
        universal_newlines=True 
    )

    print( "  Exit code " + str(programOutput.returncode) )

    outputFileName = resultsDir + grid + ".txt"
    
    outputFile = open( outputFileName, "w" )
    #outputFile.write( programOutput.decode("utf-8") )
    outputFile.write( programOutput.stdout )
    outputFile.close()
    
    print( "  " + outputFileName + " written\n" )

def testDataMgr( dataMgrType, dataMgr, makeBaseline=False ):
    print( "Testing " + dataMgrType + " with " + dataMgr )
    
    command = [ dataMgrProgram, "-fileType", dataMgrType, dataMgr ]
    programOutput = subprocess.check_output( command )
    
    if ( makeBaseline ):
        outputFileName = resultsDir + dataMgrType + "_baseline.txt"
    else:
        outputFileName = resultsDir + dataMgrType + ".txt"

    outputFile = open( outputFileName, "w" )
    outputFile.write( programOutput.decode("utf-8") )
    outputFile.close()
    
    print( "  " + outputFileName + " written\n" )

    return outputFileName

def testDataMgrs( makeBaseline ):
    if ( makeBaseline ):
        diff = open( dataMgrResultsFile, "w" )
    else:
        diff = open( dataMgrResultsFile, "a" )
    
    mismatches = 0

    for dataType, dataFile in dataMgrs.items():

        # If we're making a baseline file, generate it, and then skip comparisons 
        if ( makeBaseline ):
            resultsFile = testDataMgr( dataType, dataFile, makeBaseline )
            continue

        resultsFile = testDataMgr( dataType, dataFile )
        
        baselineFile = resultsDir + dataType + "_baseline.txt"
        baseline = open( baselineFile, "r" )
        results  = open( resultsFile, "r" )
        
        # Note - we are not reading the last line of these files, since it's the
        # runtime for the test ( hence the [:-1] specification )
        baselineLines = baseline.readlines()[:-1]
        resultsLines = results.readlines()[:-1]
        
        for line in difflib.unified_diff(resultsLines, baselineLines, resultsFile, baselineFile):
            diff.write( line )
            mismatches+=1

        baseline.close()
        results.close()
    diff.close()

    if ( makeBaseline == False ):    
        print( dataMgrResultsFile + " written" )
        print( "    DataMgr tests resulted in " + str(mismatches) + " mismatches" )
    else:
        print( "Baseline files have been generated.  Re-run smokeTests.py to run comparions.\n" )

    if ( mismatches > 0 ):
        return -1
    else:
        return 0
        
def main():
    print()
    makeBaseline = args.makeBaseline

    if ( args.makeBaseline == False and makeBaseline == True ): 
        print( "    Warning: Some or all baseline files for running DataMgr testswere missing.  "
               "    These files are needed as comparisons for the results of the current series "
               "    of tests, versus a known working build (the baseline).\n"
               "       Setting --makeBaseline to True.\n"
        )

    if ( os.path.isdir( resultsDir ) == False ):    
        os.mkdir( resultsDir )

    for grid in gridSizes:
        testGrid( grid )

    for dataType, dataFile in dataMgrs.items():
        baselineFile = resultsDir + dataType + "_baseline.txt"
        if ( os.path.isfile( baselineFile ) == False ):
            makeBaseline = True
        continue
   
    #dataMgr = testDataMgrs( makeBaseline )

if __name__ == "__main__":
    main()
