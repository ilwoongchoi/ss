#!/usr/bin/env python3
#
# LabcomDataDat.py
#
# 2023-12-27 ver.1.0.0
# 2023-12-28 ver.1.0.1
#
import sys
import os
import struct
import datetime
import zlib
class LabcomDataCommon():
    def __init__(self) :
        self.dummy=0

    def timestamp(self) -> int:
        dt = datetime.datetime(self.saved_year, self.saved_mon,self.saved_day , \
             self.saved_hour, self.saved_min , self.saved_sec, 0)
        return int(dt.timestamp())

    def saved_time(self) -> str:
        if 71 > self.saved_year or ( 200 < self.saved_year and 1980 > self.saved_year ) :
             return "UNDEF"
        dt = datetime.datetime(self.saved_year, self.saved_mon,self.saved_day , \
             self.saved_hour, self.saved_min , self.saved_sec, 0)
        return dt.strftime('"%a, %d %b %Y %H:%M:%S +0900"')

    def module_group_string(self):
        MODULE_G_NAME = { 0:'NoGroup', 3:'ANY', 1:'CAMAC', 2:'WE7000', 4:'CompactPCI/PXI', 5:'WE7000' }
        if self.module_group in MODULE_G_NAME:
            return (MODULE_G_NAME[self.module_group])
        else:
            print('ModuleGroup: ',self.module_group)
            return ("UNDEF")

    def module_type_string(self):
        MODULE_T_NAME = { 0:'NoModule',
            1:'Aurora14', 2:'TOYO629', 3:'SEGDCM', 4:'SEGADC', 5:'DMOD',
            6:'CTS308', 7:'CTS419', 8:'CTS504', 9:'TEST', 10:'General',
            11:'CANE_N209', 12:'CANE_N470', 13:'CPS412', 14:'HOUSIN_C012_1', 15:'HOUSIN_C012_2',
            16:'DTS', 17:'CTS606B', 18:'RPC330', 19:'CPHA1210', 20:'MIC480_5',
            91:'PXI6115', 92:'PXI6602', 93:'PXI1409', 94:'PXI1411', 101:'PXI6133',
            121:'WE800',	122:'WE7272', 123:'WE7251', 124:'WE7275', 125:'WE7273',
	         126:'WE7562', 127:'WE7271' }

        if self.module_type in MODULE_T_NAME:
            return (MODULE_T_NAME[self.module_type])
        else:
            return ("UNDEF")

    def data_type_string(self):
        DATA_T_NAME = { 1:'RAW', 2:'ANA', 3:'PPM'}
        if self.data_type in DATA_T_NAME:
            return (DATA_T_NAME[self.data_type])
        else:
            return ("DEF")

    def make_channel_file(self, diag_name: str, shot_no:int , sub_shot:int, savepath: str ):
        path_w = "%s/%s-%d-%d-%d.prm" % (savepath, diag_name, shot_no, sub_shot, self.channel_number)
        try :
            mod_type = self.module_type_string()
        except :
            mod_type = diag_name

        with open(path_w, mode='x') as f:
            f.write("%s,%s,%s,1\n" % (mod_type, "DiagnosticsName", diag_name))
            f.write("%s,%s,%d,4\n" % (mod_type, "Shot", shot_no))
            f.write("%s,%s,%d,4\n" % (mod_type, "SubShot", sub_shot))
            for ch_param in self.ch_params:
                f.write("%s,%s,%s,%d\n" % (mod_type, ch_param.name, ch_param.val, ch_param.type))

        path_w = "%s/%s-%d-%d-%d.dat" % (savepath, diag_name, shot_no, sub_shot, self.channel_number)
        with open(path_w, mode='xb') as f:
            if 0 < self.comp_length :
                if 'ZLIB' in self.comp_method.upper() :
                    f.write(zlib.decompress(self.channel_comp_data) )
                else :
                    f.write(self.channel_comp_data )

    def print_update_oodbms_sql(self):
        if 0 < self.timestamp() :
            print("UPDATE oodbms\
 SET data_len=%d, comp_len=%d, channel=%d, datestamp=%d, collect=%d\
 WHERE real_arcshot=%d AND real_subshot=%d\
 AND diag_id=(SELECT diag_id FROM diag WHERE diag_name='%s');"
            % (self.total_data_size, self.total_comp_size, self.n_channels,
               self.timestamp(), self.c_channels, 
               self.shot_no, self.sub_shot, self.diag_name) )
        else :
            print("UPDATE oodbms\
 SET data_len=%d, comp_len=%d, channel=%d, collect=%d\
 WHERE real_arcshot=%d AND real_subshot=%d\
 AND diag_id=(SELECT diag_id FROM diag WHERE diag_name='%s');"
            % (self.total_data_size, self.total_comp_size, self.n_channels,
               self.c_channels,
               self.shot_no, self.sub_shot, self.diag_name) )

    def make_shot_dir(self, savepath: str):
        if '.' != savepath :
            os.makedirs(savepath, exist_ok=True)
        return (savepath)

class LabcomDataHeader():
    def __init__(self, data_bin: bytes) :
        self.data_len = len(data_bin)
#       36byte
        self.bin_len = 36
        self.next_offset = self.bin_len
#       4:fid1, 4:fid2,
#       2:fver_majar, 2:ver_minor, 4:backup_stamp,
#       2:apl_ver, 2:n_channels, 2:n_modules, 2:compiler_ver,
#       4:copyright_offset, 4:note_offset, 
#       4:channel_offset 
        header = struct.unpack_from('<2I2HI4H3I', data_bin, 0) 
        self.fid1 = header[0]
        self.fid2 = header[1]
        if (0xFFFFFFFF == self.fid1) and (0xFFFFFFFF == self.fid2) :
            self.backup_stamp = header[4]
            self.n_channels = header[6]
            self.n_modules = header[7]
            self.channel_offset = header[11]
            self.c_channels = int((len(data_bin)-header[11])/4)
            if 0 == self.n_channels :
                  self.n_channels = self.c_channels

    def check_dat_format(self) -> bool:
        if (0xFFFFFFFF == self.fid1) and (0xFFFFFFFF == self.fid2) :
            return True
        else:
            return False

    def channel_offsets(self, data_bin: bytes) -> int:
        #offset_start = len(data_bin)-self.n_channels*4
        offset_start = self.channel_offset 
        ch_offsets = []
        ofs_struct=struct.Struct('<I') # 4bytes
        for ofs in range(0, self.c_channels):
            ofs, = ofs_struct.unpack_from(data_bin, offset_start)
            ch_offsets.append(ofs)
            offset_start += 4
        return ch_offsets


class LabcomOldDataHeader(LabcomDataCommon):
    def __init__(self, data_bin: bytes) :
        self.data_len = len(data_bin)
        self.total_data_size = 0
        self.total_comp_size = 0
#       MAX 32+256byte
        self.bin_len = 288
        self.next_offset = self.bin_len
#       4:ShotNumber, 2:SubShotNumber,
#       2:LastChannel, 
#       2:Year, 2:Month, 2:Day, 2:Hour, 2:Minute, 2:Second,
#       4:ManageNumber(float), 4:VersionNumber(float), 
#       256:Comment
        self.bin_len,\
        self.shot_no, self.sub_shot, self.n_channels,\
        self.saved_year, self.saved_mon, self.saved_day,\
        self.saved_hour, self.saved_min , self.saved_sec,\
        self.manage_no, self.version_no\
            = struct.unpack_from('<2I8H2f', data_bin, 0)
        term_idx = data_bin.index(0x00,32)
        self.note = data_bin[32:term_idx].decode('shift_jis') # -'\0'
        if 0 == self.saved_year :
            self.saved_year = 1970
        if 0 == self.saved_mon :
            self.saved_mon = 1
        if 0 == self.saved_day :
            self.saved_day = 1
        self.next_offset = self.bin_len + self.n_channels*4
        self.c_channels = self.n_channels

    def channel_offsets(self, data_bin: bytes) -> int:
        offset_start = self.bin_len
        ch_offsets = []
        ofs_struct=struct.Struct('<I') # 4bytes
        for ofs in range(0, self.n_channels):
            ofs, = ofs_struct.unpack_from(data_bin, offset_start)
            ch_offsets.append(ofs)
            offset_start += 4
        return ch_offsets

    def set_total(self, data_size: int, comp_size: int):
        self.total_data_size = data_size
        self.total_comp_size = comp_size

    def set_diag(self, diag_name: str):
        self.diag_name = diag_name

    def make_shot_file(self, diag_name: str, savepath: str ):
        path_w = "%s/%s-%d-%d.shot" % (savepath, diag_name, self.shot_no, self.sub_shot)
        with open(path_w, mode='x') as f:
          f.write("%s,%s,%s,1\n" % (diag_name, "DiagnosticsName", diag_name))
          f.write("%s,%s,%d,4\n" % (diag_name, "Shot", self.shot_no))
          f.write("%s,%s,%d,4\n" % (diag_name, "SubShot", self.sub_shot))
          f.write("%s,%s,%f,1\n" % (diag_name, "ManagementNumber", self.manage_no))
          f.write("%s,%s,%f,1\n" % (diag_name, "VersionNumber", self.version_no))
          f.write("%s,%s,%s,1\n" % (diag_name, "AcquisitionDate", self.saved_time()))
          f.write("%s,%s,%s,1\n" % (diag_name, "ArchiveDate", self.saved_time()))
          f.write("%s,%s,%s,1\n" % (diag_name, "ModuleGroup", "UNDEF") )
          f.write("%s,%s,%d,4\n" % (diag_name, "ChannelNumber", self.n_channels))
          f.write("%s,%s,%d,4\n" % (diag_name, "CollectedChannel", self.c_channels))
          f.write("%s,%s,%s,1\n" % (diag_name, "Comment", self.note))

    def make_channels_dir(self, diag_name: str, savepath: str , sub_dir: bool):
        if sub_dir :
            path_d = "%s/%s-%d-%d" % (savepath, diag_name, self.shot_no, self.sub_shot)
        else :
            path_d = savepath
        if '.' != path_d :
            os.makedirs(path_d, exist_ok=True)
        return (path_d)

class LabcomDataShot(LabcomDataCommon):

    def __init__(self, data_bin: bytes, shot_offset: int =0) :
        term_idx = data_bin.index(0x00, shot_offset)
        self.module_group = 0
        self.diag_name = data_bin[shot_offset:term_idx].decode() # - '\0'
        shot_idx = term_idx+1
        next_idx = shot_idx+32
#        self.shot_bin = data_bin[shot_idx:next_idx]

        term_idx = data_bin.index(0x00,next_idx)
        self.manage = data_bin[next_idx:term_idx].decode() # -'\0'
        next_idx = term_idx+1
        term_idx = data_bin.index(0x00,next_idx)
        self.note = data_bin[next_idx:term_idx].decode('shift_jis') # -'\0'
        next_idx = term_idx+1
        self.bin_len = next_idx-shot_offset
        self.next_offset = next_idx
#
#       4:shot, 2:subshot, 2:n_channels
#       2:collectd_channels, 2:n_modules, 4:total_data_size,
#       4:total_comp_size, 2:year, 2:month,
#       2:days, 2:hour, 2:minute, 2:second 
        self.shot_no, self.sub_shot, self.n_channels, \
        self.c_channels, self.n_modules, self.total_data_size, \
        self.total_comp_size , self.saved_year, self.saved_mon, \
        self.saved_day , self.saved_hour, \
        self.saved_min , self.saved_sec\
            = struct.unpack_from('<I4H2I6H', data_bin, shot_idx)

    def set_module_group(self, module_group) :
           self.module_group = module_group

    def module_group_string(self):
        MODULE_G_NAME = { 3:'ANY', 1:'CAMAC', 2:'WE7000', 3:'PXI'}
        if self.module_group in MODULE_G_NAME:
            return (MODULE_G_NAME[self.module_group])
        else:
            return ("UNDEF")

    def make_channels_dir(self, savepath: str , sub_dir: bool):
        if sub_dir :
            path_d = "%s/%s-%d-%d" % (savepath, self.diag_name, self.shot_no, self.sub_shot)
        else :
            path_d = savepath
        if '.' != path_d :
            os.makedirs(path_d, exist_ok=True)
        return (path_d)

    def make_shot_file(self, savepath: str ):
        path_w = "%s/%s-%d-%d.shot" % (savepath, self.diag_name, self.shot_no, self.sub_shot)
        with open(path_w, mode='x') as f:
          f.write("%s,%s,%s,1\n" % (self.diag_name, "DiagnosticsName", self.diag_name))
          f.write("%s,%s,%d,4\n" % (self.diag_name, "Shot", self.shot_no))
          f.write("%s,%s,%d,4\n" % (self.diag_name, "SubShot", self.sub_shot))
          f.write("%s,%s,%s,1\n" % (self.diag_name, "ManagementVersion", self.manage))
          f.write("%s,%s,%s,1\n" % (self.diag_name, "AcquisitionDate", self.saved_time()))
          f.write("%s,%s,%s,1\n" % (self.diag_name, "ArchiveDate", self.saved_time()))
          f.write("%s,%s,%s,1\n" % (self.diag_name, "ModuleGroup", self.module_group_string()))
          f.write("%s,%s,%d,4\n" % (self.diag_name, "ModuleNumber", self.n_modules))
          f.write("%s,%s,%d,4\n" % (self.diag_name, "ChannelNumber", self.n_channels))
          f.write("%s,%s,%d,4\n" % (self.diag_name, "CollectedChannel", self.c_channels))
          f.write("%s,%s,%s,1\n" % (self.diag_name, "Comment", self.note))
#          f.write("%s,%s,%d,7\n" % (self.diag_name, "TimeStamp", self.timestamp()))
#          f.write("%s,%s,%d,7\n" % (self.diag_name, "TotalDataLength", self.total_data_size))
#          f.write("%s,%s,%d,7\n" % (self.diag_name, "TotalCompLength", self.total_comp_size))
#          f.write("%s,%s,%d,1\n" % (self.diag_name, "SiteName","LHD"))

class LabcomDataChParamStruct():
    def __init__(self, data_bin: bytes, my_offset: int =0) :
        self.bin_len = 18
        self.name_offset, self.name_size, \
        self.val_offset, self.val_size, self.val_type\
            = struct.unpack_from('<4IH', data_bin, my_offset)
        self.next_offset = my_offset+self.bin_len

class LabcomDataChParam():
    bin_form=['','','<b','<h','<i','<f','<d','<q'] # undef,str,char,short,int,float,double,int64 
    def __init__(self, name, val, vtype) :
        if isinstance(name, bytes ) :
            self.name = name[0:name.find(0x00)].decode()
        elif isinstance(name, str) :
            self.name = name
        else :
            self.name = str(name)

        if isinstance(val, bytes ) :
            if 1 == vtype :
                self.val = val[0:val.find(0x00)].decode()
            elif 1 < vtype and vtype < 8 :
                self.val, = struct.unpack(self.bin_form[vtype], val)
            else :
                self.val = val
        else :
            self.val = val

        self.type = vtype
		

class LabcomDataChParams():
    def __init__(self, param_defines, data_bin: bytes, params_offset: int =0) :
        self.params = []
        self.next_offset = 0
        for pdef in param_defines:
            sofs = params_offset + pdef.name_offset
            eofs = sofs + pdef.name_size
            vsofs = params_offset + pdef.val_offset
            veofs = vsofs + pdef.val_size
            self.params.append( LabcomDataChParam(\
                data_bin[sofs:eofs], data_bin[vsofs:veofs], pdef.val_type) )
            if( self.next_offset < eofs  ) :
                self.next_offset = eofs   
            if( self.next_offset < veofs  ) :
                self.next_offset = veofs
        self.bin_len = self.next_offset-params_offset
	

class LabcomDataChannel(LabcomDataCommon):
    def __init__(self, data_bin: bytes, channel_offset: int =0) :
        channel_head = struct.unpack_from('<2B2HB2I', data_bin, channel_offset) # 15bytes
        self.module_group =  channel_head[0]	# 3 ANY
        self.module_type =  channel_head[1]	# 10 General
        self.channel_number =  channel_head[2]
        self.data_type =  channel_head[3]
        self.value_len =  channel_head[4]
#        self.undef_buffer =  channel_head[5]
        self.data_length =  channel_head[5]
        self.comp_length =  channel_head[6]
        next_idx = channel_offset+15
        term_idx = data_bin.index(0x00, next_idx)
        self.comp_method = data_bin[next_idx:term_idx].decode() # -'\0'
        next_idx = term_idx+1
        term_idx = data_bin.index(0x00, next_idx)
        self.comp_version = data_bin[next_idx:term_idx].decode() # -'\0'
        next_idx = term_idx+1
        term_idx = data_bin.index(0x00, next_idx)
        self.manage_version = data_bin[next_idx:term_idx].decode() # -'\0'
        next_idx = term_idx+1
        term_idx = data_bin.index(0x00, next_idx)
        self.channel_note = data_bin[next_idx:term_idx].decode('shift_jis') # -'\0'
        next_idx = term_idx+1
        self.ver_no = self.manage_version.split(".")
        if 2 > len(self.ver_no) :
            self.ver_no.append('0')
        tmp_params = []
        tmp_params.append(LabcomDataChParam("ChannelNumber",self.channel_number,4))
        tmp_params.append(LabcomDataChParam("ModuleGroup",self.module_group_string(),1)) # self.module_group
        tmp_params.append(LabcomDataChParam("ModuleType",self.module_type_string(),1)) # self.module_type
        tmp_params.append(LabcomDataChParam("ManagementVersion",self.manage_version,1))
        tmp_params.append(LabcomDataChParam("DataType",self.data_type_string(),1)) # self.data_type
        if 0 != self.value_len :
            tmp_params.append(LabcomDataChParam("Resolution(bit)",self.value_len,4)) # self.value_len
        tmp_params.append(LabcomDataChParam("DataLength(byte)",self.data_length,4))
        tmp_params.append(LabcomDataChParam("CompLength(byte)",self.comp_length,4))
        tmp_params.append(LabcomDataChParam("CompressionMethod",self.comp_method,1))
        tmp_params.append(LabcomDataChParam("CompressionVersion",self.comp_version,1))
        tmp_params.append(LabcomDataChParam("Comment",self.channel_note,1))
        if '1' == self.ver_no[1] :
            term_idx = data_bin.index(0x00, next_idx)
            self.signal_name = data_bin[next_idx:term_idx].decode() # -'\0'
            next_idx = term_idx+1
            term_idx = data_bin.index(0x00, next_idx)
            self.dts_source = data_bin[next_idx:term_idx].decode() # -'\0'
            next_idx = term_idx+1
            term_idx = data_bin.index(0x00, next_idx)
            term_32 = next_idx+31 if 31 < (term_idx-next_idx) else term_idx
            self.dts_host_id = data_bin[next_idx:term_32].decode('shift_jis') # -'\0'
            next_idx = term_idx+1
            term_idx = data_bin.index(0x00, next_idx)
            term_32 = next_idx+31 if 31 < (term_idx-next_idx) else term_idx
            self.dts_mod_id = data_bin[next_idx:term_32].decode('shift_jis') # -'\0'
            next_idx = term_idx+1
            term_idx = data_bin.index(0x00, next_idx)
            self.dts_clk_ch = data_bin[next_idx:term_idx].decode() # -'\0'
            next_idx = term_idx+1
            self.dts_trg_ch, self.dts_user_clk, = struct.unpack_from('<HI', data_bin, next_idx) # 4bytes
            next_idx += 6
            tmp_params.append(LabcomDataChParam("SignalName",self.signal_name,1))
            tmp_params.append(LabcomDataChParam("DTSsource",self.dts_source,1))
            tmp_params.append(LabcomDataChParam("DTShostID",self.dts_host_id,1))
            tmp_params.append(LabcomDataChParam("DTSmoduleID",self.dts_mod_id,1))
            tmp_params.append(LabcomDataChParam("DTSclockChannel",self.dts_clk_ch,1))
            tmp_params.append(LabcomDataChParam("DTStriggerChannel",self.dts_trg_ch,4))
            tmp_params.append(LabcomDataChParam("DTSuserDefinedClcok",self.dts_user_clk,4))

        self.ch_params = tmp_params
#-----------------------------
# channel data
#-----------------------------
        term_idx = next_idx + self.comp_length
        self.channel_comp_data = data_bin[next_idx:term_idx] #
        next_idx = term_idx
#-----------------------------
# channel parameters (self.module_type=0x0a)
#-----------------------------
        if 0x01 == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.aurora14_pdefs())
            return
        if 0x02 == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.toyo629_pdefs())
            return
        if 0x03 == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.segdcm_pdefs())
            return
        if 0x04 == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.segadc_pdefs())
            return
        if 0x05 == self.module_type :
#           DMOD
            return
        if 0x06 == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.cts308_pdefs())
            return
        if 0x07 == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.cts419_pdefs())
            return
        if 0x08 == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.cts504_pdefs())
            return
        if 0x09 == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.test_pdefs())
            return
        if 0x0b == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.caen_n209_pdefs())
            return
        if 0x0c == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.caen_n470_pdefs())
            return
        if 0x0d == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.cps412_pdefs())
            return
        if 0x0e == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.housin_c012_1_pdefs())
            return
        if 0x0f == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.housin_c012_2_pdefs())
            return
        if 0x10 == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.dts_pdefs())
            return
        if 0x11 == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.cts606b_pdefs())
            return
        if 0x12 == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.rpc330_pdefs())
            return
        if 91 == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.pxi6115_pdefs())
            return
        if 92 == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.pxi6602_pdefs())
            return
        if 93 == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.pxi1409_pdefs())
            return
        if 94 == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.pxi1411_pdefs())
            return
        if 101 == self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.pxi6133_pdefs())
            return
        if 122 <= self.module_type and 125 >= self.module_type :
            self.ch_params += self.mem_image_params( data_bin, next_idx, self.we72xx_pdefs())
            return
        if 0x0a != self.module_type :
            return
        self.params_block_size, self.params_head_size \
            = struct.unpack_from('<2I', data_bin, next_idx) # 8bytes
        self.n_params = int((self.params_head_size-4*2)/(4*4+2))
        param_defines = []
        next_idx += 8
        for ofs in range(0, self.n_params):
            tmp=LabcomDataChParamStruct(data_bin, next_idx)
            param_defines.append(tmp)
            next_idx = tmp.next_offset
        ch_params_part = LabcomDataChParams(param_defines, data_bin, next_idx )
        self.next_offset = ch_params_part.next_offset
        self.ch_params += ch_params_part.params
        self.bin_len = ch_params_part.next_offset - channel_offset
#        print(self.params_block_size,self.params_head_size, self.n_params)
#        for ch_param in self.ch_params:
#            print(ch_param.name, ch_param.val, ch_param.type)

    def mem_image_params(self, data_bin: bytes, chparam_offset: int, param_defs) :
        tmp_params = []
        next_idx = chparam_offset
        for param in param_defs :
            try :
                if 1 == param[2] :
                    term_idx = data_bin.index(0x00, next_idx)
                    val = data_bin[next_idx:term_idx].decode() # -'\0'
                    next_idx = term_idx+1
                else :
                    val, = struct.unpack_from(param[1], data_bin, next_idx)
                    next_idx += struct.calcsize(param[1])
                tmp_params.append(LabcomDataChParam(param[0], val, param[2] ))
            except Exception as e:
                print('Exception: ', param[0])
                print(e)
                break

        return tmp_params
 
    def aurora14_pdefs(self) :
        pdefs = [
        ["Range",            '<f', 5], ["RangeFactor",   '<I', 4],
        ["RangePolarity",      '', 1], ["ClockSpeed",    '<I', 4], 
        ["ExtIntClock",        '', 1], ["Mode",            '', 1], 
        ["ClockOutputControl", '', 1], ["InPolarityStop",  '', 1], 
        ["InPolarityStart",    '', 1], ["InPolarityClock", '', 1], 
        ["PTS",              '<I', 4], ["MemorySize",    '<I', 4] ] 
        if '1' == self.ver_no[1] :
            pdefs += [
            ["BinaryCoding", '',1], ["LastMemoryAddress",'<I',4],
            ["RunStatus",    '',1], ["AddressOverflow",    '',1],
            ["ModeCMDorDAQ", '',1], ["LAM",                '',1] ]
        return pdefs

    def caen_n209_pdefs(self) :
        pdefs = [
        ["CaenetAddress",  '<I', 4], ["ModuleName",   '', 1],
        ["Delay",          '<I', 4], ["Gate",       '<I', 4] ] 
        return pdefs

    def caen_n470_pdefs(self) :
        pdefs = [
        ["CaenetAddress",  '<I', 4], ["ModuleNameAndSoftwareVersion",   '', 1],
        ["OutCal",    '', 1], ["SignalLevel", '', 1],
        ["Alarm",     '', 1], ["Kill",  '', 1], 
        ["VSel",      '', 1], ["ISel",  '', 1], 
        ["V0",      '<i', 4], ["I0",  '<i', 4], 
        ["V1",      '<i', 4], ["I1",  '<i', 4], 
        ["Trip",    '<i', 4], ["RampUp", '<i', 4], 
        ["RampDown",'<i', 4], ["VMon",   '<i', 4], 
        ["IMon",    '<i', 4], ["MaxV",   '<i', 4], 
        ["Polarity",  '', 1] ] 
        return pdefs

    def cps412_pdefs(self) :
        pdefs = [
        ["MemorySize",      '<I', 4], ["DacRange",   '<I', 4],
        ["IntClockSpeed",   '<I', 4], ["SkipSize",   '<I', 4], 
        ["Reference",       '<I', 4], ["UpperLimit", '<I', 4], 
        ["LowerLimit",      '<I', 4], ["Offset",     '<I', 4], 
        ["DAC-OutStartMode",  '', 1],
        ["CoefficientOfUpperLimit", '<f', 5], 
        ["CoefficientOfLowerLimit", '<f', 5],
        ["CoefficientOfOffset",     '<f', 5]]
        if '1' == self.ver_no[1] :
            pdefs += [
            ["LastMemoryAddress", '<I', 4], ["LAM", '', 1] ]
        return pdefs

    def cts308_pdefs(self) :
        pdefs = [
        ["Mode",         '', 1],
        ["NumberOfActiveChannels",     '<I', 4],
        ["NumberOfWordTransferdToRAM", '<I', 4],
        ["Active",       '', 1], 
        ["IsOverflowed", '', 1],
        ["BufferMemoryChannel",  '<I', 4] ]
        return pdefs
	
    def cts419_pdefs(self) :
        pdefs = [
        ["MemorySize",        '<I', 4], ["LAM", '', 1],
        ["LastMemoryAddress", '<I', 4] ]
        return pdefs

    def cts504_pdefs(self) :
        pdefs = [
        ["SoftwareStart", '', 1], ["Interval(uSec)", '<I', 4],
        ["Count",       '<I', 4] ]
        return pdefs

    def cts606b_pdefs(self) :
        pdefs = [["Interval", '<I', 4]]
        return pdefs

    def housin_c012_1_pdefs(self) :
        pdefs = [
        ["Clock",   '', 1], ["Memory", '<I', 4],
        ["Gain",  '<I', 4], ["Delay",  '<I', 4]] 
        if '1' == self.ver_no[1] :
            pdefs += [["BinaryCoding", '', 1], ["LAM", '', 1] ]
        return pdefs

    def housin_c012_2_pdefs(self) :
        pdefs = [
        ["Clock",   '', 1], ["Memory", '<I', 4],
        ["Gain",  '<I', 4], ["Delay",  '<I', 4]] 
        if '1' == self.ver_no[1] :
            pdefs += [["BinaryCoding", '', 1], ["LAM",  '', 1]]
        return pdefs

    def pxi1409_pdefs(self) :
        pdefs = [
        ["DeviceNumber",       '<I', 4], ["ChannelNumberInModule", '<I', 4],
        ["MeasureMode",          '', 1], ["Samples/Ch",    '<I', 4], 
        ["TriggerSource",        '', 1], ["LookupTable",     '', 1], 
        ["SlaveAcquisitionMode", '', 1], ["SignalLevel",     '', 1], 
        ["PCLK_Source",          '', 1], ["CSYNC_Polarity",  '', 1], 
        ["HSYNC_Polarity",       '', 1], ["VSYNC_Polarity",  '', 1], 
        ["PCLK_Polarity",        '', 1], ["StillColorMode",  '', 1], 
        ["FrameTimeOut(ms)",   '<I', 4], ["CameraType",      '', 1], 
        ["Interlace",            '', 1], ["AcquisitionMode", '', 1], 
        ["FirstField",           '', 1], ["AcquisitionField",'', 1], 
        ["AcquisitionWindowLeft", '<I', 4], ["AcquisitionWindowTop",   '<I', 4], 
        ["AcquisitionWindowWidth",'<I', 4], ["AcquisitionWindowHeight",'<I', 4], 
        ["DigitalFilter",        '', 1], ["ScaleFactor",     '', 1], 
        ["BitDepth",           '<I', 4], ["WhiteRef.Level(V)", '<d', 6], 
        ["BlackRef.Level(V)",  '<d', 6], ["ClampStart",    '<I', 4],
        ["ClamStop",           '<I', 4], ["LockSpeed",       '', 1], 
        ["AnalogBandwidth",      '', 1], ["OutStatusSignal", '', 1], 
        ["StatusOfEnd",        '<I', 4], ["SampledFrame",  '<I', 4], 
        ["FrameByteSize",      '<I', 4], ["MissedFrame",   '<I', 4], 
        ["BitsPerPixel",       '<I', 4], ["BytesPerPixel", '<I', 4], 
        ["RegionOfInterestLeft", '<I', 4], ["RegionOfInterestTop",   '<I', 4], 
        ["RegionOfInterestWidth",'<I', 4], ["RegionOfInterestHeight",'<I', 4] ]
        return pdefs

    def pxi1411_pdefs(self) :
        pdefs = [
        ["DeviceNumber",     '<I', 4], ["ChannelNumberInModule", '<I', 4],
        ["MeasureMode",        '', 1], ["Samples/Ch",    '<I', 4], 
        ["TriggerSource",      '', 1], ["LookupTable",     '', 1], 
        ["FrameTimeOut(ms)", '<I', 4], ["InputSelect",     '', 1], 
        ["CameraType",         '', 1], 
        ["Interlace",          '', 1], ["AcquisitionMode", '', 1], 
        ["FirstField",         '', 1], ["AcquisitionField",'', 1], 
        ["AcquisitionWindowLeft", '<I', 4], ["AcquisitionWindowTop",   '<I', 4], 
        ["AcquisitionWindowWidth",'<I', 4], ["AcquisitionWindowHeight",'<I', 4], 
        ["ScaleFactor",        '', 1],
        ["ImageRepresentation",'', 1], ["ChromaFilter",    '', 1],
        ["WhiteRef.Level(V)",'<d', 6], ["BlackRef.Level(V)",'<d', 6], 
        ["LockSpeed",          '', 1], 
        ["Brightness",       '<d', 6], ["Contrast",      '<d', 6], 
        ["Saturation",       '<d', 6], ["Tint",          '<d', 6], 
        ["SetupCorrection",    '', 1], ["SetupCorrectionValue", '<d', 6],
        ["LumaBandwidth",      '', 1], ["LumaComb",        '', 1], 
        ["LumaChromaTrap",     '', 1], ["LumaPeaking",     '', 1], 
        ["ChromaProcessing",   '', 1], ["ChromaBandwidth", '', 1], 
        ["ChromaComb",         '', 1], ["HueOffsetAngle",'<d', 6], 
        ["HSL_CoringLevel",  '<i', 4], ["HueCoringReplace",'<i', 4], 
        ["RGB_CoringLevel",    '', 1], ["RGB_ChromaPhase", '<d', 6], 
        ["RedGain",            '', 1], ["GreenGain",       '<d', 6], 
        ["BlueGain",           '', 1],
        ["StatusOfEnd",      '<I', 4], ["SampledFrame",  '<I', 4], 
        ["FrameByteSize",    '<I', 4], ["MissedFrame",   '<I', 4], 
        ["BitsPerPixel",     '<I', 4], ["BytesPerPixel", '<I', 4], 
        ["RegionOfInterestLeft", '<I', 4], ["RegionOfInterestTop",   '<I', 4], 
        ["RegionOfInterestWidth",'<I', 4], ["RegionOfInterestHeight",'<I', 4] ]
        return pdefs

    def pxi6115_pdefs(self) :
        if '1' == self.ver_no[1] :
            pdefs = [
            ["DeviceNumber",     '<I', 4], ["ChannelNumberInModule",'<I', 4],
            ["MeasureMode",        '', 1], ["TriggerType",  '', 1], 
            ["TriggerSource",      '', 1], ["TriggerEdge",  '', 1],
            ["BufferSizePerCH",  '<I', 4], ["NumberOfSamplesPerCH", '<q', 7], 
            ["PreTriggerSamplesPerCH", '<I', 4], ["SamplingTimeBase", '', 1],
            ["SamplingClock",    '<d', 6], ["ExternalClockSource", '', 1],
            ["SamplingClockEdge",  '', 1], ["SamplingInterval",  '<I', 4], 
            ["ProductType",        '', 1], ["SerialNumber", '', 1],
            ["Status",     '', 1], ["Mode",        '', 1],
            ["Polarity",   '', 1], ["Gain",      '<f', 5],
            ["Range",    '<d', 6], ["RangeHigh", '<d', 6],
            ["RangeLow", '<d', 6], ["Cupling",     '', 1],
            ["Filter",     '', 1], ["FilterValue", '<d', 6], 
            ["PhysicalName", '', 1], ["BinaryCoding",'', 1],
            ["CountOfSampledData",'<q', 7], ["eStatus",        '<i', 4],
            ["ePosition",  '<i', 4], ["OnboardMemorySizePerCH",'<I', 4],
            ["Connect1From", '', 1], ["Connect1To", '', 1],
            ["Connect2From", '', 1], ["Connect2To", '', 1] ]
        else :
            pdefs = [
            ["DeviceNumber",    '<I', 4], ["ChannelNumberInModule",   '<I', 4],
            ["StopCondition",     '', 1], ["TriggerSource",             '', 1], 
            ["NumberOfSamplesPerCH",  '<I', 4], ["SamplingTimeBase",    '', 1],
            ["ExternalSampleTimeBase",'<I', 4], ["ExternalClockSource", '', 1],
            ["SamplingInterval",      '<I', 4], ["Status",  '', 1],
            ["Mode",   '', 1], ["Polarity", '', 1],
            ["Gain", '<f', 5], ["Cupling",  '', 1],
            ["Filter", '', 1], ["CountOfSampledData",'<I', 4] ]
        return pdefs

    def pxi6133_pdefs(self) :
        pdefs = [
        ["DeviceNumber",     '<I', 4], ["ChannelNumberInModule",'<I', 4],
        ["MeasureMode",        '', 1], ["TriggerType",  '', 1], 
        ["TriggerSource",      '', 1], ["TriggerEdge",  '', 1],
        ["BufferSizePerCH",  '<I', 4], ["NumberOfSamplesPerCH", '<q', 7], 
        ["PreTriggerSamplesPerCH",'<I', 4], ["SamplingTimeBase",  '', 1],
        ["SamplingClock",    '<d', 6], ["ExternalClockSource", '', 1],
        ["SamplingClockEdge",  '', 1], ["SamplingInterval",  '<I', 4], 
        ["ProductType",        '', 1], ["SerialNumber", '', 1],
        ["Status",     '', 1], ["Mode",        '', 1],
        ["Polarity",   '', 1], ["Gain",      '<f', 5],
        ["Range",    '<d', 6], ["RangeHigh", '<d', 6],
        ["RangeLow", '<d', 6], ["Cupling",     '', 1],
        ["Filter",     '', 1], ["FilterValue", '<d', 6], 
        ["PhysicalName", '', 1], ["BinaryCoding",'', 1],
        ["CountOfSampledData",'<q', 7], ["eStatus",        '<i', 4],
        ["ePosition",  '<i', 4], ["OnboardMemorySizePerCH",'<I', 4],
        ["Connect1From", '', 1], ["Connect1To", '', 1],
        ["Connect2From", '', 1], ["Connect2To", '', 1] ]
        return pdefs

    def pxi6602_pdefs(self) :
        pdefs = [
        ["DeviceNumber", '<I', 4], ["ChannelNumberInModule",'<I', 4],
        ["MeasureMode",    '', 1], ["triggerSource", '', 1],
        ["Status",         '', 1], ["Mode",          '', 1],
        ["NumberOfSamples", '<I', 4], ["Samples/Sec", '<I', 4], 
        ["SourceSignal",   '', 1], ["SourcePolarity",  '', 1],["SourceFilter",  '', 1],
        ["GateSignal",     '', 1], ["GatePolarity",    '', 1],["GateFilter",    '', 1],
        ["AuxLineSignal",  '', 1], ["AuxLinePolarity", '', 1],["AuxLineFilter", '', 1],
        ["PreScaler",      '', 1], ["Sync. Counting Mode", '', 1],
        ["CounterReached", '', 1], ["StatusOfEnd", '<i', 4],
        ["CounterValue", '<I', 4], ["CountOfSampledData", '<I', 4] ]
        return pdefs

    def rpc330_pdefs(self) :
        pdefs = [
        ["ChannelNumberInModule",'<I', 4],
        ["Gain", '<I', 4], ["Filter", '', 1], ["Bandwidth", '<d', 6],
        ["ErrorCodeOnSetup",  '<i', 4] ]
        return pdefs

    def segadc_pdefs(self) :
        pdefs = [
        ["Gain", '<I', 4], ["Filter", '', 1], ["NumberOfDigitizedData", '<I', 4]]
        if '1' == self.ver_no[1] :
            pdefs += [ ["BinaryCoding", '', 1], ["LAM", '', 1] ]
        return pdefs

    def segdcm_pdefs(self) :
        pdefs = [
        ["SamplingMode", '', 1], ["ControlMode", '', 1],
        ["F1", '<I', 4], ["N1", '<I', 4], ["F2", '<I', 4], ["N2", '<I', 4],
        ["F3", '<I', 4], ["N3", '<I', 4], ["F4", '<I', 4], ["N4", '<I', 4],
        ["NumberOfEvnetTrigger", '<I', 4]]
        if '1' == self.ver_no[1] :
            pdefs += [ ["LAM", '', 1] ]
        return pdefs

    def test_pdefs(self) :
        pdefs = [ ["Param A", '<f', 5], ["Param B", '<I', 4], ["Param C", '', 1] ]
        return pdefs

    def toyo629_pdefs(self) :
        pdefs = [ ["RouteMode", '', 1] ]
        if '1' == self.ver_no[1] :
            pdefs += [
            ["ChannelsPerFrame",   '<I', 4], ["LastFrameCounter", '<I', 4],
            ["lastAddressCounter", '<I', 4], ["LAM", '', 1] ]
        return pdefs

    def we72xx_pdefs(self) :
        if '1' == self.ver_no[1] :
            pdefs = [
            ["StationNumber", '<I', 4], ["SlotNumber", '<I', 4],
            ["ChannelNumberInModule", '<I', 4],
            ["MeasureMode",     '', 1], ["ClockSource",  '', 1],
            ["ClockInterval(uSec)",     '<I', 4],
            ["Ext.ClockInterval(uSec)", '<I', 4],
            ["Samples/Ch",    '<q', 7], ["PreSamples/Ch", '<I', 4],
            ["TriggerSource",   '', 1],
            ["OverlappedAcquisition", '', 1],
            ["HoldOffTime(uSec)", '<I', 4],
            ["Status",   '', 1], ["Mode",        '', 1],
            ["Polarity", '', 1], ["Range(mV)", '<I', 4],
            ["Coupling", '', 1], ["Filter",      '', 1],
            ["CountOfSampledData", '<q', 7],
            ["VResolution",   '<d', 6], ["VOffset", '<d', 6],
            ["BinaryCoding", '', 1] ]
        else :
            pdefs = [
            ["StationNumber", '<I', 4], ["SlotNumber", '<I', 4],
            ["ChannelNumberInModule", '<I', 4],
            ["MeasureMode",     '', 1], ["ClockSource",  '', 1],
            ["ClockInterval(uSec)",     '<I', 4],
            ["Ext.ClockInterval(uSec)", '<I', 4],
            ["Samples/Ch",    '<I', 4], ["PreSamples/Ch", '<I', 4],
            ["TriggerSource",   '', 1],
            ["OverlappedAcquisition", '', 1],
            ["HoldOffTime(uSec)", '<I', 4],
            ["Status",   '', 1], ["Mode",        '', 1],
            ["Polarity", '', 1], ["Range(mV)", '<I', 4],
            ["Coupling", '', 1], ["Filter",      '', 1],
            ["CountOfSampledData", '<I', 4],
            ["VResolution",   '<d', 6], ["VOffset", '<d', 6] ]
        return pdefs

    def dts_pdefs(self) :
        pdefs = [
        ["TimeOfCollected",     '', 1], ["ModuleClearOnSetup", '', 1],
        ["TimerClearOnSetup",   '', 1], ["ManualSetupOnSetup", '', 1],
        ["ModuleResetOnAcquire",'', 1], ["EventOutMode",       '', 1],

        ["BaseRate",          '<I', 4], ["ExternalTrigger",  '', 1], 
        ["ClockSource",         '', 1], ["VMEbusInterrupt",  '', 1],
        ["MoveMode",            '', 1],  
        ["InterruptTrigger",    '', 1], ["InterruptEvent",   '', 1],
        ["InterruptUninhibit",  '', 1], ["InterruptInhibit", '', 1],
        ["InterruptError",      '', 1], ["InterruptClockError", '', 1],
        ["InterruptSetup",      '', 1], ["InterruptStop",    '', 1],
        ["CH1Trigger", '', 1], ["CH2Trigger", '', 1],
        ["CH3Trigger", '', 1], ["CH4Trigger", '', 1],
        ["CH5Trigger", '', 1], ["CH6Trigger", '', 1],
        ["CH6Trigger", '', 1], ["CH8Trigger", '', 1],
        ["InterruptDetail",    '<I', 4], ["Event", '<I', 4],
        ["TimerTriggerChannel",'<I', 4], ["Timer", '<I', 4],
        ["Message",       '<I', 4], ["DelayLinePreset", '<I', 4],
        ["SignalTrigger",   '', 1], ["SignalEvent",       '', 1],
        ["SignalUninhibit", '', 1], ["SignalInhibit",     '', 1],
        ["SignalError",     '', 1], ["SignalClockError",  '', 1],
        ["SignalSetup",     '', 1], ["SignalStop",        '', 1],
        ["InternalDelay", '<I', 4], ["ChannelNumberInModule", '<I', 4],
        ["DvdRange",        '', 1], ["DvdMagnification",'<i', 4],
        ["DvdConnectDiag",  '', 1], ["DelayTime_s",     '<d', 6],
        ["PulseWidth_s",  '<d', 6], ["RepetitionTime_s",'<d', 6],
        ["DelayTime",     '<I', 4], ["PulseWidth",      '<I', 4],
        ["RepetitionTime",'<I', 4], ["RepetitionCount", '<I', 4],
        ["TriggerSelect", '<I', 4], 
        ["ConnectDiag",     '', 1], ["HostName", '', 1] ]
        return pdefs


class LabcomOldDataChannel(LabcomDataCommon):
    def __init__(self, data_bin: bytes, channel_offset: int =0) :
        self.value_len = 16
        self.bin_len,\
        self.channel_number, self.data_type, \
        self.data_length, self.comp_length, \
        self.manage_no, self.version_no\
            = struct.unpack_from('<I2h2I2f', data_bin, channel_offset)
        next_idx = channel_offset+24
        term_idx = data_bin.index(0x00, next_idx)
        self.comp_method = data_bin[next_idx:term_idx].decode() # -'\0'
        next_idx = term_idx+1
        term_idx = data_bin.index(0x00, next_idx)
        self.comp_version = data_bin[next_idx:term_idx].decode() # -'\0'
        next_idx = term_idx+1
        term_idx = data_bin.index(0x00, next_idx)
        self.note = data_bin[next_idx:term_idx].decode('shift_jis') # -'\0'
        self.next_offset = self.bin_len + channel_offset
#        print( self.channel_number, self.data_type, \
#        self.data_length, self.comp_length, \
#        self.manage_no, self.version_no, self.comp_method, self.comp_version, self.note)
        tmp_params = []
        tmp_params.append(LabcomDataChParam("ChannelNumber",self.channel_number,4))
        tmp_params.append(LabcomDataChParam("ManageNumber",self.manage_no,1))
        tmp_params.append(LabcomDataChParam("VersionNumber",self.version_no,1))
        tmp_params.append(LabcomDataChParam("DataType",self.data_type_string(),1))
        if 0 != self.value_len :
            tmp_params.append(LabcomDataChParam("Resolution(bit)",self.value_len,4)) # self.value_len
        tmp_params.append(LabcomDataChParam("DataLength(byte)",self.data_length,4))
        tmp_params.append(LabcomDataChParam("CompLength(byte)",self.comp_length,4))
        tmp_params.append(LabcomDataChParam("CompressionMethod",self.comp_method,1))
        tmp_params.append(LabcomDataChParam("CompressionVersion",self.comp_version,1))
        tmp_params.append(LabcomDataChParam("Comment",self.note,1))
        self.ch_params = tmp_params
#-----------------------------
# channel data
#-----------------------------
        next_idx = term_idx+1
        term_idx = next_idx + self.comp_length
        self.channel_comp_data = data_bin[next_idx:term_idx] #



import argparse
import pathlib

def main(argv):
    if sys.version_info[0] == 2:
        print("please on Python 3\n")
        return(-1)

    parser = argparse.ArgumentParser(description='Utility of LABCOM dat file.',epilog=' Version 1.0.1')
    parser.add_argument("dat_file", type=str,
                    help="LABCOM dat file name")
    parser.add_argument("-S", "--without_shot", action="store_true",
                    help="make the shot parameter file", default=False)
    parser.add_argument("-C", "--without_channel", action="store_true",
                    help="donot make the channel parameter , data file", default=False)
#    parser.add_argument("-u", "--update_oodbms", action="store_true",
#                    help="display update oodbms sql")
    parser.add_argument("-p", '--savepath', type=pathlib.Path, default='.',
                    help="path to save file")
    parser.add_argument("-M", "--without_data_dir", action="store_true",
                    help="donot make data directory( {diagnostics}-{shot}-{subshot} )", default=False)
    parser.add_argument("-v", '--verbose', action="store_true",
                    help="output verbose messages")
    args = parser.parse_args()
    make_sub_dir = not args.without_data_dir
    try:
        fr = open(args.dat_file, 'rb')
    except OSError as e:
            print(e)
    else:
        try:
            fdata = fr.read()
            head = LabcomDataHeader(fdata)
            if head.check_dat_format() :
                ch_ofss = head.channel_offsets(fdata)
                shot = LabcomDataShot(fdata, head.next_offset)
                if 0 < len(ch_ofss) and (not args.without_channel) :
                    save_path = shot.make_channels_dir(args.savepath, make_sub_dir)
                for ch_ofs in ch_ofss:
                    ch=LabcomDataChannel(fdata, ch_ofs)
                    if not args.without_channel :
                        ch.make_channel_file(shot.diag_name, shot.shot_no, shot.sub_shot, save_path)

                shot.set_module_group(ch.module_group)

                if not args.without_shot :
                    if args.without_channel :
                        shot.make_shot_dir(arg.savepath)
                    shot.make_shot_file(args.savepath)

#                if args.update_oodbms :
#                    shot.print_update_oodbms_sql()

            else :
                head = LabcomOldDataHeader(fdata)
                file_info=pathlib.PurePath(args.dat_file).name.split('0')
                ch_ofss = head.channel_offsets(fdata)
                total_data_size = 0
                total_comp_size = 0
                if 0 < len(ch_ofss) and (not args.without_channel) :
                    save_path = head.make_channels_dir(file_info[0], args.savepath, make_sub_dir)
                for ch_ofs in ch_ofss:
                    ch=LabcomOldDataChannel(fdata, ch_ofs)
                    total_data_size = total_data_size + ch.data_length
                    total_comp_size = total_comp_size + ch.comp_length
                    if not args.without_channel :
                        ch.make_channel_file(file_info[0], head.shot_no, head.sub_shot, save_path)
                head.set_total( total_data_size, total_comp_size)

                if not args.without_shot :
                    if args.without_channel :
                        shot.make_shot_dir(args.savepath)
                    head.make_shot_file(file_info[0],args.savepath)
 
#                if args.update_oodbms :
#                    head.set_diag(file_info[0])
#                    head.print_update_oodbms_sql()

        except FileExistsError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)
        except PermissionError as e:
            print(e)
        except Exception as e:
            print('The data format is different or it is not supported.')
            if args.verbose :
               print(e)
        finally:
            fr.close()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))


