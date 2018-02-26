#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Thu Apr 20 21:37:50 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import numbersink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2.5e6
        self.fft1 = fft1 = 128

        ##################################################
        # Blocks
        ##################################################
        self.sig_source = numbersink2.number_sink_f(
        	self.GetWin(),
        	unit='Units',
        	minval=-100,
        	maxval=100,
        	factor=1.0,
        	decimal_places=5,
        	ref_level=0,
        	sample_rate=samp_rate,
        	number_rate=15,
        	average=False,
        	avg_alpha=None,
        	label='sig source',
        	peak_hold=True,
        	show_gauge=True,
        )
        self.Add(self.sig_source.win)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(467.562e6, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(1, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.phase = numbersink2.number_sink_f(
        	self.GetWin(),
        	unit='Units',
        	minval=-100,
        	maxval=100,
        	factor=1.0,
        	decimal_places=10,
        	ref_level=0,
        	sample_rate=samp_rate,
        	number_rate=15,
        	average=False,
        	avg_alpha=None,
        	label='Number Plot',
        	peak_hold=False,
        	show_gauge=True,
        )
        self.Add(self.phase.win)
        self.high_pass_filter_0 = filter.fir_filter_ccf(1, firdes.high_pass(
        	1, samp_rate, 1000, 10000, firdes.WIN_HAMMING, 6.76))
        self.fft_vxx_0_0 = fft.fft_vcc(32, True, (window.blackmanharris(32)), True, 1)
        self.fft_vxx_0 = fft.fft_vcc(128, True, (window.blackmanharris(128)), True, 1)
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, 32)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, fft1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_sub_xx_0 = blocks.sub_ii(1)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 32)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft1)
        self.blocks_skiphead_0_0 = blocks.skiphead(gr.sizeof_gr_complex*1, 9)
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_gr_complex*1, 9)
        self.blocks_keep_one_in_n_0_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, 1)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, 1)
        self.blocks_complex_to_mag_0_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_arg_0_0 = blocks.complex_to_arg(1)
        self.blocks_complex_to_arg_0 = blocks.complex_to_arg(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, 467.563e6, 1, 0)
        self.actual_data = numbersink2.number_sink_f(
        	self.GetWin(),
        	unit='Units',
        	minval=-100,
        	maxval=100,
        	factor=1.0,
        	decimal_places=5,
        	ref_level=0,
        	sample_rate=samp_rate,
        	number_rate=15,
        	average=False,
        	avg_alpha=None,
        	label='actual',
        	peak_hold=True,
        	show_gauge=True,
        )
        self.Add(self.actual_data.win)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_stream_to_vector_0_0, 0))    
        self.connect((self.blocks_complex_to_arg_0, 0), (self.blocks_sub_xx_0, 0))    
        self.connect((self.blocks_complex_to_arg_0_0, 0), (self.blocks_sub_xx_0, 1))    
        self.connect((self.blocks_complex_to_mag_0, 0), (self.actual_data, 0))    
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self.sig_source, 0))    
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_complex_to_arg_0, 0))    
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_complex_to_mag_0, 0))    
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_complex_to_arg_0_0, 0))    
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_complex_to_mag_0_0, 0))    
        self.connect((self.blocks_skiphead_0, 0), (self.blocks_keep_one_in_n_0, 0))    
        self.connect((self.blocks_skiphead_0_0, 0), (self.blocks_keep_one_in_n_0_0, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))    
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.fft_vxx_0_0, 0))    
        self.connect((self.blocks_sub_xx_0, 0), (self.phase, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_skiphead_0, 0))    
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.blocks_skiphead_0_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.blocks_vector_to_stream_0, 0))    
        self.connect((self.fft_vxx_0_0, 0), (self.blocks_vector_to_stream_0_0, 0))    
        self.connect((self.high_pass_filter_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.high_pass_filter_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.high_pass_filter_0.set_taps(firdes.high_pass(1, self.samp_rate, 1000, 10000, firdes.WIN_HAMMING, 6.76))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_fft1(self):
        return self.fft1

    def set_fft1(self, fft1):
        self.fft1 = fft1


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
