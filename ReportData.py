
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
		logger.debug('Initializing: {}'.format( self ) )
		# Data [ DataGroupName ]= [ dataStructure, [ lines of data ] ]

	"""
		Returns new data element
	"""
	def createDataGroup( self, DataGroupName, dataStructure ):
		newDataGroup = self.DataGroups.get( DataGroupName )
		if newDataGroup:
			raise DataGroupAlreadyExists( 'Tried to create data element when it already existed.' )
		newDataGroup = [ dataStructure, [] ]
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
		newDataRow = [ [None, -1, -1 ], [] ]
		# set the data structure
		newDataRow[0][0] = self.DataGroups[ DataGroupName[0] ]
		# set the data row number
		newDataRow[0][1]=len( self.DataGroups[ DataGroupName ] )
		# set the original report row number
		self.DataGroups[ DataGroupName ][1].append( newDataRow )
		
		return newDataRow
		
