import numpy as np

class TracesBin():
    

    def __init__(self, filepath):
        '''
        Open the binary file that contains the traces.
        filepath: the path of the binary file
        '''
        self.HEAD_SIZE=26
        self.__filepath= filepath


        infile = open(self.__filepath,'rb');

        # read header
        self.__ntraces    = int.from_bytes( infile.read(4),byteorder='little', signed=False)
        self.__nsamples   = int.from_bytes( infile.read(4),byteorder='little', signed=False)
        self.__sampletype = infile.read(1).decode("ascii")
        self.__textlen    = int.from_bytes( infile.read(1),byteorder='little', signed=False)
        
        if (self.__sampletype=='f'):
            self.__sample_dtype=np.dtype('float32')
        elif (self.__sampletype=='d'):
            self.__sample_dtype=np.dtype('float64')
        else:
            assert(False)
        
        self.__rowlen = self.__textlen + self.__nsamples*self.__sample_dtype.itemsize

        self.__key = np.frombuffer(buffer= infile.read(16), dtype='uint8');
        
        infile.close()
    
    def getAllTraces(self):
        '''
        Get the whole batch of traces in order. Returns traces and plainexts matrixes.
        '''
        infile = open(self.__filepath, 'rb')

        infile.seek(self.HEAD_SIZE, 0)
        
        texts=np.zeros((self.__ntraces, self.__textlen), dtype= 'uint8');
        traces=np.zeros((self.__ntraces, self.__nsamples), dtype= self.__sample_dtype);
        
        for i in np.arange(0, self.__ntraces):
            traces[i,:]= np.frombuffer(buffer=infile.read(self.__nsamples* self.__sample_dtype.itemsize), dtype= self.__sample_dtype)
            texts[i,:]= np.frombuffer(buffer=infile.read(self.__textlen* texts.itemsize), dtype=texts.dtype)
            
        infile.close()
        return traces, texts

    def getTraces(self, idx):
        '''
        Get the traces and plaintexts with the specified index. 
        Returns traces and plaintexts matrixes with the same order of index

        Index can be an array of integers
        '''
        #check that all indexes are possible
        indexes= np.array(idx)
        
        assert np.all( indexes < self.__ntraces)
        assert np.all( indexes.dtype == 'int')

        n= len(indexes)

        infile = open(self.__filepath, 'rb')


        texts=np.zeros((n, self.__textlen), dtype= 'uint8');
        traces=np.zeros((n, self.__nsamples), dtype= self.__sample_dtype);
        j=0
        for i in indexes:
            infile.seek(self.HEAD_SIZE+ self.__rowlen*i, 0)
            traces[j,:]= np.frombuffer(buffer=infile.read(self.__nsamples* self.__sample_dtype.itemsize), dtype= self.__sample_dtype)
            texts[j,:]= np.frombuffer(buffer=infile.read(self.__textlen* texts.itemsize), dtype=texts.dtype)
            j=j+1
            
        infile.close()

        return traces, texts
    
    def getSamples(self, trace_idx, samples_idx):
        t_idx= np.array(trace_idx).reshape((len(trace_idx),1))
        s_idx= np.array(samples_idx)
        
        n= len(trace_idx)
        s= len(samples_idx)
        
        infile = open(self.__filepath, 'rb')
        
        traces=np.zeros((n, s), dtype= self.__sample_dtype)
        texts=np.zeros((n, self.__textlen), dtype= 'uint8')
        
        
        pos= self.HEAD_SIZE+ t_idx*self.__rowlen + s_idx* self.__sample_dtype.itemsize
        
        for i in range(pos.shape[0]):
            for j in range(pos.shape[1]):
                infile.seek(pos[i][j], 0)
                traces[i,j]=  np.frombuffer(buffer=infile.read(self.__sample_dtype.itemsize), dtype= self.__sample_dtype)
            
            infile.seek(self.HEAD_SIZE+ self.__rowlen* trace_idx[i] + self.__nsamples* self.__sample_dtype.itemsize , 0)
            texts[i,:]= np.frombuffer(buffer=infile.read(self.__textlen* texts.itemsize), dtype=texts.dtype)
            
        infile.close()
        
        return traces, texts

    
    def getKey(self):
        '''
        Get the used key
        '''
        return self.__key

    def getNTraces(self):
        '''
        Get the total number of traces
        '''
        return self.__ntraces
    
    def getNSamples(self):
        return self.__nsamples
