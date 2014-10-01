
# Copyright 2014 Douglas J. Norment for SourceApprentice
# http://www.sourceapprentice.com

import logging
from ReportDataGroup import ReportDataGroup


class DataGroupStructureAlreadyExists( Exception ):
  pass

class ColumnAlreadyExistsInDataGroupStructure( Exception ):
  pass

class BadDataGroupStructureRequest( Exception ):
  pass



logger=logging.getLogger('main.RPTSTRCT')


"""
  Abstract Report Structure Class
"""

class AbstractReportStructure( object ):
  
  """
    Initialize AbstractReportStructureClass
  """
  def __init__( self, reportName ):
    self.reportName = reportName
    self.DataGroupStructures = {}
    logger.debug( 'Initializing: {}'.format( self ) )
  

  """
    Return dataGroupStructure requested, or None, if it doesn't exist
  """
  def getDataGroupStructure( self, dataGroupName ):
    return self.DataGroupStructures.get( dataGroupName )
    
  """
    Creates and Returns new Data Element Structure
  """
  def createDataGroupStructure( self, dataGroupName ):
    newDataGroupStructure = self.DataGroupStructures.get( dataGroupName )
    if newDataGroupStructure:
      errMsg='Tried to create a new data element structure with name that already exists: {} for report ({})'.format( dataGroupName, self.reportName )
      logger.critical( errMsg )
      raise DataGroupStructureAlreadyExists( errMsg )
      
    newDataGroupStructure = ReportDataGroup( self.reportName, dataGroupName )
    self.DataGroupStructures[ dataGroupName ] = newDataGroupStructure
    logger.debug("+ ({}) {}={}".format( self.reportName, dataGroupName, self.DataGroupStructures[ dataGroupName ] ) )
    return newDataGroupStructure

  """
    Sets column in data element structure
  """
  def createDataColumnStructure( self, dataGroupName, columnName, structureTuple ):
    newDataGroupColumn = self.getDataColumnStructure( dataGroupName, columnName )
    if newDataGroupColumn:
      errMsg="Tried to create {} in data element structure {} in ({}).  Column already exists.".format( columnName, dataGroupName, self.reportName )
      logger.critical( errMsg )
      raise ColumnAlreadyExistsInDataGroupStructure( errMsg )
      
    self.DataGroupStructures[ dataGroupName ].columns[ columnName ] = structureTuple
    
    stu = self.DataGroupStructures[ dataGroupName ].columns[ columnName ]
    
    logger.debug("+ ({}) {}.{}={}".format( self.reportName, dataGroupName, columnName, stu ) )
    return stu
    
  """
    Get structure for column name given, or None if column doesn't exist
  """
  def getDataColumnStructure( self, dataGroupName, columnName ):
      if not self.DataGroupStructures.get( dataGroupName ):
        errMsg="Tried to get data element structure that didn't exist: {}".format( dataGroupName )
        logger.critical( errMsg )
        raise BadDataGroupStructureRequest( errMsg )
      return self.DataGroupStructures.get( dataGroupName ).columns.get( columnName )


  def dumpReportStructure( self ):

      # Return report structure as YAML:
      
      returnString=[]
    
      tab=' '*3 # YAML doesn't seem to recognize tabs as whitespace
    
      for eachDataGroupName in sorted(self.DataGroupStructures):
        returnString.append( "{}{}{}:\n".format( tab,tab,eachDataGroupName ) )
        
        for eachColumn in sorted(self.DataGroupStructures[eachDataGroupName].columns):
          returnString.append( "{}{}{}{}: {}\n".format(tab,tab,tab,eachColumn, str(self.DataGroupStructures[eachDataGroupName].columns[eachColumn]).replace("'",'') ) )
        returnString.append("\n")
        
      return ''.join( returnString )

