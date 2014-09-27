# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 13:51:02 2014

@author: Bassett_S
"""




import guidata.dataset.datatypes as dt
import guidata.dataset.dataitems as di

class Processing(dt.DataSet):
    """Example"""
    inputDir = di.DirectoryItem("INPUT DIR:", None)
    startDateTime = di.DateTimeItem("Start Date/Time", default=datetime.datetime(2010, 10, 10))
    endDateTime = di.DateTimeItem("End Date/Time", default=datetime.datetime(2010, 10, 10))
    
    
if __name__ == '__main__':
    import guidata
    _app = guidata.qapplication()
    param = Processing()   
    param.edit()
    param.view()