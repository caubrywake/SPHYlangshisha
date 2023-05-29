%% Compare one season at Langshisha
% rain vs melt events, soil moisture vs gw level. Pick an event and zoom in
% science questions: is soil moisture the main control on gw level?
% does rain infiltrate to gw?

% First, Build a table with common tme steps
% GW: langshisha top and bottom
% Soil Moisture:Langshihsa Transect and Langshisha Pluvio
% snowdepth langshisha
% Ls plubio
% ls tipping bucket
% Ls ta
close all
clear all

addpath('F:\13_Utrecht\03_data')
savedir = 'F:\13_Utrecht\05_figure\00_dataexploration\langshisha_exploration\'
figdir =  'F:\13_Utrecht\05_figure\00_dataexploration\langshisha_exploration\'
 % GW bottom
T = readtable('G:\13_Utrecht\03_data\data\Groundwater\202111_LangshishaBottom_Groundwater.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
t = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
x = table2array(T(:, 3))*1000./(999.965*9.81)-2.07;
x(x<-1.8)=nan;
LS = timetable (t,x);


% GW  toip
T = readtable('F:\13_Utrecht\03_data\data\Groundwater\202111_LangshishaTop_Groundwater.csv');
Tt = datevec(table2array(T(:,1))); Ttt = datevec(table2array(T(:,2)));
t = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
x = table2array(T(:, 3))*1000./(999.965*9.81)-2.07;
x(x<-5)=nan;
T = timetable(t,x); TT= retime(T, LS.t, 'linear');
LS(:,2)=TT(:,1);

% Soil Moisture Langshisha pluvio (1-2-3)
T = readtable('F:\13_Utrecht\03_data\data\SoilMoisture\201804_LangshishaPluvio_soilmoisture.csv');
Tt = datevec(table2array(T(:,1))); Ttt = datevec(table2array(T(:,2)));
x = table2array(T(:,3:5));
t = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
x(x>0.5)=nan;; x(x<0.0)=nan;
T = timetable(t,x(:,1), x(:,2), x(:,3)); TT= retime(T, LS.t, 'linear');
LS(:,3:5)=TT(:,1:3);

% Soil Moisture Langshisha Transect (1-2-3)
T = readtable('F:\13_Utrecht\03_data\data\SoilMoisture\202111_LangshishaTranssect_soilmoisture.csv');
Tt = datevec(table2array(T(:,1))); Ttt = datevec(table2array(T(:,2)));
x = table2array(T(:,3:5));
t = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
x(x>0.5)=nan;; x(x<0.0)=nan;
T = timetable(t,x(:,1), x(:,2), x(:,3)); TT= retime(T, LS.t, 'linear');
LS(:,6:8)=TT(:,1:3);

% Snow depth langshisha
T = readtable('F:\13_Utrecht\03_data\data\Pluvio\20211206_Pluvio_Langshisha.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
t = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
x = table2array(T(:,9));
% clean it up
x(x>=2.8)= nan; x(x<=1.70)= nan;
T = timetable(t,x);  TT= retime(T, LS.t);
LS(:,9)=TT(:,1);

% Air temperature
T = readtable('F:\13_Utrecht\03_data\data\Pluvio\20211206_Pluvio_Langshisha.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
t = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
x = table2array(T(:,6));
T = timetable(t,x);  TT= retime(T, LS.t);
LS(:,10)=TT(:,1);

% Pluvio
T = readtable('F:\13_Utrecht\03_data\data\Pluvio\20211206_Pluvio_Langshisha.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
t = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
x = table2array(T(:,3));
T = timetable(t,x);  TT= retime(T, LS.t);
LS(:,11)=TT(:,1);

% Tipping bucket
T = readtable('G:\13_Utrecht\03_data\data\TippingBuckets\20211206_TB_LangshishaBC_10271177_data.csv');
Tt = datevec(table2array(T(:,1)));Ttt = datevec(table2array(T(:,2)));
t = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
x= ones(length(t),1)*0.2;% as one tip is 0.2 mm
T = timetable(t, x); 
TT = retime(T, 'daily', 'sum');
LS(:,12)=TT(:,1);
% export as csv
writetimetable (TT, 'D:\UU\processed_files\timeseries\Precip_LStippingbucket.csv')
% Columns:  
Varname = {'GWbottom';'GWtop';'SMtransect_1';'SMtransect_2';'SMtransect_3';'SMpluvio_1';'SMpluvio_2';'SMpluvio_3';'SnowDepth';'AirT';'Pluvio';'TippingBucket'};
LS.Properties.VariableNames=Varname;
clear t T Tt TT Ttt Varname x

%% Now I can start to look into variables
a = x(:,1);
a(a<-1.64)=nan;
x(:,1)=a;
% I think it should de daily values
LS2= LS;
LSd = retime(LS, 'daily', 'mean');
LSd2 = retime(LS2, 'daily', 'sum');

t = LSd.t;
x = table2array(LSd);
x2 =  table2array(LSd2);
x(:, 11:12)=x2(:,11:12);
clear x2 LS2 LSd2

a = x(:,11);
a(a>60)=nan;
x(:,11)=a;

yyaxis right
plot(t, x(:,1))
yyaxis left
plot(t, x(:,3:5))

%  GW and precip
figure;
yyaxis right
plot(t, x(:,11)); hold on
plot(t, x(:,12))
ylabel('Pluvio Precip (mm)')
yyaxis left
plot(t, x(:,2)); hold on
plot(t, x(:,1))
ylabel('GW Top, distance to water (m)')

corrcoef(x(:,11),x(:,1), 'rows', 'pairwise')
scatter(x(:,11), x(:,1))

% GW and snowpack
figure;
yyaxis right
plot(t, -x(:,9)+2.697);
ylabel('Snowdepth (m)')
yyaxis left
plot(t, x(:,2)); hold on
plot(t, x(:,1))
ylabel('GW Top, distance to water (m)')
filename = 'Precip_monthly_KyLsMm'
saveas (gcf,strcat(figdir, filename), 'png')
saveas (gcf,strcat(figdir, filename), 'pdf')
savefig (gcf,strcat(figdir, filename))


% snowpack and rain
figure;
yyaxis right
plot(t, -x(:,9)+2.697);
ylabel('Snowdepth (m)')
yyaxis left
plot(t, x(:,11)); hold on
plot(t, x(:,12))
ylabel('Precip (mm)')
legend('pluvio','tipping bucket')

% rain and soil
% moisture
figure;
yyaxis right
plot(t, x(:, 3:5));
ylabel('Soil Moisture (m3/m3)')
yyaxis left
plot(t, x(:,12)); 
ylabel('Rainfall (mm)')

% soil
% moisture and snow
close all

figure;
yyaxis right
h1 = plot(t, -x(:,9)+2.697); hold on
h2 = plot(t, x(:,1)+1.5, '-k')
ylabel('GW, Snowdepth (m)')
yyaxis left
h3 = plot(t, x(:, [3,5]));
ylabel('Soil Moisture (m3/m3)')
legend ([h1(1) h2(1) h3(1), h3(2)],'snowdepth', 'gw bottom+1.5', 'soil moisture 47cm','soil moisture 12 cm','location', 'best') 

% at langshishsa, snowmelt recharge soil moisture for sure. the timing of
% the fist increase is exaclty the same - or it when the soil thaws? 
filename = 'LS_SoilMoisture_Snowdepth_GW'
saveas (gcf,strcat(figdir, filename), 'png')
saveas (gcf,strcat(figdir, filename), 'pdf')
savefig (gcf,strcat(figdir, filename))


% Soil moisture and precip