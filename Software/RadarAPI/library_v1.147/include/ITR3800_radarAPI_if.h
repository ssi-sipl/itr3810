/**************************************************************************************

      II    N     N     N     N      OOOO      SSSSS     EEEEE    N     N    TTTTTTT
     II    NNN   N     NNN   N    OO    OO    S         E        NNN   N       T
    II    N NN  N     N NN  N    OO    OO    SSSSS     EEE      N NN  N       T
   II    N  NN N     N  NN N    OO    OO        S     E        N  NN N       T
  II    N    NN     N    NN      OOOO      SSSSS     EEEEE    N    NN       T
                         copyright (c) 2021, InnoSenT GmbH
                                 all rights reserved

***************************************************************************************

    filename:			ITR3800_radarAPI_if.h
    brief:
    creation:			15.03.2021
    author:             Sebastian Weidmann

    version:			v1.101
    last edit:          15.03.2021
    last editor:        Sebastian Weidmann
    change:
    compile switches:


***************************************************************************************/

#ifndef ITR3800_RADARAPI_IF_H
#define ITR3800_RADARAPI_IF_H

/**************************************************************************************
  includes
**************************************************************************************/
#include "ITR3800_radarAPI_basicTypes.h"
#include "ITR3800_radarAPI_enums.h"
#include "ITR3800_radarAPI_structs.h"


/**************************************************************************************
 defines
**************************************************************************************/
#if defined(_WIN32) && !defined(ITR3800_RADARAPI_LIBRARY_AS_SOURCE)
    #ifdef ITR3800_RADARAPI_LIBRARY
        #define RADAR_API_EXPORT __declspec(dllexport)
    #else
        #define RADAR_API_EXPORT __declspec(dllimport)
    #endif
#else
    #ifndef RADAR_API_EXPORT
        #define RADAR_API_EXPORT
    #endif
#endif

#ifdef __cplusplus
extern "C" {
#endif

/**************************************************************************************
 api functions
**************************************************************************************/
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getApiVersion(float32_t *version);

/* system functions */
RADAR_API_EXPORT ITR3800_Result_t ITR3800_initSystem(APIHandle_t *pHandle, uint8_t ipPart1, uint8_t ipPart2, uint8_t ipPart3, uint8_t ipPart4);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_exitSystem(APIHandle_t pHandle);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_restartSystem(APIHandle_t pHandle);   /* restart system */
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getSystemInfo(APIHandle_t pHandle, ITR3800_SystemInfo_t *systemInfo); /* get the status of system */
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setDescription(APIHandle_t pHandle, ITR3800_Description_t description);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getDescription(APIHandle_t pHandle, ITR3800_Description_t *pDescription);

/* system configuration functions */
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setNetworkHostname(APIHandle_t pHandle, char *hostName, uint8_t length);    /* set network hostname */
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getNetworkHostname(APIHandle_t pHandle, char *hostName, uint8_t *length);   /* get network hostname */
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setRS485BaudRate(APIHandle_t pHandle, ITR3800_RS485_Baudrate_t baudrate);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getRS485BaudRate(APIHandle_t pHandle, ITR3800_RS485_Baudrate_t *baudrate);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setStaticIP(APIHandle_t pHandle, uint8_t ipPart1, uint8_t ipPart2, uint8_t ipPart3, uint8_t ipPart4,
                                                        uint8_t subnetPart1, uint8_t subnetPart2, uint8_t subnetPart3, uint8_t subnetPart4,
                                                        uint8_t stdGatewayPart1, uint8_t stdGatewayPart2, uint8_t stdGatewayPart3, uint8_t stdGatewayPart4); /* change static ip address */
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setDhcpIP(APIHandle_t pHandle);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getIPsettings(APIHandle_t pHandle, ITR3800_NetworkSetting_t *mode, uint8_t *ipPart1, uint8_t *ipPart2, uint8_t *ipPart3, uint8_t *ipPart4,
                                                            uint8_t *subnetPart1, uint8_t *subnetPart2, uint8_t *subnetPart3, uint8_t *subnetPart4,
                                                            uint8_t *stdGatewayPart1, uint8_t *stdGatewayPart2, uint8_t *stdGatewayPart3, uint8_t *stdGatewayPart4);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setInstallationHeight(APIHandle_t pHandle, float32_t height_m);   /* installation height - used by signal processing */
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getInstallationHeight(APIHandle_t pHandle, float32_t *pHeight_m);   /* installation height - used by signal processing */
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setInstallationHeightImperial(APIHandle_t pHandle, float32_t height_ft);   /* installation height - used by signal processing */
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getInstallationHeightImperial(APIHandle_t pHandle, float32_t *pHeight_ft);   /* installation height - used by signal processing */
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setElevationAngle(APIHandle_t pHandle, float32_t angle_deg); /* elevation angle - used by signal processing*/
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getElevationAngle(APIHandle_t pHandle, float32_t *pAngle_deg); /* elevation angle - used by signal processing*/
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getInclinationAngles(APIHandle_t pHandle, float32_t *pPitch_deg, float32_t *pRoll_deg); /* measured by internal inclination sensor */
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getDateTime(APIHandle_t pHandle, uint16_t *year, uint16_t *month, uint16_t *day, uint16_t *hour, uint16_t *minute, uint16_t *second, ITR3800_TimeZone_t *timeZone);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setDateTime(APIHandle_t pHandle, uint16_t year, uint16_t month, uint16_t day, uint16_t hour, uint16_t minute, uint16_t second, ITR3800_TimeZone_t timeZone);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getGpsDateTimeSyncEnable(APIHandle_t pHandle, bool_t *enable);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setGpsDateTimeSyncEnable(APIHandle_t pHandle, bool_t enable);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getNtpDateTimeSyncEnable(APIHandle_t pHandle, bool_t *enable);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setNtpDateTimeSyncEnable(APIHandle_t pHandle, bool_t enable);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getGpsCoordinates(APIHandle_t pHandle, float32_t *lat, float32_t *lng);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getGpsSatellitesInView(APIHandle_t pHandle, ITR3800_GpsSatellitesInView_t *gpsSatellitesInView);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setFrequencyChannel(APIHandle_t pHandle, ITR3800_FrequencyChannel_t channel);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getFrequencyChannel(APIHandle_t pHandle, ITR3800_FrequencyChannel_t *channel);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setHighwayMode(APIHandle_t pHandle, uint8_t enable);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getHighwayMode(APIHandle_t pHandle, uint8_t *enable);

RADAR_API_EXPORT ITR3800_Result_t ITR3800_setSimulation(APIHandle_t pHandle, uint8_t enable);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getSimulation(APIHandle_t pHandle, uint8_t *enable);

RADAR_API_EXPORT ITR3800_Result_t ITR3800_setPlayback(APIHandle_t pHandle, uint8_t enable);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getPlayback(APIHandle_t pHandle, uint8_t *enable);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_uploadPlaybackFile(APIHandle_t pHandle, const char *FilePath);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getUploadPlaybackFileStatus(APIHandle_t pHandle, uint8_t *status_percent, ITR3800_Result_t *errorcode);

RADAR_API_EXPORT ITR3800_Result_t ITR3800_setMaxStopTimeObject(APIHandle_t pHandle, uint16_t time_s); /* time (seconds) static track is hold */
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getMaxStopTimeObject(APIHandle_t pHandle, uint16_t *pTime_s); /* time (seconds) static track is hold */

RADAR_API_EXPORT ITR3800_Result_t ITR3800_setStaticTargetsEnable(APIHandle_t pHandle, uint8_t enable);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getStaticTargetsEnable(APIHandle_t pHandle, uint8_t *enable);

RADAR_API_EXPORT ITR3800_Result_t ITR3800_setUdpSettings(APIHandle_t pHandle, ITR3800_Udp_Mode_t mode, uint16_t port, uint8_t dstIpPart1, uint8_t dstIpPart2, uint8_t dstIpPart3, uint8_t dstIpPart4);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getUdpSettings(APIHandle_t pHandle, ITR3800_Udp_Mode_t *mode, uint16_t *port, uint8_t *dstIpPart1, uint8_t *dstIpPart2, uint8_t *dstIpPart3, uint8_t *dstIpPart4);

RADAR_API_EXPORT ITR3800_Result_t ITR3800_setOperationMode(APIHandle_t pHandle, ITR3800_OperationMode_t mode);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getOperationMode(APIHandle_t pHandle, ITR3800_OperationMode_t *mode);

RADAR_API_EXPORT ITR3800_Result_t ITR3800_setFactorySettings(APIHandle_t pHandle);

/* traffic eventzone functions */
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setEventZones(APIHandle_t pHandle, ITR3800_EventZones_t eventzones);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getEventZones(APIHandle_t pHandle, ITR3800_EventZones_t *eventzones);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setEventZonesImperial(APIHandle_t pHandle, ITR3800_EventZones_t eventzones);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getEventZonesImperial(APIHandle_t pHandle, ITR3800_EventZones_t *eventzones);

RADAR_API_EXPORT ITR3800_Result_t ITR3800_setUnitTypes(APIHandle_t pHandle, ITR3800_UnitType_t distanceUnit, ITR3800_UnitType_t velocityUnit);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getUnitTypes(APIHandle_t pHandle, ITR3800_UnitType_t *distanceUnit, ITR3800_UnitType_t *velocityUnit);

/* traffic ignorezone functions */
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setIgnoreZones(APIHandle_t pHandle, ITR3800_IgnoreZones_t ignorezones);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getIgnoreZones(APIHandle_t pHandle, ITR3800_IgnoreZones_t *ignorezones);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setIgnoreZonesImperial(APIHandle_t pHandle, ITR3800_IgnoreZones_t ignorezones);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getIgnoreZonesImperial(APIHandle_t pHandle, ITR3800_IgnoreZones_t *ignorezones);

/* read object list functions */
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getObjectList(APIHandle_t pHandle, ITR3800_ObjectList_t *pObjectList);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getObjectListImperial(APIHandle_t pHandle, ITR3800_ObjectListImperial_t *pObjectListImperial);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_removeObject(APIHandle_t pHandle, uint32_t ui32_objectID);      /* remove track */

/* camera control */
RADAR_API_EXPORT ITR3800_Result_t ITR3800_stillImageTrigger(APIHandle_t pHandle);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_setStillImageCallbackFn(APIHandle_t pHandle, void (*pfCallback)());
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getStillImage(APIHandle_t pHandle, ITR3800_PNGBuf *&pBuf);
RADAR_API_EXPORT ITR3800_Result_t ITR3800_getRtspUrl(APIHandle_t pHandle, char *&rtspUrl);


/**************************************************************************************
 api functions end
**************************************************************************************/


#ifdef __cplusplus
}
#endif

#endif // ITR3800_RADARAPI_IF_H
