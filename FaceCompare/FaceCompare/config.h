#pragma once

#define sizeOfFeature 1032
#define sizeOfName 1024

#define SafeFree(p) { if ((p)) free(p); (p) = NULL; }
#define SafeArrayDelete(p) { if ((p)) delete [] (p); (p) = NULL; }
#define SafeDelete(p) { if ((p)) delete (p); (p) = NULL; }



#ifdef _WIN32
#define APPID "F7vkKXYJv6H4Bouwm54nJbZy5M9EoxF9PMoSSGx817Yv"
#define SDKKEY "HWNECEj34eZVbYAt7NVjmspAoTrYABUamezb47rMCCgE"

#else
#define APPID "F7vkKXYJv6H4Bouwm54nJbZy5M9EoxF9PMoSSGx817Yv"
#define SDKKEY "HWNECEj34eZVbYAt7NVjmspAoTrYABUamezb47rMCCgE"

#endif // 

