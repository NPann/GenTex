# README #

Thinning algorithm from Kalman Palagyi based on:

*A 3D 6-subiteration thinning algorithm for extracting medial lines* in Pattern Recogn. Lett. 1998. DOI: 10.1016/S0167-8655(98)00031-2

### What is this repository for? ###

The implementations is efficient, since it use a predefined look up table ( d6c_pk\d6c_pk_lut.dat ), and it assumes images store in ANALYZE file format.

Usage of the program (written is C):

./d6c_pk  inp  out

where: 

* inp : name of the input image (files inp.hdr and inp.img corresponds to zhe input image)
* out : name of the output image (the pair of files out.hdr and out.img is generated)


### How do I get set up? ###

Compile d6c_pk.c with a C-compiler

ex: clang d6c_pk.c -o build/d6c_pk