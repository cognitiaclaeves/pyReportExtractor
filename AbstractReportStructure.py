
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
      
    #logger.critical( "{},{}".format( self.reportName, dataGroupName) )
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
    
      returnString=[]
    
      for eachDataGroupName in sorted(self.DataGroupStructures):
        returnString.append( "'{}': {{".format( eachDataGroupName ) )
        
        for eachColumn in sorted(self.DataGroupStructures[eachDataGroupName].columns):
          returnString.append( "'{}': {},".format(eachColumn, self.DataGroupStructures[eachDataGroupName].columns[eachColumn] ) )
        returnString.append("},")
        
      return ''.join( returnString )
    


# {'ColumnStructures':
# - {'ReportName1': {
#  'dataGroup1': {'columnName1': [0, 1],
#                 'columnName2': [1, '-', 15]},
#  'dataGroup2': {'columnName3': [0, 2]}
# - },
# - 'ReportName2': {
#  'dataGroup3': {'columnName1': [0, 1]}
# - }
# - },

