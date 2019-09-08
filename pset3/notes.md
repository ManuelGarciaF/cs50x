#Notes on pset3

##`fread()` and `fwrite()`

The function `fread()` reads nmemb items of data, each size bytes long, from the stream pointed to by stream, storing them at the location given by ptr.

The function `fwrite()` writes nmemb items of data, each size bytes long, to the stream pointed to by stream, obtaining them from the location given by ptr.


```C
#include <stdio.h>

size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream);

size_t fwrite(const void *ptr, size_t size, size_t nmemb,
 FILE *stream);
```

##`fseek()`

```C
int fseek(FILE *stream, long offset, int whence);
```


