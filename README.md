# ICD - 10 Explorer?
PyGTK application to find icd codes in pysql database  
## depends:

- pysqlite: dev-lang/python +sqlite
- pygobject: dev-python/pygobject  


##issues  
>>ImportError: No module named 'gi'  

PYTHON_TARGETS value must match the Python interpreter  
example:  

    $ python3.4 ./applicaiton.py  
    $ grep PYTHON_TARGETS /etc/portage/make.conf  
    PYTHON_TARGETS="othersx_y python3_4"  
    emerge -pv dev-python/pygobject  
    [ebuild   R    ] dev-python/pygobject-3.14.0:3::gentoo  USE="cairo threads -examples {-test}" PYTHON_TARGETS="othersx_y python3_4" 0 KiB
    
    



