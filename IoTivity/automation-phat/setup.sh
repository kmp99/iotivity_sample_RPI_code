#!/bin/bash
CURPWD=`pwd`
PROJNAME=${PWD##*/}

cp ${EXAMPLEPATH}/Iotivity-Raspberry-Pi-Code/IoTivity/automation-phat/SConscript ${CURPWD}/
cp ${EXAMPLEPATH}/Iotivity-Raspberry-Pi-Code/IoTivity/automation-phat/automation-phat-config.json ${CURPWD}/${PROJNAME}-config.json
cp ${EXAMPLEPATH}/Iotivity-Raspberry-Pi-Code/pi-boards/automation-phat/automation-phat.json ${CURPWD}/${PROJNAME}.json
cp ${EXAMPLEPATH}/Iotivity-Raspberry-Pi-Code/IoTivity/automation-phat/automation-phat.cpp ${CURPWD}/src/${PROJNAME}.cpp
cp ${EXAMPLEPATH}/Iotivity-Raspberry-Pi-Code/IoTivity/automation-phat/automation-phat-gen.cpp ${CURPWD}/src/${PROJNAME}-gen.cpp
cp ${EXAMPLEPATH}/Iotivity-Raspberry-Pi-Code/pi-boards/automation-phat/automation-hat.py ${CURPWD}/bin/
cp ${EXAMPLEPATH}/Iotivity-Raspberry-Pi-Code/pi-boards/automation-phat/lcdlib.py ${CURPWD}/bin/
