/**************************************************************************************

      II    N     N     N     N      OOOO      SSSSS     EEEEE    N     N    TTTTTTT
     II    NNN   N     NNN   N    OO    OO    S         E        NNN   N       T
    II    N NN  N     N NN  N    OO    OO    SSSSS     EEE      N NN  N       T
   II    N  NN N     N  NN N    OO    OO        S     E        N  NN N       T
  II    N    NN     N    NN      OOOO      SSSSS     EEEEE    N    NN       T
                         copyright (c) 2021, InnoSenT GmbH
                                 all rights reserved

***************************************************************************************

    filename:			ITR3800_radarAPI_enums.h
    brief:				enums
    creation:			15.03.2021
    author:				Sebastian Weidmann
    version:			v1.101
    last edit:          15.03.2021
    last editor:        Sebastian Weidmann
    change:
    compile switches:



***************************************************************************************/

#ifndef RADARAPI_ENUMS_H
#define RADARAPI_ENUMS_H

/**************************************************************************************
  includes
**************************************************************************************/
#include "ITR3800_radarAPI_basicTypes.h"


/**************************************************************************************
   typedefs
**************************************************************************************/

typedef enum {
    ITR3800_API_ERR_OK                                          = 0x0000,
    ITR3800_API_ERR_HANDLE_NOT_INITIALISED                      ,
    ITR3800_API_ERR_SYSTEM_ALREADY_INITIALISED                  ,
    ITR3800_API_ERR_SYSTEM_NOT_INITIALISED                      ,
    ITR3800_API_ERR_CMD_SOCKET_CONNECTION_LOST                  ,
    ITR3800_API_ERR_CMD_NOT_ACCEPTED                            ,
    ITR3800_API_ERR_CMD_NOT_WRITEABLE                           ,
    ITR3800_API_ERR_CMD_DATA_CORRUPTED                          ,
    ITR3800_API_ERR_CMD_PARAMETER                               ,
    ITR3800_API_ERR_CREATE_HANDLE                               ,
    ITR3800_API_ERR_OBJECT_SOCKET_NO_CONNECTION_AVAILABLE       ,
    ITR3800_API_ERR_OBJECT_SOCKET_CONNECTION_LOST               ,
    ITR3800_API_ERR_SYSTEM_FILENAME_NOT_VALID                   ,
    ITR3800_API_ERR_CMD_TOO_MUCH_DATA_TO_READ                   ,
    ITR3800_API_ERR_CMD_STILL_DATA_AVAILABLE                    ,
    ITR3800_API_ERR_NULL_POINTER                                ,
    ITR3800_API_ERR_OBJECT_NO_VALID_SOCKET                      ,
    ITR3800_API_ERR_CMD_UNKNOWN                                 ,
    ITR3800_API_ERR_FUNCTION_DEPRECATED                         ,
    ITR3800_API_ERR_CONNECTION_CLOSED                           ,
    ITR3800_API_ERR_CONNECTION_RESET                            ,
    ITR3800_API_ERR_COMMUNICATION_TIMEOUT                       ,
    ITR3800_API_ERR_COMMUNICATION_ERROR                         ,
    ITR3800_API_ERR_CONNECTION_LOST                             ,
    ITR3800_API_ERR_ISYS_NOT_FOUND                              ,
    ITR3800_API_ERR_IP_MASK                                     ,
    ITR3800_API_ERR_CMD_TOO_LESS_DATA_TO_READ                   ,
    ITR3800_API_ERR_MUTEX_ERROR                                 ,
    ITR3800_API_ERR_OBJECT_LIST_MUTEX                           ,
    ITR3800_API_ERR_OBJECT_THREAD_INIT                          ,
    ITR3800_API_ERR_OBJECT_LIST_TIMEOUT                         ,
    ITR3800_API_ERR_OBJECT_LIST_UNKNOWN                         ,
    ITR3800_API_ERR_OBJECT_LIST_DISCONNECTED_BY_SYSTEM          ,
    ITR3800_API_ERR_OBJECT_LIST_DISCONNECTED_BY_DLL             ,
    ITR3800_API_ERR_OBJECT_LIST_RESET                           ,
    ITR3800_API_ERR_OBJECT_LIST_SOCKET_NULL                     ,
    ITR3800_API_ERR_OBJECT_LIST_SET_MUTEX                       ,
    ITR3800_API_ERR_OBJECT_LIST_NO_VALID_MUTEX                  ,
    ITR3800_API_ERR_OBJECT_LIST_MUTEX_TIMED_OUT                 ,
    ITR3800_API_ERR_COMMBUFFER_RAWDATA_SOCKET_CONNECTION_LOST   = 0x100 ,
    ITR3800_API_ERR_COMMBUFFER_RAWDATA_TIMEOUT                  ,
    ITR3800_API_ERR_COMMBUFFER_RAWDATA_MUTEX                    ,
    ITR3800_API_ERR_COMMBUFFER_RAWDATA_MUTEX_TIMEOUT            ,
    ITR3800_API_ERR_COMMBUFFER_RAWDATA_INIT                     ,
    ITR3800_API_ERR_IMGBUF_NOT_READY                            ,
    ITR3800_API_ERR_STILLIMAGE_STILL_IN_PROGRESS                ,
    ITR3800_API_ERR_NO_CONNECTION_AVAILABLE                     = 0x200 ,
    ITR3800_API_ERR_NO_VALID_SOCKET                             ,
    ITR3800_API_ERR_ISYS_SW_VERSION_NOT_SUPPORTED               ,
    ITR3800_API_ERR_RAWDATA_NO_FIRST_VALID_FRAME                ,
    ITR3800_API_ERR_OBJECT_LIST_SIZE_METRIC_IMPERIAL            ,
    ITR3800_API_ERR_FIRMWARE_VERSION_INCOMPATIBLE               ,
    ITR3800_API_ERR_FUNCTION_NOT_IMPLEMENTED
} ITR3800_Result_t;

#define I_RESULT_NAMES {{ITR3800_API_ERR_OK,"OK"},\
                       {ITR3800_API_ERR_HANDLE_NOT_INITIALISED,"handle not initialized"},\
                       {ITR3800_API_ERR_SYSTEM_ALREADY_INITIALISED,"system already initialized"},\
                       {ITR3800_API_ERR_SYSTEM_NOT_INITIALISED,"system not initialized"},\
                       {ITR3800_API_ERR_CMD_SOCKET_CONNECTION_LOST,"command socket connection lost"},\
                       {ITR3800_API_ERR_CMD_NOT_ACCEPTED,"command not accepted"},\
                       {ITR3800_API_ERR_CMD_NOT_WRITEABLE,"command not writeable"},\
                       {ITR3800_API_ERR_CMD_DATA_CORRUPTED,"command data corrupted"},\
                       {ITR3800_API_ERR_CMD_PARAMETER,"command parameter"},\
                       {ITR3800_API_ERR_CREATE_HANDLE,"create handle"},\
                       {ITR3800_API_ERR_OBJECT_SOCKET_NO_CONNECTION_AVAILABLE,"object socket no connection available"},\
                       {ITR3800_API_ERR_OBJECT_SOCKET_CONNECTION_LOST,"object socket connection lost"},\
                       {ITR3800_API_ERR_SYSTEM_FILENAME_NOT_VALID,"system filename not valid"},\
                       {ITR3800_API_ERR_CMD_TOO_MUCH_DATA_TO_READ,"command too much data to read"},\
                       {ITR3800_API_ERR_CMD_STILL_DATA_AVAILABLE,"command still data available"},\
                       {ITR3800_API_ERR_NULL_POINTER,"null pointer"},\
                       {ITR3800_API_ERR_OBJECT_NO_VALID_SOCKET,"object no valid socket"},\
                       {ITR3800_API_ERR_CMD_UNKNOWN,"command unknown"},\
                       {ITR3800_API_ERR_FUNCTION_DEPRECATED,"function deprecated"},\
                       {ITR3800_API_ERR_CONNECTION_CLOSED,"connection closed"},\
                       {ITR3800_API_ERR_CONNECTION_RESET,"connection reset"},\
                       {ITR3800_API_ERR_COMMUNICATION_TIMEOUT,"communication timeout"},\
                       {ITR3800_API_ERR_COMMUNICATION_ERROR,"communication error"},\
                       {ITR3800_API_ERR_CONNECTION_LOST,"connection lost"},\
                       {ITR3800_API_ERR_ISYS_NOT_FOUND,"isys not found"},\
                       {ITR3800_API_ERR_IP_MASK,"ip mask"},\
                       {ITR3800_API_ERR_CMD_TOO_LESS_DATA_TO_READ,"command too less data to read"},\
                       {ITR3800_API_ERR_MUTEX_ERROR,"mutex error"},\
                       {ITR3800_API_ERR_OBJECT_LIST_MUTEX,"object list mutex"},\
                       {ITR3800_API_ERR_OBJECT_THREAD_INIT,"object thread init"},\
                       {ITR3800_API_ERR_OBJECT_LIST_TIMEOUT,"object list timeout"},\
                       {ITR3800_API_ERR_OBJECT_LIST_UNKNOWN,"object list unknown"},\
                       {ITR3800_API_ERR_OBJECT_LIST_DISCONNECTED_BY_SYSTEM,"object list disconnected by system"},\
                       {ITR3800_API_ERR_OBJECT_LIST_DISCONNECTED_BY_DLL,"object list disconnected by dll"},\
                       {ITR3800_API_ERR_OBJECT_LIST_RESET,"object list reset"},\
                       {ITR3800_API_ERR_OBJECT_LIST_SOCKET_NULL,"object list socket null"},\
                       {ITR3800_API_ERR_OBJECT_LIST_SET_MUTEX,"object list set mutex"},\
                       {ITR3800_API_ERR_OBJECT_LIST_NO_VALID_MUTEX,"object list no valid mutex"},\
                       {ITR3800_API_ERR_OBJECT_LIST_MUTEX_TIMED_OUT,"object list mutex timed out"},\
                       {ITR3800_API_ERR_COMMBUFFER_RAWDATA_SOCKET_CONNECTION_LOST,"rawdata socket connection lost"},\
                       {ITR3800_API_ERR_COMMBUFFER_RAWDATA_TIMEOUT,"rawdata timeout"},\
                       {ITR3800_API_ERR_COMMBUFFER_RAWDATA_MUTEX,"rawdata mutex"},\
                       {ITR3800_API_ERR_COMMBUFFER_RAWDATA_MUTEX_TIMEOUT,"rawdata mutex timeout"},\
                       {ITR3800_API_ERR_COMMBUFFER_RAWDATA_INIT,"rawdata init"},\
                       {ITR3800_API_ERR_IMGBUF_NOT_READY,"image buffer not ready"},\
                       {ITR3800_API_ERR_NO_CONNECTION_AVAILABLE,"no connection available"},\
                       {ITR3800_API_ERR_NO_VALID_SOCKET,"no valid socket"},\
                       {ITR3800_API_ERR_ISYS_SW_VERSION_NOT_SUPPORTED,"isys software version not supported"},\
                       {ITR3800_API_ERR_RAWDATA_NO_FIRST_VALID_FRAME,"rawdata no first valid frame"},\
                       {ITR3800_API_ERR_OBJECT_LIST_SIZE_METRIC_IMPERIAL,"object list size metric imperial"},\
                       {ITR3800_API_ERR_FIRMWARE_VERSION_INCOMPATIBLE,"firmware version incompatible"},\
                       {ITR3800_API_ERR_FUNCTION_NOT_IMPLEMENTED,"function not implemented"}}

typedef enum {
    ITR3800_API_TRACK_CLASS_OTHERS          =  2u,
    ITR3800_API_TRACK_CLASS_PEDESTRIAN      = 10u,
    ITR3800_API_TRACK_CLASS_BICYCLE         = 12u,
    ITR3800_API_TRACK_CLASS_CAR             = 30u,
    ITR3800_API_TRACK_CLASS_SMALL_TRUCK     = 60u,
    ITR3800_API_TRACK_CLASS_BIG_TRUCK       = 70u
}ITR3800_TrackClass_t;

union ITR3800_TrackClass_u {
    ITR3800_TrackClass_t ITR3800_TrackClass;
    uint32_t dummy;
};

typedef enum {
    ITR3800_API_OBJECT_LIST_OK                          = 0x00,
    ITR3800_API_OBJECT_LIST_FULL                        = 0x01,
    ITR3800_API_OBJECT_LIST_REFRESHED                   = 0x02,
    ITR3800_API_OBJECT_LIST_ALREADY_REQUESTED           = 0x03,
    ITR3800_API_OBJECT_LIST_NOT_RUNNING                 = 0x04,
    ITR3800_API_OBJECT_LIST_FIRMWARE_UPDATE_RUNNING     = 0x05,
    ITR3800_API_OBJECT_LIST_LISTENING                   = 0x06,
    ITR3800_API_OBJECT_LIST_COMMUNICATION_TIMEOUT       = 0x07
} ITR3800_ObjectListError_t;

union ITR3800_ObjectListError_u {
    ITR3800_ObjectListError_t ITR3800_ObjectListError;
    uint32_t dummy;
};

typedef enum {
    ITR3800_API_LOCATION_RAM = 0,
    ITR3800_API_LOCATION_EEPROM = 1
} ITR3800_SaveLocation_t;

typedef enum {
    ITR3800_API_NETWORK_DHCP = 0,
    ITR3800_API_NETWORK_STATICIP = 1
} ITR3800_NetworkSetting_t;

typedef enum {
    ITR3800_API_DIRECTION_APPROACHING               = 0x00,
    ITR3800_API_DIRECTION_RECEDING                  = 0x01,
    ITR3800_API_DIRECTION_BOTH                      = 0x02
}ITR3800_TrafficDirection_t;

typedef enum {
    ITR3800_FREQUENCY_CHANNEL_1 = 1,
    ITR3800_FREQUENCY_CHANNEL_2 = 2,
    ITR3800_FREQUENCY_CHANNEL_3 = 3,
    ITR3800_FREQUENCY_CHANNEL_4 = 4
} ITR3800_FrequencyChannel_t;

typedef enum {
    ITR3800_EVENTZONE_MOTION                 = 0x00,
    ITR3800_EVENTZONE_PRESENCE               = 0x01,
    ITR3800_EVENTZONE_SIDEWALK               = 0x02,
    ITR3800_EVENTZONE_LOOP                   = 0x03
} ITR3800_EventZoneType_t;

typedef enum {
    ITR3800_CONDITIONCLASS_ALL                    = 0x00,
    ITR3800_CONDITIONCLASS_CAR                    = 0x01,
    ITR3800_CONDITIONCLASS_BIKE_PEDEST            = 0x02,
    ITR3800_CONDITIONCLASS_SMALL_TRUCK            = 0x03,
    ITR3800_CONDITIONCLASS_BIG_TRUCK              = 0x04,
    ITR3800_CONDITIONCLASS_CAR_BIG_TRUCK          = 0x05,
    ITR3800_CONDITIONCLASS_CAR_SMALL_TRUCK        = 0x06,
    ITR3800_CONDITIONCLASS_CAR_SMALL_BIG_TRUCK    = 0x07
} ITR3800_ConditionClass_t;

typedef enum {
    ITR3800_CONDITIONDIRECTION_BOTH           = 0x00,
    ITR3800_CONDITIONDIRECTION_APPROACHING    = 0x01,
    ITR3800_CONDITIONDIRECTION_RECEDING       = 0x02
} ITR3800_ConditionDirection_t;

typedef enum {
    ITR3800_UNIT_METER                       = 0x00,
    ITR3800_UNIT_KMH                         = 0x01,
    ITR3800_UNIT_FEET                        = 0x02,
    ITR3800_UNIT_MPH                         = 0x03
} ITR3800_UnitType_t;

typedef enum {
    ITR3800_BAUDRATE_115200 = 115200,
    ITR3800_BAUDRATE_230400 = 230400
} ITR3800_RS485_Baudrate_t;

typedef enum {
    ITR3800_UDP_MODE_BROADCAST = 0,
    ITR3800_UDP_MODE_MULTICAST = 1,
    ITR3800_UDP_MODE_IP        = 2
} ITR3800_Udp_Mode_t;

typedef enum {
    ITR3800_OPERATION_MODE_0 = 0,
    ITR3800_OPERATION_MODE_1 = 1,
    ITR3800_OPERATION_MODE_2 = 2
} ITR3800_OperationMode_t;

typedef enum {
    /* UTC-10 */
    ITR3800_API_TIMEZONE_ALEUTIAN                   = 0,  /* US/Aleutian */
    ITR3800_API_TIMEZONE_HAWAII                     ,     /* US/Hawaii */

    /* UTC-9:30 */
    ITR3800_API_TIMEZONE_MARQUESAS                  ,     /* Pacific/Marquesas */

    /* UTC-9:00 */
    ITR3800_API_TIMEZONE_ALASKA                     ,     /* US/Alaska */

    /* UTC-8:00 */
    ITR3800_API_TIMEZONE_PACIFIC_TIME               ,     /* US/Pacific */

    /* UTC-7:00 */
    ITR3800_API_TIMEZONE_ARIZONA                    ,     /* US/Arizona */
    ITR3800_API_TIMEZONE_MOUNTAIN_TIME              ,     /* US/Mountain */
    ITR3800_API_TIMEZONE_LA_PAZ                     ,     /* America/La_Paz */

    /* UTC-6:00 */
    ITR3800_API_TIMEZONE_CENTRAL_TIME               ,     /* US/Central */
    ITR3800_API_TIMEZONE_MEXICO_CITY                ,     /* America/Mexico_City */
    ITR3800_API_TIMEZONE_EASTER                     ,     /* Pacific/Easter */

    /* UTC-5:00 */
    ITR3800_API_TIMEZONE_BOGOTA_LIMA_QUITO_RIO_BRANCO   ,     /* America/Bogota */
    ITR3800_API_TIMEZONE_EASTERN_TIME               ,     /* US/Easternr */

    /* UTC-4:00 */
    ITR3800_API_TIMEZONE_ASUNCION                   ,     /* America/Asuncion */
    ITR3800_API_TIMEZONE_CARACAS                    ,     /* America/Caracas */
    ITR3800_API_TIMEZONE_CUIABA                     ,     /* America/Cuiaba */
    ITR3800_API_TIMEZONE_SANTAGIO                   ,     /* America/Santiago */

    /* UTC-3:00 */
    ITR3800_API_TIMEZONE_BUENOS_AIRES               ,     /* America/Argentina/Buenos_Aires */
    ITR3800_API_TIMEZONE_CAYENNE                    ,     /* America/Cayenne */
    ITR3800_API_TIMEZONE_MONTEVIDEO                 ,     /* America/Montevideo */
    ITR3800_API_TIMEZONE_EL_SALVADOR                ,     /* America/El_Salvador */
    ITR3800_API_TIMEZONE_MIQUELON                   ,     /* America/Miquelon */

    /* UTC-0:00  GREENWICH-TIME */
    ITR3800_API_TIMEZONE_CASABLANCA                 ,     /* Africa/Casablanca */
    ITR3800_API_TIMEZONE_DUBLIN                     ,     /* Europe/Dublin */
    ITR3800_API_TIMEZONE_MONROVIA                   ,     /* Africa/Monrovia */

    /* UTC+1:00 */
    ITR3800_API_TIMEZONE_AMSTERDAM_BERLIN_ROME_STOCKHOLM_VIENNA                  ,     /* Europe/Amsterdam */
    ITR3800_API_TIMEZONE_BELGRADE                   ,     /* Europe/Belgrade */
    ITR3800_API_TIMEZONE_BRUSSELS                   ,     /* Europe/Brussels */
    ITR3800_API_TIMEZONE_SARAJEVO                   ,     /* Europe/Sarajevo */
    ITR3800_API_TIMEZONE_WINDHOEK                   ,     /* Africa/Windhoek */

    /* UTC+2:00 */
    ITR3800_API_TIMEZONE_AMMAM                      ,     /* Asia/Amman */
    ITR3800_API_TIMEZONE_ATHENS                     ,     /* Europe/Athens */
    ITR3800_API_TIMEZONE_BEIRUT                     ,     /* Asia/Beirut */
    ITR3800_API_TIMEZONE_CHISINAU                   ,     /* Europe/Chisinau */
    ITR3800_API_TIMEZONE_DAMASCUS                   ,     /* Asia/Damascus */
    ITR3800_API_TIMEZONE_GAZA                       ,     /* Asia/Gaza */
    ITR3800_API_TIMEZONE_HARARE                     ,     /* Africa/Harare */
    ITR3800_API_TIMEZONE_HELSINKI                   ,     /* Europe/Helsinki */
    ITR3800_API_TIMEZONE_JERUSALEM                  ,     /* Asia/Jerusalem */
    ITR3800_API_TIMEZONE_KALININGRAD                ,     /* Europe/Kaliningrad */
    ITR3800_API_TIMEZONE_CAIRO                      ,     /* Africa/Cairo */
    ITR3800_API_TIMEZONE_TRIPOLIS                   ,     /* Africa/Tripoli */

    /* UTC+3:00 */
    ITR3800_API_TIMEZONE_ISTANBUL                   ,     /* Europe/Istanbul */
    ITR3800_API_TIMEZONE_KUWAIT                     ,     /* Asia/Kuwait */
    ITR3800_API_TIMEZONE_MINSK                      ,     /* Europe/Minsk */
    ITR3800_API_TIMEZONE_MOSCOW                     ,     /* Europe/Moscow */
    ITR3800_API_TIMEZONE_NAIROBI                    ,     /* Africa/Nairobi */

    /* UTC+4:00 */
    ITR3800_API_TIMEZONE_BAKU                       ,     /* Asia/Baku */
    ITR3800_API_TIMEZONE_SAMARA                     ,     /* Europe/Samara */

    /* UTC+4:30 */
    ITR3800_API_TIMEZONE_KABUL                      ,     /* Asia/Kabul */

    /* UTC+5:00 */
    ITR3800_API_TIMEZONE_ASHGABAT                   ,     /* Asia/Ashgabat */
    ITR3800_API_TIMEZONE_KARACHI                    ,     /* Asia/Karachi */

    /* UTC+5:30 */
    ITR3800_API_TIMEZONE_KOLKATA                    ,     /* Asia/Kolkata */

    /* UTC+5:45 */
    ITR3800_API_TIMEZONE_KATMANDU                   ,     /* Asia/Katmandu */

    /* UTC+6:00 */
    ITR3800_API_TIMEZONE_OMSK                       ,     /* Asia/Omsk */

    /* UTC+7:00 */
    ITR3800_API_TIMEZONE_BANGKOK_HANOI_JAKARTA      ,     /* Asia/Bangkok */
    ITR3800_API_TIMEZONE_HOVD                       ,     /* Asia/Hovd */
    ITR3800_API_TIMEZONE_KRASNOYARSK                ,     /* Asia/Krasnoyarsk */

    /* UTC+8:00 */
    ITR3800_API_TIMEZONE_IRKUTSK                    ,     /* Asia/Irkutsk */
    ITR3800_API_TIMEZONE_KUALA_LUMPUR               ,     /* Asia/Kuala_Lumpur */
    ITR3800_API_TIMEZONE_HONG_KONG                  ,     /* Asia/Hong_Kong */
    ITR3800_API_TIMEZONE_PERTH                      ,     /* Australia/Perth */
    ITR3800_API_TIMEZONE_ULAN_BATOR                 ,     /* Asia/Ulan_Bator */
    ITR3800_API_TIMEZONE_TAIPEI                     ,     /* Asia/Taipei */

    /* UTC+8:30 */
    ITR3800_API_TIMEZONE_PYONGYANG                  ,     /* Asia/Pyongyang */

    /* UTC+8:45 */
    ITR3800_API_TIMEZONE_EUCLA                      ,     /* Australia/Eucla */

    /* UTC+9:00 */
    ITR3800_API_TIMEZONE_SEOUL                      ,     /* Asia/Seoul */

    /* UTC+9:30 */
    ITR3800_API_TIMEZONE_ADELAIDE                   ,     /* Australia/Adelaide */
    ITR3800_API_TIMEZONE_DARWIN                     ,     /* Australia/Darwin */

    /* UTC+10:00 */
    ITR3800_API_TIMEZONE_BRISBANE                   ,     /* Australia/Brisbane */
    ITR3800_API_TIMEZONE_CANBERRA                   ,     /* Australia/Canberra */
    ITR3800_API_TIMEZONE_GUAM                       ,     /* Pacific/Guam */
    ITR3800_API_TIMEZONE_HOBART                     ,     /* Australia/Hobart */
    ITR3800_API_TIMEZONE_VLADIVOSTOK                ,     /* Asia/Vladivostok */

    /* UTC+10:30 */
    ITR3800_API_TIMEZONE_LORD_HOWE                  ,     /* Australia/Lord_Howe */

    /* UTC+11:00 */
    ITR3800_API_TIMEZONE_MAGADAN                    ,     /* Asia/Magadan */
    ITR3800_API_TIMEZONE_NORFOLK                    ,     /* Pacific/Norfolk */

    /* UTC+12:00 */
    ITR3800_API_TIMEZONE_AUCKLAND                   ,     /* Pacific/Auckland */
    ITR3800_API_TIMEZONE_FIJI                       ,     /* Pacific/Fiji */

    /* UTC+12:45 */
    ITR3800_API_TIMEZONE_CHATHAM                    ,     /* Pacific/Chatham */

    /* UTC+13:00 */
    ITR3800_API_TIMEZONE_SAMOA                      ,     /* Pacific/Samoa */

    /* UTC+14:00 */
    ITR3800_API_TIMEZONE_KIRIMATI                   ,     /* Pacific/Kiritimati */

    /* UTC MAX */
    ITR3800_API_TIMEZONE_MAX
} ITR3800_TimeZone_t ;

#endif // RADARAPI_ENUMS_H
