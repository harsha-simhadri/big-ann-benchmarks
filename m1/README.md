
My notes for running on M1:

General troubleshooting:
* upgrade to a recent docker desktop
* install docker AFTER installing developer support 
* make sure docker python package is at right version 
* make sure docker-py is NOT installed ( if so, uninstall and reinstall docker package )

faiss troubleshooting:
* QEMU may not be emulating AVX, so switch to building libfaiss.so not libfaiss_avx.so


