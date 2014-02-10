#!/usr/bin/python

from OleFileIO_PL import *   
import numpy as np
import h5py 
import nxs
import sys
import struct
import datetime
import time
import argparse



# Questions for Xradia:
# Where is the sample name? They will answer me that after holidays.
# Orientation of the axis in microscope X, Y, Z: z is direction of beamlight, y normal to the floor (image plane), x parallel to the floor (image plane).

# Questions for NeXus:

# What is the distance? (self.nxinstrument['sample']['distance']=
# (1'float': it is the distance between the sample and the detector. 
# Look if I cand find it inside the .txrm). ((self.nxinstrument['sample']['distance']='float'))

# Control monitor. What is exactly that? What we should do? We put 1s for the moment. We think that is a diode controlling the intensity of the beamlight, but we don't have this kind of measure in mistral.

# PositionsX, Y, Z. What is exactly that? SampleX, SampleY, SampleZ (in micrometers from the 0 of the motor)

# Float images will never be accepted in Nexus?

# We don't have any dark-field. Dark-field is mandatory?

# FlatField corresponds to the BrightField?



class mosaicnex:

    def __init__(self, mosaic_file_xrm, filename_hdf5, mosaicfile=None, title='X-ray tomography', 
                 sourcename='ALBA', sourcetype='Synchrotron X-ray Source', 
                 sourceprobe='x-ray', instrument='BL09 @ ALBA', sample='Unknown'): 
    
        self.mosaic_file_xrm = mosaic_file_xrm
        self.filename_hdf5 = filename_hdf5
        

        """ The attribute self.metadata indicates if the metadata has been 
        # extracted or not. If metadata has not been extracted from the 'txrm' 
        file, we cannot extract the data from the images in the 'txrm'. """
        self.metadata=0
     
   

        self.title = title
        self.sourcename = sourcename
        self.sourcetype = sourcetype
        self.sourceprobe = sourceprobe
        self.instrumentname = instrument
        self.samplename = sample
        self.sampledistance = 0
        self.datatype = 'uint16' #two bytes
        self.sequence_number = 0
        self.sequence_number_sample=0
        
        self.programname = 'mosaic2nexus.py'
        self.nxentry = 0
        self.nxsample = 0
        self.nxmonitor = 0
        self.nxinstrument = 0
        self.nxdata = 0
        
        self.nxdetectorsample = 0
        
        self.numrows = 0
        self.numcols = 0
        self.nSampleFrames = 0


        self.monitorsize = self.nSampleFrames 
        self.monitorcounts = 0


        return
     
 
    def NXmosaic_structure(self):    
        #create_basic_structure
    
        self.nxentry = nxs.NXentry(name= "NXmosaic") 
           
        self.nxentry['program_name'] = self.programname
        self.nxentry['program_name'].attrs['version']='1.0'
        
        self.nxentry['title']=self.mosaic_file_xrm
        self.nxentry['definition'] = 'NXtomo'
        
        self.nxsample = nxs.NXsample()
        self.nxentry.insert(self.nxsample)
        self.nxsample['name'] = self.samplename

        self.nxmonitor = nxs.NXmonitor(name= 'control')
        self.nxentry.insert(self.nxmonitor)

        self.nxdata = nxs.NXdata()
        self.nxentry.insert(self.nxdata)

        self.nxinstrument = nxs.NXinstrument(name= 'instrument')
        self.nxinstrument['name'] = self.instrumentname        
        self.nxentry.insert(self.nxinstrument)

        self.nxsource = nxs.NXsource(name = 'source')
        self.nxinstrument.insert(self.nxsource)
        self.nxinstrument['source']['name'] = self.sourcename
        self.nxinstrument['source']['type'] = self.sourcetype
        self.nxinstrument['source']['probe'] = self.sourceprobe

        self.nxdetectorsample = nxs.NXdetector(name = 'sample')
        self.nxinstrument.insert(self.nxdetectorsample)  

        self.nxentry.save(self.filename_hdf5, 'w5')

        return 

  
        

    #### Function used to convert the metadata from .txrm to NeXus .hdf5
    def convert_metadata(self):

        verbose = False
        print("Trying to convert txrm metadata to NeXus HDF5.")
        
        #Opening the .txrm files as Ole structures
        ole = OleFileIO(self.mosaic_file_xrm)
        #txrm files have been opened

        self.nxentry['program_name'].attrs['configuration'] = (self.programname + ' ' 
                                                              + ' '.join(sys.argv[1:]))
        # SampleID
        if ole.exists('SampleInfo/SampleID'):   
            stream = ole.openstream('SampleInfo/SampleID')
            data = stream.read()
            struct_fmt ='<'+'50s' 
            samplename = struct.unpack(struct_fmt, data)
            if self.samplename != 'Unknown':
                self.samplename = samplename[0]    
            if verbose: 
                print "SampleInfo/SampleID: %s " % self.samplename 
            self.nxsample['name'] = nxs.NXfield(
                name = 'name', value = self.samplename)    
            self.nxsample['name'].write()    
        else:
            print("There is no information about SampleID")
	            
        # Pixel-size
        if ole.exists('ImageInfo/PixelSize'):   
            stream = ole.openstream('ImageInfo/PixelSize')
            data = stream.read()
            struct_fmt = '<1f'
            pixelsize = struct.unpack(struct_fmt, data)
            pixelsize = pixelsize[0]
            if verbose: 
                print "ImageInfo/PixelSize: %f " %  pixelsize  
            self.nxinstrument['sample']['x_pixel_size'] = nxs.NXfield(
                name='x_pixel_size', value = pixelsize, attrs = {'units': 'um'})
            self.nxinstrument['sample']['x_pixel_size'].write()    
            self.nxinstrument['sample']['y_pixel_size'] = nxs.NXfield(
                name='y_pixel_size', value = pixelsize, attrs = {'units': 'um'}) 
            self.nxinstrument['sample']['y_pixel_size'].write()    
        else:
            print("There is no information about PixelSize")

        # Accelerator current (machine current)
        if ole.exists('ImageInfo/Current'):   
            stream = ole.openstream('ImageInfo/Current')
            data = stream.read()
            struct_fmt = '<1f'
            current = struct.unpack(struct_fmt, data)
            current = current[0]
            if verbose: 
                print "ImageInfo/Current: %f " %  current  
            self.nxinstrument['sample']['current'] = nxs.NXfield(
                name = 'current', value=current, attrs = {'units': 'mA'})
            self.nxinstrument['sample']['current'].write()
        else:
            print("There is no information about Current")
    
	# Tomography data size 
        if (ole.exists('ImageInfo/NoOfImages') and 
            ole.exists('ImageInfo/ImageWidth') and 
            ole.exists('ImageInfo/ImageHeight')):                  
                    
            stream = ole.openstream('ImageInfo/NoOfImages')
            data = stream.read()
            nimages = struct.unpack('<I', data)
            if verbose: 
                print "ImageInfo/NoOfImages = %i" % nimages[0] 
            self.nSampleFrames = np.int(nimages[0])
        
            stream = ole.openstream('ImageInfo/ImageHeight')
            data = stream.read()
            ximage = struct.unpack('<I', data)    
            if verbose: 
                print "ImageInfo/ImageHeight = %i" % ximage[0]  
            self.numrows = np.int(ximage[0])
            
            stream = ole.openstream('ImageInfo/ImageWidth')
            data = stream.read()
            yimage = struct.unpack('<I', data)
            if verbose: 
                print "ImageInfo/ImageWidth = %i" % yimage[0]  
            self.numcols = np.int(yimage[0])

        else:
            print('There is no information about the tomography size (ImageHeight,'
            'ImageWidth or Number of images)')
 
        # Energy            	
        if ole.exists('ImageInfo/Energy'):
            stream = ole.openstream('ImageInfo/Energy')
    	    data = stream.read()
     	    struct_fmt = "<{0:10}f".format(self.nSampleFrames)
       	    try: #we found some txrm images (flatfields) with different encoding of data
                energies = struct.unpack(struct_fmt, data)
            except struct.error:
                print >> sys.stderr, 'Unexpected data length (%i bytes). Trying to unpack energies with: "f"+"36xf"*(nSampleFrames-1)'%len(data) 
                struct_fmt = '<'+"f"+"36xf"*(self.nSampleFrames-1)
                energies = struct.unpack(struct_fmt, data)
            if verbose: print "ImageInfo/Energy: \n ",  energies  
            self.nxinstrument['source']['energy'] = nxs.NXfield(
                name = 'energy', value = energies, attrs = {'units': 'eV'}) 
            self.nxinstrument['source']['energy'].write()
        else:
            print('There is no information about the energies with which '  
                   'have been taken the different tomography images')

        # DataType: 10 float; 5 uint16 (unsigned 16-bit (2-byte) integers)
        if ole.exists('ImageInfo/DataType'):                  
            stream = ole.openstream('ImageInfo/DataType')
            data = stream.read()
            struct_fmt = '<1I'
            datatype = struct.unpack(struct_fmt, data)
            datatype = int(datatype[0])
            if datatype == 5:
                self.datatype = 'uint16'
            else:
                self.datatype = 'float'
            if verbose: 
                print "ImageInfo/DataType: %s " %  self.datatype      
        else:
            print("There is no information about DataType")

        # Start and End Times 
        if ole.exists('ImageInfo/Date'):  
            stream = ole.openstream('ImageInfo/Date')       
            data = stream.read()
            dates = struct.unpack('<'+'17s23x'*self.nSampleFrames, data) 
            
            startdate = dates[0]
            [day, hour] = startdate.split(" ")
            [month, day, year] = day.split("/")
            [hour, minute, second] = hour.split(":")    
            
            year = '20'+year
            year = int(year)   
            month = int(month)
            day = int(day)
            hour = int(hour)
            minute = int(minute)
            second = int(second)

            starttime = datetime.datetime(year, month, day, 
                                          hour, minute, second)                 
            starttimeiso = starttime.isoformat()
            times = time.mktime(starttime.timetuple())

            if verbose: 
                print "ImageInfo/Date = %s" % starttimeiso 
            self.nxentry['start_time'] = str(starttimeiso)
            self.nxentry['start_time'].write()    

            enddate = dates[self.nSampleFrames-1]    
            [endday, endhour] = enddate.split(" ")
            [endmonth, endday, endyear] = endday.split("/")
            [endhour, endminute, endsecond] = endhour.split(":")

            endyear = '20'+endyear
            endyear = int(endyear)   
            endmonth = int(endmonth)
            endday = int(endday)
            endhour = int(endhour)
            endminute = int(endminute)
            endsecond = int(endsecond)

            endtime = datetime.datetime(endyear, endmonth, endday, 
                                        endhour, endminute, endsecond)                 
            endtimeiso = endtime.isoformat()
            endtimes = time.mktime(endtime.timetuple())   
            
            if verbose: 
                print "ImageInfo/Date = %s" % endtimeiso 
            self.nxentry['end_time']= str(endtimeiso)
            self.nxentry['end_time'].write()

        else:
            print("There is no information about Date")

        # Sample rotation angles 
        if ole.exists('ImageInfo/Angles'):    
            stream = ole.openstream('ImageInfo/Angles')
            data = stream.read()
            struct_fmt = '<{0:10}f'.format(self.nSampleFrames)
            angles = struct.unpack(struct_fmt, data)
            if verbose: 
                print "ImageInfo/Angles: \n ",  angles
            self.nxsample['rotation_angle'] = nxs.NXfield(
                name = 'rotation_angle', value=angles, attrs={'units': 'degrees'})
            self.nxsample['rotation_angle'].write() 
            self.nxdata['rotation_angle'] = nxs.NXlink(
                target = self.nxsample['rotation_angle'], group=self.nxdata)
            self.nxdata['rotation_angle'].write()

        else:
            print('There is no information about the angles at' 
                   'which have been taken the different tomography images')

        # Sample translations in X, Y and Z 
        # X sample translation: nxsample['z_translation']
        if ole.exists('ImageInfo/XPosition'):

            stream = ole.openstream('ImageInfo/XPosition')
            data = stream.read()
            struct_fmt = "<{0:10}f".format(self.nSampleFrames)
            try: #we found some txrm images (flatfields) with different encoding of data #
                xpositions = struct.unpack(struct_fmt, data) 
            except struct.error:
                print >> sys.stderr, 'Unexpected data length (%i bytes). Trying to unpack XPositions with: "f"+"36xf"*(nSampleFrames-1)'%len(data) 
                struct_fmt = '<'+"f"+"36xf"*(self.nSampleFrames-1)
                xpositions = struct.unpack(struct_fmt, data)
            if verbose: 
                print "ImageInfo/XPosition: \n ",  xpositions  

            self.nxsample['x_translation'] = nxs.NXfield(
                name = 'x_translation', value=xpositions, attrs={'units': 'mm'})   
            self.nxsample['x_translation'].write()

        else:
            print("There is no information about xpositions")

        # Y sample translation: nxsample['z_translation']
        if ole.exists('ImageInfo/YPosition'):

            stream = ole.openstream('ImageInfo/YPosition')
            data = stream.read()
            struct_fmt = "<{0:10}f".format(self.nSampleFrames)
            try: #we found some txrm images (flatfields) with different encoding of data.
                ypositions = struct.unpack(struct_fmt, data) 
            except struct.error:
                print >> sys.stderr, 'Unexpected data length (%i bytes). Trying to unpack YPositions with: "f"+"36xf"*(nSampleFrames-1)'%len(data) 
                struct_fmt = '<'+"f"+"36xf"*(self.nSampleFrames-1)
                ypositions = struct.unpack(struct_fmt, data)
            if verbose: 
                print "ImageInfo/YPosition: \n ",  ypositions  
      
            self.nxsample['y_translation'] = nxs.NXfield(
                name = 'y_translation', value=ypositions, attrs={'units': 'mm'})   
            self.nxsample['y_translation'].write()

        else:
            print("There is no information about xpositions")

        # Z sample translation: nxsample['z_translation']
        if ole.exists('ImageInfo/ZPosition'):

            stream = ole.openstream('ImageInfo/ZPosition')
            data = stream.read()
            struct_fmt = "<{0:10}f".format(self.nSampleFrames)
            try: #we found some txrm images (flatfields) with different encoding of data.
                zpositions = struct.unpack(struct_fmt, data)
            except struct.error:
                print >> sys.stderr, 'Unexpected data length (%i bytes). Trying to unpack ZPositions with: "f"+"36xf"*(nSampleFrames-1)'%len(data)
                struct_fmt = '<'+"f"+"36xf"*(self.nSampleFrames-1)
                zpositions = struct.unpack(struct_fmt, data)
            if verbose: 
                print "ImageInfo/ZPosition: \n ",  zpositions  
      
            self.nxsample['z_translation'] = nxs.NXfield(
                name = 'z_translation', value=zpositions, attrs={'units': 'mm'})   
            self.nxsample['z_translation'].write()

        else:
            print("There is no information about xpositions")

        # NXMonitor data: Not used in TXM microscope. 
        # Used to normalize in function fo the beam intensity (to verify). 
        # In the ALBA-BL09 case all the values will be set to 1.
        self.monitorsize = self.nSampleFrames
        self.monitorcounts = np.ones((self.monitorsize), dtype= np.uint16)
        self.nxmonitor['data'] = nxs.NXfield(
            name='data', value=self.monitorcounts)
        self.nxmonitor['data'].write()        
        self.metadata=1

        ole.close()
        print ("Meta-Data conversion from 'txrm' to NeXus HDF5 has been done.\n")  
        return

    


    
    #### Converts a Mosaic image fromt txrm to NeXus hdf5.    
    def convert_mosaic(self): 
        verbose = False
        print("Converting mosaic image data from txrm to NeXus HDF5.")

        #Opening the mosaic .xrm file as an Ole structure.
        olemosaic = OleFileIO(self.mosaic_file_xrm)

        # Mosaic data image
        self.nxinstrument['sample']['data'] = nxs.NXfield(
            name='data', dtype=self.datatype , shape=[self.numrows, self.numcols])
        self.nxinstrument['sample']['data'].attrs['Data Type']=self.datatype 
        self.nxinstrument['sample']['data'].attrs['Number of Subimages']=self.nSampleFrames
        self.nxinstrument['sample']['data'].attrs['Image Height']=self.numrows
        self.nxinstrument['sample']['data'].attrs['Image Width']=self.numcols
        self.nxinstrument['sample']['data'].write()

        img_string = "ImageData1/Image1"
        stream = olemosaic.openstream(img_string)

        slab_offset = [0, 0]
        for i in range(0, self.numrows):
            
            if self.datatype == 'uint16':    
                if (i%100 == 0):
                    print('Mosaic row %i is being converted' % (i+1))
                dt = np.uint16
                data = stream.read(self.numcols*2)              
                imgdata = np.frombuffer(data, dtype=dt, count=self.numcols)
                imgdata = np.reshape(imgdata, (1, self.numcols), order='A')
                slab_offset = [i, 0]
                self.nxinstrument['sample']['data'].put(imgdata, slab_offset, refresh=False)
                self.nxinstrument['sample']['data'].write()
     
            elif self.datatype == 'float':  
                if (i%100 == 0):
                    print('Mosaic row %i is being converted' % (i+1))
                dt = np.float          
                data = stream.read(self.numcols*4)                      
                imgdata = np.frombuffer(data, dtype=dt, count=self.numcols)
                imgdata = np.reshape(imgdata, (1, self.numcols), order='A')
                slab_offset = [i, 0]
                self.nxinstrument['sample']['data'].put(imgdata, slab_offset, refresh=False)
                self.nxinstrument['sample']['data'].write()

            else:                            
                print "Wrong data type"
                return
           

        self.nxdata['data'] = nxs.NXlink(target=self.nxinstrument['sample']['data'], group=self.nxdata)
        self.nxdata['data'].write()

        olemosaic.close()    
        print ("Mosaic image data conversion to NeXus HDF5 has been done.\n")
        return


    



"""from nxs import NXfield #needs Nexus v>=4.3
from nxs import napi, NeXusError
import numpy

class NXfield_comp(NXfield):
    
    #NOTE: THE CONSTRUCTOR IS OPTIONAL. IF NOT IMPLEMENTED, WE CAN STILL USE THE nxslab_dims PROPERTY
    def __init__(self, value=None, name='field', dtype=None, shape=(), group=None,
                 attrs={}, nxslab_dims=None, **attr):
        NXfield.__init__(self, value=value, name=name, dtype=dtype, shape=shape, group=group,
                 attrs=attrs, **attr)
        self._slab_dims = nxslab_dims
        
    def write(self):
        
        #Write the NXfield, including attributes, to the NeXus file.
        
        if self.nxfile:
            if self.nxfile.mode == napi.ACC_READ:
                raise NeXusError("NeXus file is readonly")
            if not self.infile:
                shape = self.shape
                if shape == (): shape = (1,)
                with self.nxgroup as path:
                    if self.nxslab_dims is not None:
                    #compress
                        path.compmakedata(self.nxname, self.dtype, shape, 'lzw', 
                                          self.nxslab_dims)
                    else:
                    # Don't use compression
                        path.makedata(self.nxname, self.dtype, shape)
                self._infile = True
            if not self.saved:            
                with self as path:
                    path._writeattrs(self.attrs)
                    value = self.nxdata
                    if value is not None:
                        path.putdata(value)
                self._saved = True
        else:
            raise IOError("Data is not attached to a file")
    
    def _getnxslabdims(self):
        try:
            return self._nxslab_dims
        except:
            slab_dims = None
        #even if slab_dims have not been set, check if the dataset is large 
        shape = self.shape or (1,)
        if numpy.prod(shape) > 10000:
            slab_dims = numpy.ones(len(shape),'i')
            slab_dims[-1] = min(shape[-1], 100000)
        return slab_dims
    
    def _setnxslabdims(self, slab_dims):
        self._nxslab_dims = slab_dims
    
    nxslab_dims = property(_getnxslabdims,_setnxslabdims,doc="Slab (a.k.a. chunk) dimensions for compression")
    """


    
    
    
    

   
