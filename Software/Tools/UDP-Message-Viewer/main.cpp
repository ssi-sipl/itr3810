//if using MSVC, please do not uncomment the following line:
//#pragma comment(lib, "ws2_32.lib")
//
//

//the program is compatible for Windows and Linux
#ifdef _WIN32
    #include <winsock2.h>
    #include <Ws2tcpip.h>
    #include <Windows.h>
#else
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <netinet/in.h>
    #include <arpa/inet.h>
    #include <time.h>
    #include <errno.h>
#endif
#include <stdlib.h>
#include <stdio.h>
#include <string.h>





int main()
{
  char* group = "239.255.43.21";
  int port = 62200;
  char buf[256];
  sockaddr_in remoteAddr;
  long rc;

#ifdef _WIN32
  SOCKET s;
  int remoteAddrLen=sizeof(sockaddr_in);
  WSADATA wsa;
  rc = WSAStartup(MAKEWORD(2,0),&wsa);
#else
  int s;
  socklen_t remoteAddrLen=sizeof(sockaddr_in);
#endif

  //create UDP Socket
  s=socket(AF_INET,SOCK_DGRAM,0);
#if _WIN32
  if(s==INVALID_SOCKET){
      printf("Fehler: Der Socket konnte nicht erstellt werden, fehler code: %d\n",WSAGetLastError());
      return 1;
  }
#else
  if(s==-1){
      printf("Fehler: Der Socket konnte nicht erstellt werden, fehler code: %d\n",errno);
      return 1;
  }
#endif

      struct sockaddr_in addr;
      memset(&addr, 0, sizeof(addr));
      addr.sin_family = AF_INET;
      addr.sin_addr.s_addr = htonl(INADDR_ANY); // differs from sender
      addr.sin_port = htons(port);

//binding the socket
  #if _WIN32
  rc=bind(s,(SOCKADDR*)&addr,sizeof(sockaddr_in));
  if(rc==SOCKET_ERROR)
  {
    printf("Fehler: bind, fehler code: %d\n",WSAGetLastError());
    return 1;
  }
  else
  {
    printf("ready for reading data\n");
  }
#else
      rc=bind(s,(struct sockaddr *)&addr,sizeof(sockaddr_in));
      if(rc==-1)
      {
        printf("Fehler: bind, fehler code: %d\n",errno);
        return 1;
      }
      else
      {
        printf("ready for reading data\n");
      }
#endif

  struct ip_mreq mreq;
  mreq.imr_multiaddr.s_addr = inet_addr(group);
  mreq.imr_interface.s_addr = htonl(INADDR_ANY);
  if (
      setsockopt(
          s, IPPROTO_IP, IP_ADD_MEMBERSHIP, (char*) &mreq, sizeof(mreq)
      ) < 0
  ){
      perror("setsockopt");
      return 1;
  }
  while(1)
  {
//reading the UDP Messages
    #if _WIN32
    rc=recvfrom(s,buf,256,0,(struct sockaddr*)&remoteAddr,&remoteAddrLen);
    if(rc==SOCKET_ERROR)
    {
      printf("Fehler: recvfrom, fehler code: %d\n",WSAGetLastError());
      return 1;
    }
    else
    {
      buf[rc]='\0';

      printf("%u.%u.%u.%u received data: %s\n",remoteAddr.sin_addr.S_un.S_un_b.s_b1,remoteAddr.sin_addr.S_un.S_un_b.s_b2, remoteAddr.sin_addr.S_un.S_un_b.s_b3, remoteAddr.sin_addr.S_un.S_un_b.s_b4,buf );

       }
    #else
      rc=recvfrom(s,buf,256,0,(struct sockaddr *)&remoteAddr,&remoteAddrLen);
      if(rc==-1)
      {
        printf("Fehler: recvfrom, fehler code: %d\n",errno);
        return 1;
      }
      else
      {
        buf[rc]='\0';
        char ip[30];
        strcpy(ip, (char*)inet_ntoa((struct in_addr)remoteAddr.sin_addr));
        printf("%s received data: %s\n", ip,buf);
         }
    #endif
  }
  return 0;
}


