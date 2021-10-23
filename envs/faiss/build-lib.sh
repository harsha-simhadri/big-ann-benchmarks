#conda install six mkl mkl_random mkl_fft mkl-service 

# Build libfaiss.so/libfaiss_avx2.so.
../cmake/bin/cmake -B _build \
      -DBUILD_SHARED_LIBS=ON \
      -DBUILD_TESTING=OFF \
      -DFAISS_ENABLE_GPU=OFF \
      -DFAISS_ENABLE_PYTHON=ON \
      -DPython_EXECUTABLE=$PYTHON \
      -DBLA_VENDOR=Intel10_64_dyn \
      -DFAISS_OPT_LEVEL=avx2 \
      -DMKL_LIBRARIES=/root/anaconda3/lib \
      -DCMAKE_INSTALL_LIBDIR=/root/anaconda3/lib \
      -DCMAKE_BUILD_TYPE=Release .

make -C _build -j $CPU_COUNT 
