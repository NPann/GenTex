#include <math.h>

/* Generate 2-dimensional co-occurrence histograms
   P = f(i, j) where i and j are discrete image (grey) levels
   See Pattern Recognition Engineering (Morton Nadler & Eric
   P. Smith) - modified S Van Der Walt's 2D version to make
   1,2,3,4D versions - KY
*/

/* Generate from a single Nd image */

void
makecomat1D(int* input,
	    int* mask, 
	    int xi,
	    int* coords,
	    int levels, 
	    int* output) {
  int x, xval, i, j;

  for (x = 0; x < xi; x++) {
    if(mask[x] == 1) { 
      i = input[x];
      xval = x + coords[0];
      if ((xval >= 0) && (xval < xi))
	{
	  if (mask[xval] == 1)
	    {
	      j = input[xval];
	      if (i >= 0 && i < levels && j >= 0 && j < levels) {
		output[i*levels + j]++;
	      } // else raise a warning
	    }
	}
    }
  }
}

void
makecomat2D(int* input,
	    int* mask, 
	    int xi, int yi,
	    int* coords,
	    int levels, 
	    int* output) {
  int x, y, xval, yval, i, j;

  for (x = 0; x < xi; x++) {
    for (y = 0; y < yi; y++) {
      if(mask[x*yi + y] == 1)
	{ 
	  i = input[x*yi + y];
	  xval = x + coords[0];
	  yval = y + coords[1];
	    
	  if ((xval >= 0) && (xval < xi) &&
	      (yval >= 0) && (yval < yi))
	    {
	      if (mask[xval*yi + yval] == 1)
		{
		  j = input[xval*yi + yval];
		    
		  if (i >= 0 && i < levels && j >= 0 && j < levels) {
		    output[i*levels + j]++;
		  } // else raise a warning
		}
	    }
	}
    }
  }
}

void
makecomat3D(int* input,
	    int* mask, 
	    int xi, int yi, int zi,
	    int* coords,
	    int levels, 
	    int* output) {
  int x, y, z, xval, yval, zval, i, j;

  /* 5-dimensional histogram
     P = f(i, j, d, theta,phi) where i and j are grey levels
     See Pattern Recognition Engineering (Morton Nadler & Eric
     P. Smith) - modified S Van Der Walt's 2D version to make
     3D version - KY
  */

  for (x = 0; x < xi; x++) {
    for (y = 0; y < yi; y++) {
      for (z = 0; z < zi; z++) {
	if(mask[(x*yi + y)*zi + z] == 1)
	  { 
	    i = input[(x*yi + y)*zi + z];
	    
	    xval = x + coords[0];
	    yval = y + coords[1];
	    zval = z + coords[2];
	    
	    if ((xval >= 0) && (xval < xi) &&
		(yval >= 0) && (yval < yi) &&
		(zval >= 0) && (zval < zi))
	      {
		if (mask[(xval*yi + yval)*zi + zval] == 1)
		  {
		    j = input[(xval*yi + yval)*zi + zval];
		    
		    if (i >= 0 && i < levels && j >= 0 && j < levels) {
		      output[i*levels + j]++;
		    } // else raise a warning
		  }
	      }
	  }
      }
    }
  }
}

void
makecomat4D(int* input, 
	    int* mask, 
	    int xi, int yi, int zi, int ti,
	    int* coords,
	    int levels, 
	    int* output) {
  int x, y, z, t, xval, yval, zval, tval, i, j;

  for (x = 0; x < xi; x++) {
    for (y = 0; y < yi; y++) {
      for (z = 0; z < zi; z++) {
	for (t = 0; t < ti; t++) {
	  if(mask[((x*yi + y)*zi + z)*ti + t] == 1)
	    { 
	      i = input[((x*yi + y)*zi + z)*ti + t];
	    
	      xval = x + coords[0];
	      yval = y + coords[1];
	      zval = z + coords[2];
	      tval = t + coords[3];
	    
	      if ((xval >= 0) && (xval < xi) &&
		  (yval >= 0) && (yval < yi) &&
		  (zval >= 0) && (zval < zi) &&
		  (tval >= 0) && (tval < ti))
		{
		  if (mask[((xval*yi + yval)*zi + zval)*ti + tval] == 1)
		    {
		      j = input[((xval*yi + yval)*zi + zval)*ti + tval];
		    
		      if (i >= 0 && i < levels && j >= 0 && j < levels) {
			output[i*levels + j]++;
		      } // else raise a warning
		    }
		}
	    }
	}
      }
    }
  }
}

/* Generate from a pair of Nd images */

void
makecomat1D_2T(int* input1,
	       int* mask1, 
	       int xi1,
	       int* input2,
	       int* mask2, 
	       int xi2,
	       int* coords,
	       int levels1, int levels2, 
	       int* output) {
  int x, xval, i, j;

  for (x = 0; x < xi1; x++) {
    if(mask1[x] == 1) { 
      i = input1[x];
      xval = x + coords[0];
      if ((xval >= 0) && (xval < xi1))
	{
	  if (mask2[xval] == 1)
	    {
	      j = input2[xval];
	      if (i >= 0 && i < levels1 && j >= 0 && j < levels2) {
		output[i*levels2 + j]++;
	      } // else raise a warning
	    }
	}
    }
  }
}

void
makecomat2D_2T(int* input1,
	       int* mask1, 
	       int xi1, int yi1,
	       int* input2,
	       int* mask2, 
	       int xi2, int yi2,
	       int* coords,
	       int levels1, int levels2, 
	       int* output) {
  int x, y, xval, yval, i, j;

  for (x = 0; x < xi1; x++) {
    for (y = 0; y < yi1; y++) {
      if(mask1[x*yi1 + y] == 1)
	{ 
	  i = input1[x*yi1 + y];
	  xval = x + coords[0];
	  yval = y + coords[1];
	    
	  if ((xval >= 0) && (xval < xi1) &&
	      (yval >= 0) && (yval < yi1))
	    {
	      if (mask2[xval*yi2 + yval] == 1)
		{
		  j = input2[xval*yi2 + yval];
		    
		  if (i >= 0 && i < levels1 && j >= 0 && j < levels2) {
		    output[i*levels2 + j]++;
		  } // else raise a warning
		}
	    }
	}
    }
  }
}

void
makecomat3D_2T(int* input1,
	       int* mask1, 
	       int xi1, int yi1, int zi1,
	       int* input2,
	       int* mask2, 
	       int xi2, int yi2, int zi2,
	       int* coords,
	       int levels1, int levels2, 
	       int* output) {
  int x, y, z, xval, yval, zval, i, j;

  /* 5-dimensional histogram
     P = f(i, j, d, theta,phi) where i and j are grey levels
     See Pattern Recognition Engineering (Morton Nadler & Eric
     P. Smith) - modified S Van Der Walt's 2D version to make
     3D version - KY
  */

  for (x = 0; x < xi1; x++) {
    for (y = 0; y < yi1; y++) {
      for (z = 0; z < zi1; z++) {
	if(mask1[(x*yi1 + y)*zi1 + z] == 1)
	  { 
	    i = input1[(x*yi1 + y)*zi1 + z];
	    
	    xval = x + coords[0];
	    yval = y + coords[1];
	    zval = z + coords[2];
	    
	    if ((xval >= 0) && (xval < xi1) &&
		(yval >= 0) && (yval < yi1) &&
		(zval >= 0) && (zval < zi1))
	      {
		if (mask2[(xval*yi2 + yval)*zi2 + zval] == 1)
		  {
		    j = input2[(xval*yi2 + yval)*zi2 + zval];
		    
		    if (i >= 0 && i < levels1 && j >= 0 && j < levels2) {
		      output[i*levels2 + j]++;
		    } // else raise a warning
		  }
	      }
	  }
      }
    }
  }
}

void
makecomat4D_2T(int* input1,
	       int* mask1, 
	       int xi1, int yi1, int zi1, int ti1,
	       int* input2,
	       int* mask2, 
	       int xi2, int yi2, int zi2, int ti2,
	       int* coords,
	       int levels1, int levels2,
	       int* output) {
  int x, y, z, t, xval, yval, zval, tval, i, j;

  for (x = 0; x < xi1; x++) {
    for (y = 0; y < yi1; y++) {
      for (z = 0; z < zi1; z++) {
	for (t = 0; t < ti1; t++) {
	  if(mask1[((x*yi1 + y)*zi1 + z)*ti1 + t] == 1)
	    { 
	      i = input1[((x*yi1 + y)*zi1 + z)*ti1 + t];
	    
	      xval = x + coords[0];
	      yval = y + coords[1];
	      zval = z + coords[2];
	      tval = t + coords[3];
	    
	      if ((xval >= 0) && (xval < xi1) &&
		  (yval >= 0) && (yval < yi1) &&
		  (zval >= 0) && (zval < zi1) &&
		  (tval >= 0) && (tval < ti1))
		{
		  if (mask2[((xval*yi2 + yval)*zi2 + zval)*ti2 + tval] == 1)
		    {
		      j = input2[((xval*yi2 + yval)*zi2 + zval)*ti2 + tval];
		    
		      if (i >= 0 && i < levels1 && j >= 0 && j < levels2) {
			output[i*levels2 + j]++;
		      } // else raise a warning
		    }
		}
	    }
	}
      }
    }
  }
}

