function [ doa ] = node_algo( sig_arrival, tx_signal,t,f )
%This function will take into input the signal arival times of each
%antenna in the array of the node, and the transmitter signal
%then by comparing tx signal to a created reference signal, find the
%phase shift at each antenna and then calculate the direction of the
%transmitter
ref_sig = sin(2*pi*f*t);

sw_freq = 500; %switching freq of multiplexer
sw_period = 1/sw_freq;
ant_active = sw_period/4;
first_t =[];

for d=1:4
    
    first_contact =mod(sig_arrival(d),1/f);
    first_t_whole = find(first_contact<t);
    first_t = [first_t, first_t_whole(1)];
    
    
end


test_fft = [];
test_fft = [test_fft, 180*tx_signal(first_t(1))/pi];
ant1_sig = [tx_signal(first_t(1):end),tx_signal(1:first_t(1)-1)];
phase_shift1 = acos(dot(ref_sig,ant1_sig)./(norm(ref_sig)*norm(ant1_sig)));



test_fft = [test_fft, 180*tx_signal(first_t(2))/pi];
ant2_sig = [tx_signal(first_t(2):end),tx_signal(1:first_t(2)-1)];
%phase_shift2 = acos(dot(ref_sig,ant2_sig)./(norm(ref_sig)*norm(ant2_sig)));
phase_shift2 = acos(dot(ant1_sig,ant2_sig)./(norm(ant1_sig)*norm(ant2_sig)));


test_fft = [test_fft,180*tx_signal(first_t(3))/pi];
ant3_sig = [tx_signal(first_t(3):end),tx_signal(1:first_t(3)-1)];
%phase_shift3 = acos(dot(ref_sig,ant3_sig)./(norm(ref_sig)*norm(ant3_sig)));
phase_shift3 = acos(dot(ant2_sig,ant3_sig)./(norm(ant2_sig)*norm(ant3_sig)));


test_fft = [test_fft, 180*tx_signal(first_t(4))/pi];
ant4_sig = [tx_signal(first_t(4):end),tx_signal(1:first_t(4)-1)];
%phase_shift4 = acos(dot(ref_sig,ant4_sig)./(norm(ref_sig)*norm(ant4_sig)));
phase_shift4 = acos(dot(ant3_sig,ant4_sig)./(norm(ant3_sig)*norm(ant4_sig)));

doa = [phase_shift1,phase_shift2,phase_shift3,phase_shift4];
doa = 180*doa/pi;

'FFT test'
test_fft = fft(test_fft);
180*angle(test_fft(2))/pi
mod(180*sum(fft(test_fft))/pi,360);

diff_L = 0;
val = 1;
last_L =0;
for d=1:4
    if d == 4
        e = 1;
    else
        e = d+1;
    end
    if abs(doa(d)-doa(e)) >diff_L && doa(d)-doa(e)>0
        diff_L = abs(doa(d)-doa(e));
        val = 1;
        last_L = d;
    elseif abs(doa(d)-doa(e)) >diff_L && doa(d)-doa(e)<0
        diff_L = abs(doa(d)-doa(e));
        val = -1;
        last_L = d;
    end
        
end

diff_L = diff_L*val;

diff_S = 1000000;
val = 1;
last_S = 0;
for d=1:4
    if d == 4
        e = 1;
    else
        e = d+1;
    end
    if abs(doa(d)-doa(e)) <diff_S && doa(d)-doa(e)>0
        diff_S = abs(doa(d)-doa(e));
        val = 1;
        last_S = d;
    elseif abs(doa(d)-doa(e)) <diff_S && doa(d)-doa(e)<0
        diff_S = abs(doa(d)-doa(e));
        val = -1;
        last_S = d;
    end
        
end

diff_L;
last_L;
diff_S = diff_S*val;
last_S;


end

