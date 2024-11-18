/**************************************************************************************

      II    N     N     N     N      OOOO      SSSSS     EEEEE    N     N    TTTTTTT
     II    NNN   N     NNN   N    OO    OO    S         E        NNN   N       T
    II    N NN  N     N NN  N    OO    OO    SSSSS     EEE      N NN  N       T
   II    N  NN N     N  NN N    OO    OO        S     E        N  NN N       T
  II    N    NN     N    NN      OOOO      SSSSS     EEEEE    N    NN       T
                         copyright (c) 2021, InnoSenT GmbH
                                 all rights reserved

***************************************************************************************

    filename:			ITR3800_radarAPI_structs.h
    brief:				structs
    creation:			15.03.2021
    author:				Sebastian Weidmann

    version:			v1.101
    last edit:          15.03.2021
    last editor:        Sebastian Weidmann
    change:
    compile switches:



***************************************************************************************/

#ifndef ITR3800_RADARAPI_STRUCTS_H
#define ITR3800_RADARAPI_STRUCTS_H

/**************************************************************************************
  includes
**************************************************************************************/
#include "ITR3800_radarAPI_basicTypes.h"
#include "ITR3800_radarAPI_enums.h"

#include <cstdlib>
#include <string>


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

#define MAX_TRACKS (0x3C)
#define MAX_DETECTIONS (0x3C * 4)
#define MAX_SYSTEMS_CONNECTED (255)
#define ITR3800_MAX_NR_OF_TRACKS     	(256)
#define ITR3800_MAX_NR_OF_DETECTIONS  (512)
#define ITR3800_MAX_NR_OF_IGNOREZONES                  (10)
#define ITR3800_MAX_NR_OF_EVENTZONES                   (64)
#define ITR3800_MAX_NR_OF_POINTS_PER_EVENT_ZONE        (20)
#define ITR3800_MAX_NR_OF_POINTS_PER_IGNORE_ZONE       (10)
#define ITR3800_MAX_LENGTH_EVENTZONE_NAME              (20)
#define ITR3800_MAX_LENGTH_IGNOREZONE_NAME             (20)
#define ITR3800_MAX_LENGTH_DESCRIPTION_NAME            (64)
#define ITR3800_MAX_NR_OF_CONDITIONS                   (10)
#define ITR3800_MAX_EVENT_MESSAGE_LENGTH               (128)
#define ITR3800_MAX_NR_OF_EVENT_MESSAGES               (256)


#ifdef __cplusplus
extern "C" {
#endif

#ifdef WIN32
/* windows stuff */
#else
typedef unsigned long DWORD;
typedef unsigned short WORD;
typedef unsigned int UNINT32;
#endif

/**************************************************************************************
   typedefs
**************************************************************************************/
typedef struct ITR3800_eventMessage{
    char c_eventMessage[ITR3800_MAX_EVENT_MESSAGE_LENGTH];
    uint8_t ui8_eventMessageLength;
} ITR3800_EventMessage_t;

typedef struct ITR3800_EventMessageList{
    ITR3800_EventMessage_t eventMessages[ITR3800_MAX_NR_OF_EVENT_MESSAGES];
    uint8_t nrOfMessages;
} ITR3800_EventMessageList_t;

typedef struct {
    uint32_t ui32_objectID;
    uint16_t ui16_ageCount;
    uint16_t ui16_predictionCount;
    uint16_t ui16_staticCount;
    float32_t f32_trackQuality;                             /* track quality */
    union ITR3800_TrackClass_u classID;                    /* object class of vehicle [id] */
    sint16_t si16_motion_eventZoneIndex;                    /* object in motion eventzone [index] */
    sint16_t si16_presence_eventZoneIndex;                  /* object in presence eventzone [index] */
    sint16_t si16_loop_eventZoneIndex;                      /* object in loop eventzone [index] */
    float32_t f32_positionX_m;                              /* position x in cartesian coordiante system [meter] */
    float32_t f32_positionY_m;                              /* position y in cartesian coordiante system [meter] */
    float32_t f32_velocityX_mps;                            /* velocity x in cartesian coordiante system [meter per second] */
    float32_t f32_velocityY_mps;                            /* velocity y in cartesian coordiante system [meter per second] */
    float32_t f32_velocityInDir_mps;                        /* velocity in direction Meter per Second [meter per second] */
    float32_t f32_directionX;                               /* normed direction x */
    float32_t f32_directionY;                               /* normed direction y */
    float32_t f32_distanceToFront_m;                        /* distance To Front [meter] */
    float32_t f32_distanceToBack_m;                         /* distance To Back [meter] */
    float32_t f32_length_m;                                 /* length of object [meter] */
    float32_t f32_width_m;                                  /* width of object [meter] */
} ITR3800_TrackedObject_t;

typedef struct {
    uint16_t protocolVersion;
    uint8_t reserved_0;
    uint8_t configurationChanged;
    uint32_t systemState;
    union ITR3800_ObjectListError_u error;
    uint32_t timestamp_ms;
    uint16_t frameID;
    uint16_t nrOfTracks;
    ITR3800_TrackedObject_t trackedObjects[ITR3800_MAX_NR_OF_TRACKS];
    ITR3800_EventMessageList_t eventMessages;
    float reserved0;
    float reserved1;
    float reserved2;
    float reserved3;
} ITR3800_ObjectList_t;

typedef struct {
    uint32_t ui32_objectID;
    uint16_t ui16_ageCount;
    uint16_t ui16_predictionCount;
    uint16_t ui16_staticCount;
    float32_t f32_trackQuality;                             /* track quality */
    union ITR3800_TrackClass_u classID;                    /* object class of vehicle [] */
    sint16_t si16_motion_eventZoneIndex;                    /* object in motion eventzone [index] */
    sint16_t si16_presence_eventZoneIndex;                  /* object in presence eventzone [index] */
    sint16_t si16_loop_eventZoneIndex;                      /* object in loop eventzone [index] */
    float32_t f32_positionX_feet;                           /* position x in cartesian coordiante system [feet] */
    float32_t f32_positionY_feet;                           /* position y in cartesian coordiante system [feet] */
    float32_t f32_velocityX_mph;                            /* velocity x in cartesian coordiante system [miles per hour] */
    float32_t f32_velocityY_mph;                            /* velocity y in cartesian coordiante system [miles per hour] */
    float32_t f32_velocityInDir_mph;                        /* velocity in direction [miles per hour] */
    float32_t f32_directionX;                               /* normed direction x */
    float32_t f32_directionY;                               /* normed direction y */
    float32_t f32_distanceToFront_feet;                     /* distance To Front [feet] */
    float32_t f32_distanceToBack_feet;                     /* distance To Back [feet] */
    float32_t f32_length_feet;                             /* length of object [feet] */
    float32_t f32_width_feet;                              /* width of object [feet] */
} ITR3800_TrackedObjectImperial_t;

typedef struct {
    uint16_t protocolVersion;
    uint8_t reserved_0;
    uint8_t configurationChanged;
    uint32_t systemState;
    union ITR3800_ObjectListError_u error;
    uint32_t timestamp_ms;
    uint16_t frameID;
    uint16_t nrOfTracks;
    ITR3800_TrackedObjectImperial_t trackedObjects[ITR3800_MAX_NR_OF_TRACKS];
    ITR3800_EventMessageList_t eventMessages;
    float reserved0;
    float reserved1;
    float reserved2;
    float reserved3;
} ITR3800_ObjectListImperial_t;

typedef struct {
    float32_t swVersion;
    float32_t blVersion;
    float32_t serialNumber;
}ITR3800_DeviceInfo_t;

typedef struct {
    uint32_t productcode;
    uint32_t serialNumber;
    uint32_t swVersionMajor;
    uint32_t swVersionMinor;
    uint32_t reserved1;
    uint32_t reserved2;
    uint32_t reserved3;
    uint32_t reserved4;
} ITR3800_SystemInfo_t;

typedef struct {
    float32_t x;
    float32_t y;
} ITR3800_PointXY_t;

union ITR3800_TrafficDirection_u{
    ITR3800_TrafficDirection_t direction;
    uint32_t dummy;
};

typedef struct {
    bool enable;
    uint8_t outputNumber;
    ITR3800_ConditionClass_t conditionClass;
    ITR3800_ConditionDirection_t direction;
    float32_t velocity_min_kmh;
    float32_t velocity_max_kmh;
    float32_t queuelength_min_m;
    float32_t queuelength_max_m;
    uint16_t eventmessage_delay;
    uint16_t eventmessage_extend;
    float32_t eta_min_s;
    float32_t eta_max_s;
    uint8_t nrOfPedestBikes_min;
    uint8_t nrOfPedestBikes_max;
    uint8_t nrOfCars_min;
    uint8_t nrOfCars_max;
    uint8_t nrOfSmallTrucks_min;
    uint8_t nrOfSmallTrucks_max;
    uint8_t nrOfBigTrucks_min;
    uint8_t nrOfBigTrucks_max;
} ITR3800_Condition_t;

/* event zone struct */
typedef struct {
    bool enable;
    bool eventFlag;
    char zoneName[ITR3800_MAX_LENGTH_EVENTZONE_NAME];
    uint8_t zoneNameLength;
    uint32_t nrOfZonePoints;
    ITR3800_PointXY_t zoneData[ITR3800_MAX_NR_OF_POINTS_PER_EVENT_ZONE];
    ITR3800_Condition_t conditions[ITR3800_MAX_NR_OF_CONDITIONS];
    ITR3800_EventZoneType_t zoneType;    /* EventZone Type */
    uint8_t phaseNumber;
    uint8_t outputNumber;
    uint16_t eventmessage_delay;
    uint16_t eventmessage_extend;
    bool eta_enable;
    ITR3800_PointXY_t etaPoint;
} ITR3800_EventZone_t;

typedef struct {
    ITR3800_EventZone_t eventZones[ITR3800_MAX_NR_OF_EVENTZONES];
} ITR3800_EventZones_t;

/* ignore zone struct */
typedef struct {
    bool enable;
    bool eventFlag;
    char zoneName[ITR3800_MAX_LENGTH_EVENTZONE_NAME];
    uint8_t zoneNameLength;
    uint32_t nrOfZonePoints;
    ITR3800_PointXY_t zoneData[ITR3800_MAX_NR_OF_POINTS_PER_IGNORE_ZONE];
    bool ignoreEverything;
} ITR3800_IgnoreZone_t;

typedef struct {
    ITR3800_IgnoreZone_t ignoreZones[ITR3800_MAX_NR_OF_IGNOREZONES];
} ITR3800_IgnoreZones_t;

/* description */
typedef struct{
    char description[ITR3800_MAX_LENGTH_DESCRIPTION_NAME];
    uint8_t descriptionLength;
}ITR3800_Description_t;

/* self test */
typedef struct{
    uint32_t errorPowerSupply:1;
    uint32_t errorAquisition:1;
    uint32_t errorRxPath:1;
    uint32_t errorIncSensor:1;
    uint32_t errorGpsSensor:1;
    uint32_t errorCalibData:1;
    uint32_t errorPeripherie:1;
    uint32_t errorTemperature:1;
    uint32_t errorInterface:1;

    uint32_t reserved:23;
}ITR3800_SelfTestFlags_t;

typedef union{
    ITR3800_SelfTestFlags_t flags;
    uint32_t all;
}ITR3800_SelfTest_u;

/* a buffer containing a png image with complete header */
typedef struct{
    uint32_t size;

    uint8_t *mem;
}ITR3800_PNGBuf;

/* GPS satellites in view */
typedef struct{
    char talkerId_au8[2];
    uint16_t satelliteId_u16;
    uint16_t elevation_deg_u16;
    uint16_t azimuth_deg_u16;
    uint16_t signalStrength_u16;
}ITR3800_GpsSatelliteProperties_t;

typedef struct{
    uint32_t nrOfGpsSatellitesInView;
    ITR3800_GpsSatelliteProperties_t satellites[32];
}ITR3800_GpsSatellitesInView_t;

typedef struct APIHandle *APIHandle_t;


#ifdef __cplusplus
}
#endif

#endif // ITR3800_RADARAPI_STRUCTS_H
