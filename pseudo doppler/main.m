% Orion Boylston
% Pseudo Doppler sim and algorithm
%XE402

%wave properties
f = 467.5625e6;
sw_freq = 500; %switching freq of multiplexer
wave_spd = 300000;
sw_freq = 500; %switching freq of multiplexer
sw_period = 1/sw_freq;
ant_active = sw_period/4;
%center point for all nodes
x_nodes = [666,666,333,333];
y_nodes = [666,333,333,666];
%find quarder wavelength
v = 300;
lambda = v/(f/1e6);
lambda_quarter = lambda/2;
%create x/y coordinates for antenna array
%node 1
x_node1 = [x_nodes(1)+lambda_quarter/2,
    x_nodes(1)+lambda_quarter/2,
    x_nodes(1)-lambda_quarter/2,
    x_nodes(1)-lambda_quarter/2];
y_node1 = [y_nodes(1)+lambda_quarter/2,
    y_nodes(1)-lambda_quarter/2,
    y_nodes(1)-lambda_quarter/2,
    y_nodes(1)+lambda_quarter/2];

%node 2
x_node2 = [x_nodes(2)+lambda_quarter/2,
    x_nodes(2)+lambda_quarter/2,
    x_nodes(2)-lambda_quarter/2,
    x_nodes(2)-lambda_quarter/2];
y_node2 = [y_nodes(2)+lambda_quarter/2,
    y_nodes(2)-lambda_quarter/2,
    y_nodes(2)-lambda_quarter/2,
    y_nodes(2)+lambda_quarter/2];

%node 3
x_node3 = [x_nodes(3)+lambda_quarter/2,
    x_nodes(3)+lambda_quarter/2,
    x_nodes(3)-lambda_quarter/2,
    x_nodes(3)-lambda_quarter/2];
y_node3 = [y_nodes(3)+lambda_quarter/2,
    y_nodes(3)-lambda_quarter/2,
    y_nodes(3)-lambda_quarter/2,
    y_nodes(3)+lambda_quarter/2];
%node 4
x_node4 = [x_nodes(4)+ lambda_quarter/2,
    x_nodes(4)+lambda_quarter/2,
    x_nodes(4)-lambda_quarter/2,
    x_nodes(4)-lambda_quarter/2];
y_node4 = [y_nodes(4)+lambda_quarter/2,
    y_nodes(4)-lambda_quarter/2,
    y_nodes(4)-lambda_quarter/2,
    y_nodes(4)+lambda_quarter/2];

%create transmitter in random location and plot
x_transmitter = rand*1000;
y_transmitter = rand*1000;

hold all
scatter(x_transmitter,y_transmitter)
scatter(x_node1, y_node1)
scatter(x_node2, y_node2)
scatter(x_node3, y_node3)
scatter(x_node4, y_node4)

%figure     
tot_time = 1000/wave_spd; %longest possible dist travelled/speed of light
t = [0:1e-15:1/f];
A = 1;
trans_sine = sin(2*pi*f*t);
%plot(t,trans_sine)

% nodes


%node 1 calculations 
arrival_time_n1 = [] ;

for c=1:4
     dist = pythag(x_node1(c)-x_transmitter,y_node1(c)-y_transmitter);
     arrival_time_n1 = [arrival_time_n1, dist/wave_spd+ant_active*c];
     
end
doa_1 = node_algo(arrival_time_n1,trans_sine,t,f);

%node 2 calculations 
arrival_time_n2 = [] ;

for c=1:4
     dist = pythag(x_node2(c)-x_transmitter,y_node2(c)-y_transmitter);
     arrival_time_n2 = [arrival_time_n2, dist/wave_spd+ant_active*c];
     
end
doa_2 = node_algo(arrival_time_n2,trans_sine,t,f);

%node 3 calculations 
arrival_time_n3 = [] ;

for c=1:4
     dist = pythag(x_node3(c)-x_transmitter,y_node3(c)-y_transmitter);
     arrival_time_n3 = [arrival_time_n3, dist/wave_spd+ant_active*c];
     
end
doa_3 = node_algo(arrival_time_n3,trans_sine,t,f);

%node 4 calculations 
arrival_time_n4 = [] ;

for c=1:4
     dist = pythag(x_node4(c)-x_transmitter,y_node4(c)-y_transmitter);
     arrival_time_n4 = [arrival_time_n4, dist/wave_spd+ant_active*c];
     
end
doa_4 = node_algo(arrival_time_n4,trans_sine,t,f);


for c=1:4
    line([x_nodes(c),x_transmitter],[y_nodes(c),y_transmitter],'LineWidth',1)
end




hold off
drawnow