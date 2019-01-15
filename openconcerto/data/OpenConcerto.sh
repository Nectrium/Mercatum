#!/bin/bash

java -DredirectToFile=true -Dfwk_sql.debug.undefined_id=true -Dfile.encoding=UTF-8 -Xms100M -Xmx768M $JAVA_VMARGS -jar OpenConcerto.jar

