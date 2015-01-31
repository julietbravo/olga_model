#
# Copyright (c) 2013-2014 Bart van Stratum (bart@vanstratum.com)
# 
# This file is part of OLGA.
# 
# OLGA is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# OLGA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with OLGA.  If not, see <http://www.gnu.org/licenses/>.
#

import gc
import numpy as np
import pylab as pl
import sys

from readwrf import *
from colormaps import *
from tools import *
from skewtlogp import *
from readsounding import *

## Function to create maps
def create_sounding(olga,wrfout,dom,times):
    for name, lon, lat in zip(olga.soundLoc[dom].shortName, olga.soundLoc[dom].lon, olga.soundLoc[dom].lat):
	d = readwrf_loc(olga,wrfout,lon,lat,times[0],times[-1])
        sset = skewt_input()

        for t in times:
            stype = 0
            sset.stype  = stype
            sset.hgt    = d.hgt[t]
            sset.T      = d.T[t,:] 
            sset.Td     = d.Td[t,:]
            sset.p      = d.p[t,:] 
            sset.z      = d.zf[t,:]
            sset.u      = d.u[t,:]
            sset.v      = d.v[t,:]
            sset.name   = name
            sset.time   = d.datetime[t]

            # Idealized parcel settings
            sset.parcel = True
            sset.ps     = d.ps[t]
            sset.Ts     = d.T[t,0]#d.T2[t]
            sset.rs     = d.q2[t]

            # Add data from TEMF updrafts
            sset.Tu     = d.Tu[t,:] 
            sset.Tdu    = d.Tdu[t,:] 
            sset.cfru   = d.c3dtemf[t,:] 
            sset.qlu    = d.qltemf[t,:]
            sset.lclu   = d.lcl[t]

            # If time == 00 UTC or 12 UTC, try to get reference sounding for validation (only useful for historical runs)
            sset.Tm     = np.array([])
            sset.Tdm    = np.array([])
            sset.pm     = np.array([])
            #if((d.time[t]/3600.)%12 == 0):
            #    t = 0 if((d.time[t]/3600.) % 24 == 0) else 12
            #    tmp = readsounding(int(name), int(d.year[t]), int(d.month[t]) ,int(d.day[t]), t)
            #    if(tmp.success):
            #        sset.Tm   = tmp.T
            #        sset.Tdm  = tmp.Td
            #        sset.pm   = tmp.p * 100.

            fig         = skewtlogp(olga,sset)
            xtime       = d.time[t] / 3600.
            hour        = int(np.floor(xtime))
            minute      = int((xtime - hour) * 60.)
            tmp         = str(hour).zfill(4) + str(minute).zfill(2)

            # Save figure
            nameo = '%s%04i%02i%02i_t%02iz/sound_%s_%02i_%s.png'%(olga.figRoot, olga.year, olga.month, olga.day, olga.cycle, name, dom+1, tmp)
            pl.savefig(nameo)

            # Cleanup!
            fig.clf()
            pl.close()
            gc.collect()

