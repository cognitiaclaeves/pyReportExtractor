
from AbstractReportDataCollectorClass import AbstractReportDataCollectorClass
import logging

class SampleDataCollectorClass( AbstractReportDataCollectorClass ):

  def __init__( self ):
    super( SampleDataCollectorClass, self ).__init__()
    self.logger = logging.getLogger( 'DATACOLL' )
    self.logger.debug( 'Initializing {}'.format( self ) )
