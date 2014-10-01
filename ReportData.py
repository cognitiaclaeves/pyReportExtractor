
# Copyright 2014 Douglas J. Norment for SourceApprentice
# http://www.sourceapprentice.com

import logging
logger=logging.getLogger('main.RPT_DATA')

class DataGroupAlreadyExists ( Exception ):
  pass


class ReportData ( object ):


  """
    Initialize class
  """
  def __init__( self ):
    self.DataGroups = []
    # self.DataGroups [ DataGroupName ]= [ dataStructure ( column structure ), [ rows of data ] ]
    logger.debug('Initializing: {}'.format( self ) )


  """
    Returns new data element
  """
  def createDataGroup( self, DataGroupName, dataStructure ):
    newDataGroup = self.DataGroups.get( DataGroupName )
    if newDataGroup:
      raise DataGroupAlreadyExists( 'Tried to create data element when it already existed.' )
    newDataGroup = [ [dataStructure,], [] ] # seed column structure for datagroup into [0][0], [1] will be list of all rows in datagroup
    self.DataGroups[ DataGroupName ] = newDataGroup
    return newDataGroup

  """
    Returns data element [] requested, or None
  """
  def getDataGroup( self, DataGroupName ):
    return self.DataGroups.get( DataGroupName )[1]
    
  """
    Stores and returns new data row
  """
  def createNewDataRow( self, DataGroupName, reportRowNumber, dataTuple ):
    columnStructureForDatagroup=self.DataGroups[ DataGroupName ][0][0]
    newDataRowID = len( self.DataGroups[ DataGroupName ][1] )
  
    logger.debug( 'DataStructureID', self.DataGroups[ DataGroupName ][0][0] )

    newDataRow = [ [columnStructureForDatagroup, newDataRowID, reportRowNumber], dataTuple ]

    logger.debug( 'columnStructureID', newDataRow[0][0] )
    
    # hopefully those are the same... list object linked to both references, rather than copied
    
    # newDataRow = [ [None, -1, -1 ], [] ] # [ ColumnStructure-for-dataGroup, DataRowID, ReportRowID ]
    # # set the data structure
    # newDataRow[0][0] = self.DataGroups[ DataGroupName[0] ]
    # # set the data row number
    # newDataRow[0][1]=len( self.DataGroups[ DataGroupName ] )
    # # set the original report row number

    self.DataGroups[ DataGroupName ][1].append( newDataRow )
    
    return newDataRow
    

