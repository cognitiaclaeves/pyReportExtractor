
# Copyright 2014 Douglas J. Norment for SourceApprentice
# http://www.sourceapprentice.com

import logging

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
  def __init__( self ):
    self.DataGroupStructures = []
    logger.debug( 'Initializing: {}'.format( self ) )
  

  def getDataGroupStructure( self, dataGroupName ):
    return self.DataGroupStructures[ dataGroupName ]
    
  """
    Creates and Returns new Data Element Structure
  """
  def createDataGroupStructure( self, dataGroupName ):
    newDataGroupStructure = self.DataGroupStructures.get( dataGroupName )
    if newDataGroupStructure:
      errMsg='Tried to create a new data element structure with name that already exists: {}'.format( dataGroupName )
      logger.critical( errMsg )
      raise DataGroupStructureAlreadyExists( errMsg )
    newDataGroupStructure = []
    self.DataGroupStructures[ dataGroupName ] = newDataGroupStructure
    return newDataGroupStructure

  """
    Sets column in data element structure
  """
  def setDataColumnStructure( self, dataGroupName, columnName, structureTuple ):
    newDataGroupColumn = self.getDataColumnStructure( dataGroupName, columnName )
    if newDataGroupColumn:
      errMsg="Tried to create {} in data element structure {}.  Column already exists.".format( columnName, dataGroupName )
      logger.critical( errMsg )
      raise ColumnAlreadyExistsInDataGroupStructure( errMsg )
      
    self.DataGroupStructures[ dataGroupName ][ columnName ] = structureTuple
    
  """
    Get structure for column name given
  """
  def getDataColumnStructure( self, dataGroupName, columnName ):
      if not self.DataGroupStructures.get( dataGroupName ):
        errMsg="Tried to get data element structure that didn't exist: {}".format( dataGroupName )
        logger.critical( errMsg )
        raise BadDataGroupStructureRequest( errMsg )
      return self.DataGroupStructures.get( dataGroupName ).get( columnName )

