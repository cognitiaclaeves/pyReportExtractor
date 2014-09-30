
# Copyright 2014 Douglas J. Norment for SourceApprentice
# http://www.sourceapprentice.com

import sys
import os
import logging
import logging.config
import yaml

class BadConfigException( Exception ):
  pass


class DataCollectorRunner( object ):
  
  def __init__( self):
    pass

  # Set configuration from caller
  def set_config( self, config ):
    self.config = config
    self.datacollector = None
    self.dynamic_modules = []

  """
    Dynamically initialize data collector defined in config file.
    Since the user is being relied upon to enter the module and class in a config file,
      ( and to create new class files for data collectors ),
      There is some effort to protect the user from themself.
  """
  def initialize_dataCollector( self ):
    
    dataCollectorClassname = self.config['Control']['ReportCollectorClass']
    logger.debug( "Data collector module.class: {}".format( dataCollectorClassname ))
  
    # This will load multiple modules, but then the classes need to be instantiated
    moduleNames=[ dataCollectorClassname.split('.')[0], ]
    
    try:
      self.dynamic_modules=map( __import__, moduleNames )
      
      # Reload module to ensure that any changes that would cause errors at class load are caught
      # ( This actually "double-loads" the module, but if it isn't done this way, then Python's 'lazy-load'
      #   may not catch changes made to the imported module. )
      
      reload( self.dynamic_modules[0] )
      
      # Note: I'm not up to date on the issues ( such as memory leaks ) that can be caused by reloading the module
      #       programatically, however, I think it should be fine, in this, case, as this script is not always running
      #       with the same python kernel.
  
    except ImportError:
      errMsg = "Bad module name in config file: {}".format( dataCollectorClassname.split('.')[0] )
      logger.critical( errMsg )
      raise BadConfigException( errMsg )
    except KeyboardInterrupt:
      raise
    except Exception, e:
      # Since part of the design is to have custom DataCollectorClasses, provide friendly message if it can't be imported.
      errMsg = "Custom data collector class is too broken to import."
      logger.exception( errMsg )
      raise e
    
    logger.debug( 'Modules: {}'.format( self.dynamic_modules ))
    
    try:
      self.dataCollector=getattr(self.dynamic_modules[0], dataCollectorClassname.split('.')[-1] )()
    except AttributeError:
      # Since the module and class are specified in a config file, provide friendly message if class has a bad name.
      errMsg = "Bad class name in config file: {}".format( dataCollectorClassname.split('.')[-1] )
      logger.critical( errMsg )
      raise BadConfigException( errMsg )
    except KeyboardInterrupt:
      raise
    except Exception, e:
      # Since part of the design is to have custom DataCollectorClasses, provide friendly message if it can't be instantiated.
      errMsg = "Custom data collector class is too broken to instantiate."
      logger.exception( errMsg )
      raise e
    
    logger.info( 'DataCollector Class Instantiated: {}'.format( self.dataCollector ) )
  
  
  """
    Validate working paths exist.
    ( I like to create the conditions for success if they are not already in place. )
  """
  def validate_working_paths( self ):
    self.input_path = self.config['Control']['InputPath']
    self.work_path = self.config['Control']['WorkPath']
  
    def checkPath( aPath ):
      
      if not os.path.isdir( aPath ):
        logger.warn( 'Cannot find working path: {}.'.format( os.path.abspath( aPath ) ) )
        try:
          os.mkdir( aPath )
        except:
          pass
        
        if not os.path.isdir( aPath ):
          errMsg = 'Unable to create path: {}.'.format( os.path.abspath( aPath ))
          logger.critical( errMsg )
          raise RuntimeError( errMsg )
        else:
          logger.debug( 'Successfully created path: {}.'.format( os.path.abspath( aPath )))
      else:
        logger.debug( 'Validated path: {} exists.'.format( os.path.abspath( aPath )))
      
    checkPath( self.input_path )
    checkPath( self.work_path )
    
  
  """
    Load manually defined column structures.
  """
  def load_column_structures( self ):
    
    column_structures = self.config['ColumnStructures']
    
    for eachReportKey in column_structures:
        print eachReportKey, cs[ eachReportKey ]
        logger.debug( "Creating report structure: {}".format( eachReportKey ) )
        self.dataCollector.
      
        
        
        dataGroups = cs[ eachReportKey ]
        for eachDataGroupKey in dataGroups:
            print eachDataGroupKey, dataGroups[ eachDataGroupKey ]
            dataColumns = dataGroups[ eachDataGroupKey ]
            for eachColumn in dataColumns:
                print eachColumn, dataColumns[ eachColumn ]
    
    
    
    for eachReportName in column_structures:
      logger.warn( 'report name: {}'.format ( column_structures( eachReportName ) ) )
      data_groups = column_structures( eachReportName )
      for eachDataGroup in data_groups:
        logger.warn( 'data group: {}'.format ( data_groups( eachDataGroup )))
        column_names = data_groups( eachDataGroup )
        for eachColumnName in column_names:
          logger.warn( 'column names: {}'.format ( column_names( eachColumnName ) ) )
    pass



"""
  Error codes:
  1 = Exception related to command entered ( ie, missing / bad config file )
  
"""
  
  
if __name__ == '__main__':
  if len(sys.argv)<2:
    print "Syntax: {} CONFIG_FILE\n".format( sys.argv[0] )
    sys.exit(1)
    
  logging.config.dictConfig(yaml.load( open( 'logging.conf.yaml','r' ) ))
  logging.basicConfig(filename='ReportDataCollector.log', level=logging.DEBUG) # Set initial log level to debug

  # create logger
  # logger = logging.getLogger() # Use this if logging stops working for some reason
  logger = logging.getLogger('main')
  logger.debug( "** ** ** ** ** ** Starting MAIN Logger" )

  prospectiveCfgFile = sys.argv[1]
  if not os.path.exists( prospectiveCfgFile ):
    logger.warn( "Config file '{}' is not found.".format( prospectiveCfgFile ) )
    sys.exit(1)
  
  runner = DataCollectorRunner()
  logger.debug( "DataCollectorRunner: {}".format( runner ) )
  logger.info( "Loading Config: {}".format( prospectiveCfgFile ) )
  
  runner.set_config ( yaml.load( open( prospectiveCfgFile,'r' ) ) )

  runner.validate_working_paths()
  
  loglevel=runner.config['Control']['LogLevel']

  # Set master LogLevel from config file:
  # Note:  This affects what is output to the console, as well as what is logged to file
  # Recommend setting loglevel to '*WARN' in config if not debugging,
  #       and setting loglevel to '*DEBUG' while trying to create new report or troubleshooting.
  # Be careful with changing logging settings in logging.conf.yaml, in addition,
  #       as these settings will apply to *ALL* data collectors and can easily make things difficult to read.

  logger.info( "Config setting all log levels to {}.".format( loglevel ) )
  logger.setLevel( loglevel )

  runner.initialize_dataCollector()
  
  runner.load_column_structures()


  