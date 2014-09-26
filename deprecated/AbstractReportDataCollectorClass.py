
from ReportStructure import ReportStructure
from ReportData import ReportData
import logging

logger = logging.getLogger( '_DATACOL' )

class BadReportCollectorException( Exception ):
  pass

"""
  Abstract representation of ReportDataCollector class
  All specific ReportDataCollector classes will inherit from this one.
"""
class AbstractReportDataCollector( object ):
  
  """
    Initialize AbstractReportDataCollector class.
  """
  def __init__( self):
    super(AbstractReportDataCollector, self).__init__()
    self.ReportData = ReportData()
    self.ReportStructures = []
    self.lastReportName = ''
    logger.debug( 'Initializing ({})'.format( self ) )
    

  """
    Add report structure.
  """
  def addReportStructure( self, reportStructureName, reportStructure ):
    if self.ReportStructure.get( reportStructureName ):
      errorMsg = "Tried to add report structure for '{}'.  This report structure already exists.".format( reportStructureName)
      logger.critical( errorMsg )
      raise BadReportCollectorException( logMsg )
    self.ReportStructures[  reportStructureName ] = reportStructure
    
  """
    Return report structure requested ( or None )
  """
  def getReportStructure( self, reportStructureName ):
    return self.ReportStructures.get( reportStructureName )

  # getColumnByName( dataElementName, columnName, dataRowToParse )
  
  """
    Set up to process requested file.
  """
  def processFile( self, reportName, excludedTargets ):
    
    self.lastReportName = reportName
    

    # fetchDataMethods()
