import openhtf as htf
from openhtf.output.callbacks import console_summary
from openhtf.output.callbacks import json_factory
from datetime import datetime

class ConsoleLogs():    #custom callback
    def __call__(self,record):                                                                                  #Test record contains all of the information
        for log_record in record.log_records:                                                                   #OpenHTF has about a test, but one of the more interesting
            #convert time stamp                                                                                 #fielfs is log_records wich contains a list of the LogRecord 
            timestamp = datetime.fromtimestamp(log_record.timestamp_millis / 1000.0)                            #entries generated during the test. 
            timestamp_str = timestamp.strftime('%m/%d/%Y %H:%M:%S')
            print(f"{timestamp_str}\t{log_record.level}\t{log_record.message}")

class ConsoleMeasurements():    #custom callback to know if the measurements passed or no. 
    def __call__(self, record):
        for phase in record.phases:
            print(f"{phase.name}:")
            for name, measurement in phase.measurements.items():
                print(f"\t{measurement.docstring}\t{measurement.outcome}")

@htf.measures(htf.Measurement("P4_digital")                #all the important task are in this kind of metod
              .doc("Pin 4 Digital Measurement")
              .equals(True))

@htf.measures(htf.Measurement("P5_digital")
              .doc("Pin 5 Digital Measurement")
              .equals(True))

@htf.measures(htf.Measurement("P6_digital")
              .doc("Pin 6 Digital Measurement")
              .equals(True))
              
def digital_read(test):
    test.measurements.P4_digital = True
    test.measurements.P5_digital = True
    test.measurements.P6_digital = True

test = htf.Test(digital_read)
test.add_output_callbacks(json_factory.OutputToJSON('./test.{start_time_millis}.json', indent=4))   #Genera un archivo json con toda la informacion
#test.add_output_callbacks(console_summary.ConsoleSummary())                                         #Muetra en la consola si algun measurement no se realizo correctamente, ya que normalmente solo muestra fail o pass
test.add_output_callbacks(ConsoleLogs()) 
test.add_output_callbacks(ConsoleMeasurements())
test.execute()