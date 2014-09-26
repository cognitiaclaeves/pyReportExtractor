
# Copyright 2014 Douglas J. Norment for SourceApprentice
# http://www.sourceapprentice.com

from AbstractReportDataCollector import AbstractReportDataCollector
import logging

logger=logging.getLogger( 'main.DATACOLL' )

class SampleDataCollector( AbstractReportDataCollector ):

  def __init__( self ):
    super( SampleDataCollector, self ).__init__()
    logger.debug( 'Initializing {}'.format( self ) )
