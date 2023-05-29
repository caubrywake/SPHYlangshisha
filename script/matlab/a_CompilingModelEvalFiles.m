%% Creating clean model evaluation files
% Creating streamflow, soil moisture, gw and snow files at daily time
% steps, 

clear all
close all

addpath('F:\13_Utrecht\03_data')
savedir = 'F:\13_Utrecht\05_figure\00_dataexploration\'
figdir =  'F:\13_Utrecht\05_figure\00_dataexploration\'

%% import spkhy simulatio time
%  Create time array basedon start and end time in config file
dir = 'C:\SPHY3\'% location of config file
fn = 'sphy_config_walter.cfg'% name of config file
opts = detectImportOptions(strcat(dir,fn), 'FileType','text');
x = readtable(strcat(dir,fn), opts);
x = string(table2array(x(:,1)));

% find the lines of the text file that matche the keyword strings and
keyword = {'startyear','startmonth','startday','endyear','endmonth','endday'};
for ii = 1:length(keyword)
for i = 1:length(x)
    a = x(i, :);
    k = strfind(a,keyword(ii));
   if ~isempty(k)
      timevalues(1, ii) = str2double(regexp(a,'\d*','Match'));
   end
end
end 
starttime = datetime(timevalues(1:3));endtime = datetime(timevalues(4:6));
t = datetime(starttime:caldays(1):endtime);t=t';

clear keyword x timevalues a k i ii timevalues starttime endtime ots fn dir 


%% Streamflow
% kyanjing
T = readtable('F:\13_Utrecht\03_data\data\Discharge\Kyangjin\Kyanjing_Q_20132019.csv');
Tt = datevec(table2array(T(:,2)));
Ttt = datevec(table2array(T(:,3)));
v =  str2double(table2array(T(:,4)));
x = timetable (datetime([Tt(:,1:3) Ttt(:, 4:6)]), v);

xx = retime(x, 'daily', 'mean'); % retime to dialy averages
xxx = retime(xx, t, 'fillwithmissing'); % retime to the SPHY timeframe
Streamflow = timetable(t, xxx.v);
Streamflow.Properties.VariableNames = {'Kyanjing'};
plot(Streamflow.t, Streamflow.Kyanjing);

% Langshihsa 2013
T = readtable('F:\13_Utrecht\03_data\data\Discharge\Langshisha\Langshisha_Q_20132016.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
v =  str2double(table2array(T(:,3)));
x = timetable (datetime([Tt(:,1:3) Ttt(:, 4:6)]), v);
xx = retime(x, 'daily', 'mean'); % retime to dialy averages
xxx = retime(xx, t, 'fillwithmissing'); % retime to the SPHY timeframe
Streamflow.Langshisha2013 = xxx.v;
plot(Streamflow.t, Streamflow.Langshisha2013);

% Langshihsa 2017
T = readtable('F:\13_Utrecht\03_data\data\Discharge\Langshisha\Langshisha_Q_20172018.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
v =  table2array(T(:,3));
x = timetable (datetime([Tt(:,1:3) Ttt(:, 4:6)]), v);
xx = retime(x, 'daily', 'mean'); % retime to dialy averages
xxx = retime(xx, t, 'fillwithmissing'); % retime to the SPHY timeframe
Streamflow.Langshisha2017 = xxx.v;
plot(Streamflow.t, Streamflow.Langshisha2017);

% Lirung
T = readtable('F:\13_Utrecht\03_data\data\Discharge\Lirung\Lirung_Q_all.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
v =  str2double(table2array(T(:,3)));
x = timetable (datetime([Tt(:,1:3) Ttt(:, 4:6)]), v);
xx = retime(x, 'daily', 'mean'); % retime to dialy averages
xxx = retime(xx, t, 'fillwithmissing'); % retime to the SPHY timeframe
Streamflow.Lirung = xxx.v;
plot(Streamflow.t, Streamflow.Lirung);

% plot together
figure
plot(Streamflow.t, Streamflow.Kyanjing); hold on
plot(Streamflow.t, Streamflow.Langshisha2013);
plot(Streamflow.t, Streamflow.Langshisha2017);
plot(Streamflow.t, Streamflow.Lirung);
legend ('Kyanjing','Langshihsha','Langshisha','Lirung')
ylabel ('Streamflow (m^3 s^{-1})')

% export table as csv
dir = 'F:\13_Utrecht\02_SPHY\analysis\run_20002019\evaldata\'
fn = 'StreamflowDailyKyLs13Ls17Li'
writetimetable (Streamflow, strcat(dir,fn, '.csv'));

%% Soil Moisture
% Langshisha pluvio
T = readtable('F:\13_Utrecht\03_data\data\SoilMoisture\201804_LangshishaPluvio_soilmoisture.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
soilmoisture_pluvio_ls = table2array(T(:,3:5));
time_pluviosoilmoisture_ls = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
soilmoisture_pluvio_ls(soilmoisture_pluvio_ls>0.5)=nan;
soilmoisture_pluvio_ls(soilmoisture_pluvio_ls<0.0)=nan;

v =  str2double(table2array(T(:,3)));
x = timetable (datetime([Tt(:,1:3) Ttt(:, 4:6)]), v);
xx = retime(x, 'daily', 'mean'); % retime to dialy averages
xxx = retime(xx, t, 'fillwithmissing'); % retime to the SPHY timeframe
Streamflow.Lirung = xxx.v;


% Langshisha Transect
T = readtable('F:\13_Utrecht\03_data\data\SoilMoisture\202111_LangshishaTranssect_soilmoisture.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
soilmoisture_lstransect = table2array(T(:,3:5));
time_soilmoisture_lstransect = datetime([Tt(:,1:3) Ttt(:, 4:6)]);

soilmoisture_lstransect(soilmoisture_lstransect<0.0)=nan;


% Langshisha BC
T = readtable('F:\13_Utrecht\03_data\data\SoilMoisture\20200210_LangshishaBC_soilmoisture.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
soilmoisture_lsbc = table2array(T(:,3:5));
time_soilmoisture_lsbc = datetime([Tt(:,1:3) Ttt(:, 4:6)]);

soilmoisture_lsbc(soilmoisture_lsbc<0.0)=nan;


% Ganja La
T = readtable('F:\13_Utrecht\03_data\data\SoilMoisture\202111_GanjaLa_soilmoisture.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
soilmoisture_gl = table2array(T(:,3:5));
time_soilmoisture_gl = datetime([Tt(:,1:3) Ttt(:, 4:6)]);

soilmoisture_gl(soilmoisture_gl<0.0)=nan;


% Langtang
T = readtable('F:\13_Utrecht\03_data\data\SoilMoisture\202111_Langtang_soilmoisture.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
soilmoisture_lg = table2array(T(:,3:5));
time_soilmoisture_lg = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
soilmoisture_lg(soilmoisture_lg<0.0)=nan;

% Tangshyap
T = readtable('F:\13_Utrecht\03_data\data\SoilMoisture\202111_Tangshyap_soilmoisture.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
soilmoisture_ts = table2array(T(:,3:5));
time_soilmoisture_ts = datetime([Tt(:,1:3) Ttt(:, 4:6)]);


% tserkoRi
T = readtable('F:\13_Utrecht\03_data\data\SoilMoisture\20200210_TserkoRi_soilmoisture.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
soilmoisture_tr = table2array(T(:,3:5));
time_soilmoisture_tr = datetime([Tt(:,1:3) Ttt(:, 4:6)]);

