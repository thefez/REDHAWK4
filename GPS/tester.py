from ossie.utils import sb
gps = sb.launch('BU353S4.spd.xml')
gps.start()

gps.ports[0].ref._get_gps_time_pos()
gps.ports[0].ref._get_gps_info()
