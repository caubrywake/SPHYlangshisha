%% Exploring variables at Langshisha
clear all
close all

addpath('F:\13_Utrecht\03_data')
savedir = 'F:\13_Utrecht\05_figure\00_dataexploration\'
figdir =  'F:\13_Utrecht\05_figure\00_dataexploration\'


% Temperature
% Langshisha and Kyanjing temperature regime
T = readtable('F:\13_Utrecht\03_data\data\AWS\Kyangjin_ICIMOD.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
time_kyanjing = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
ta_kyanjing = table2array(T(:,6));
aws_kyanjing = T;
% monthly
TT = timetable(time_kyanjing,ta_kyanjing); TT = retime(TT, 'monthly', 'mean');
time_kyanjing_mth = TT.time_kyanjing;
ta_kyanjing_mth = table2array(TT);

% At langshisha
T = readtable('F:\13_Utrecht\03_data\data\Pluvio\20211206_Pluvio_Langshisha.csv');
pluvio_ls = T;
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
time_pluvio_ls = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
ta_pluvio_ls = table2array(T(:,6));
% monthly
TT = timetable(time_pluvio_ls,ta_pluvio_ls); TT = retime(TT, 'monthly', 'mean');
time_pl_ls_mth = TT.time_pluvio_ls;
ta_pl_ls_mth = table2array(TT);

% At Ganga la
T = readtable('F:\13_Utrecht\03_data\data\Pluvio\Pluvio_GanjaLa.csv');
pluvio_gl = T;
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
time_pluvio_gl = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
ta_pluvio_gl = table2array(T(:,5));
% monthly
TT = timetable(time_pluvio_gl,ta_pluvio_gl); TT = retime(TT, 'monthly', 'mean');
time_pl_gl_mth = TT.time_pluvio_gl;
ta_pl_gl_mth = table2array(TT);

% At Yala
T = readtable('F:\13_Utrecht\03_data\data\Pluvio\Pluvio_Yala.csv');
pluvio_ya = T;
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
time_pluvio_ya = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
ta_pluvio_ya = table2array(T(:,5));
% monthly
TT = timetable(time_pluvio_ya,ta_pluvio_ya); TT = retime(TT, 'monthly', 'mean');
time_pl_ya_mth = TT.time_pluvio_ya;
ta_pl_ya_mth = table2array(TT);

% At Morimoto
T = readtable('F:\13_Utrecht\03_data\data\Pluvio\20211206_Pluvio_Morimoto.csv');
pluvio_mm = T;
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
time_pluvio_mm = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
ta_pluvio_mm = table2array(T(:,6));
% monthly
TT = timetable(time_pluvio_mm,ta_pluvio_mm); TT = retime(TT, 'monthly', 'mean');
time_pl_mm_mth = TT.time_pluvio_mm;
ta_pl_mm_mth = table2array(TT);

% plot together
figure
plot(time_pl_ls_mth, ta_pl_ls_mth,' -xr'); hold on
plot(time_kyanjing_mth, ta_kyanjing_mth, '-xb')
plot(time_pl_gl_mth, ta_pl_gl_mth, '-xk')
plot(time_pl_ya_mth, ta_pl_ya_mth, '-xm')
plot(time_pl_mm_mth, ta_pl_mm_mth, '-xc')

legend ('langshisha (4452m)', 'kyanjing (3862m)', 'ganjala (4361m)', ...
    'yala (4831m)', 'morimoto (4919 m)', 'location', 'southeast');
ylabel('Ta (C)')
grid on
xlim([time_kyanjing_mth(1) time_kyanjing_mth(end)])

filename = 'Ta_monthly_pluviostations'
saveas (gcf,strcat(figdir, filename), 'png')
saveas (gcf,strcat(figdir, filename), 'pdf')
savefig (gcf,strcat(figdir, filename))

% January real cold, july august warmest. storng seasonal cycle. At
% Langhsihsa, above 0 between March and april (ish)

%% Monthly Precipitation Regime
% langshisha
var = pluvio_ls;
time = time_pluvio_ls; 
TT = timetable(time, table2array(var(:,3))); TT = retime(TT, 'monthly', 'sum'); var_mth = table2array(TT); time_mth = TT.time; 
time_pl_ls_mth = time_mth;
precip_pl_ls_mth = var_mth; 

% kyanjing
var = aws_kyanjing;
time = time_kyanjing; 
TT = timetable(time, table2array(var(:,4))); TT = retime(TT, 'monthly', 'sum'); var_mth = table2array(TT); time_mth = TT.time; 
time_ky_mth = time_mth;
precip_ky_mth = var_mth; 

% ganjala
var = pluvio_gl;
time = time_pluvio_gl; 
TT = timetable(time, table2array(var(:,3))); TT = retime(TT, 'monthly', 'sum'); var_mth = table2array(TT); time_mth = TT.time; 
time_pl_gl_mth = time_mth;
precip_pl_gl_mth = var_mth; 

% morimoto
var = pluvio_mm;
time = time_pluvio_mm; 
TT = timetable(time, table2array(var(:,3))); TT = retime(TT, 'monthly', 'sum'); var_mth = table2array(TT); time_mth = TT.time; 
time_pl_mm_mth = time_mth;
precip_pl_mm_mth = var_mth; 

% yala
var = pluvio_ya;
time = time_pluvio_ya; 
TT = timetable(time, table2array(var(:,3))); TT = retime(TT, 'monthly', 'sum'); var_mth = table2array(TT); time_mth = TT.time; 
time_pl_ya_mth = time_mth;
precip_pl_ya_mth = var_mth; 

% Put all in one timestep (of kyanjing)
pluvio_precip  = timetable(time_ky_mth , precip_ky_mth);

TT = timetable(time_pl_ls_mth , precip_pl_ls_mth); TT = retime(TT, time_ky_mth, 'fillwithmissing'); 
pluvio_precip(:, 2)= TT(:,1);
TT = timetable(time_pl_gl_mth , precip_pl_gl_mth); TT = retime(TT, time_ky_mth, 'fillwithmissing'); 
pluvio_precip(:, 3)= TT(:,1);
TT = timetable(time_pl_mm_mth , precip_pl_mm_mth); TT = retime(TT, time_ky_mth, 'fillwithmissing'); 
pluvio_precip(:, 4)= TT(:,1);
TT = timetable(time_pl_ya_mth , precip_pl_ya_mth); TT = retime(TT, time_ky_mth, 'fillwithmissing'); 
pluvio_precip(:, 5)= TT(:,1);
time_pluvio_precip = pluvio_precip.time_ky_mth;
pluvio_precip = table2array(pluvio_precip);
figure
bar(time_pluvio_precip,pluvio_precip)
ylim([0 1000])
legend ('Kyanjing','Langshisha','Ganja La','Morimoto','Yala')
ylim([0 300])

% Compare only Kyanjing, langshisha and morimoto
pluvio_precip  = timetable(time_ky_mth , precip_ky_mth);
TT = timetable(time_pl_ls_mth , precip_pl_ls_mth); TT = retime(TT, time_ky_mth, 'fillwithmissing'); 
pluvio_precip(:, 2)= TT(:,1);
TT = timetable(time_pl_mm_mth , precip_pl_mm_mth); TT = retime(TT, time_ky_mth, 'fillwithmissing'); 
pluvio_precip(:, 3)= TT(:,1);
time_pluvio_precip = pluvio_precip.time_ky_mth;
pluvio_precip = table2array(pluvio_precip);
figure
bar(time_pluvio_precip,pluvio_precip)
ylim([0 1000])
legend ('Kyanjing','Langshisha','Morimoto')
ylim([0 300])
xlim ([datetime('01-jan-2018') datetime('01-Jan-2021')])
ylabel ('Monthly Precip Pluvio (mm)');

filename = 'Precip_monthly_KyLsMm'
saveas (gcf,strcat(figdir, filename), 'png')
saveas (gcf,strcat(figdir, filename), 'pdf')
savefig (gcf,strcat(figdir, filename))


%% snow depth
% langshisha
sd_pluvio_ls = table2array(pluvio_ls(:,9));
figure
plot(time_pluvio_ls, sd_pluvio_ls); hold on
% clean it up
sd_pluvio_ls(sd_pluvio_ls>=2.8)= nan;
sd_pluvio_ls(sd_pluvio_ls<=1.70)= nan;
plot(time_pluvio_ls, sd_pluvio_ls);

% ganja la
sd_pluvio_gl = table2array(pluvio_gl(:,6));
figure
plot(time_pluvio_gl, sd_pluvio_gl); % Not a good record

% morimoto
sd_pluvio_mm = table2array(pluvio_mm(:,7));
figure
plot(time_pluvio_mm, sd_pluvio_mm); % Not a good record
% clean it up
sd_pluvio_mm(sd_pluvio_mm>=2.7)= nan;
sd_pluvio_mm(sd_pluvio_mm<=2.1)= nan;
plot(time_pluvio_mm, sd_pluvio_mm);

close all
figure
plot(time_pluvio_mm, -sd_pluvio_mm+2.64);
hold on
plot(time_pluvio_ls, -sd_pluvio_ls+2.64);

xlim ([datetime('01-jan-2019') datetime('01-Jul-2020')])
ylabel ('Snow depth (SR50) (m)');
legend ('Morimoto','Langshisha');
filename = 'SnowDepth_20192020_Langshisha_Morimoto'
saveas (gcf,strcat(figdir, filename), 'png')
saveas (gcf,strcat(figdir, filename), 'pdf')
savefig (gcf,strcat(figdir, filename))

% yala
sd_pluvio_ya = table2array(pluvio_ya(:,6));
% shift second half
a = find(time_pluvio_ya=='30-Jun-2013')
sh = 2.593 - 2.225;
sd_pluvio_ya(a:end)= sd_pluvio_ya(a:end)+sh;
% clean it up
sd_pluvio_ya(sd_pluvio_ya>=2.63)= nan;
plot(time_pluvio_ya, -sd_pluvio_ya+2.64);
xlim ([datetime('01-jan-2013') datetime('01-Jul-2014')])
ylim([0 1.4])
ylabel ('Snow depth (SR50) (m)');
legend ('Yala');
filename = 'SnowDepth_20132014_Yala'
saveas (gcf,strcat(figdir, filename), 'png')
saveas (gcf,strcat(figdir, filename), 'pdf')
savefig (gcf,strcat(figdir, filename))

figure
plot(time_pluvio_ya, sd_pluvio_ya); % Not a good record

sd_pluvio_mm(sd_pluvio_mm<=2.1)= nan;

close all
figure
plot(time_pluvio_mm, -sd_pluvio_mm+2.64);
hold on
plot(time_pluvio_ls, -sd_pluvio_ls+2.64);

% snow on the ground between late december and mid april, but shallow
% snowpack ~ 1m thick (is it wind or just very small snowfall?

% at kyanjing
sd_kyanjing = str2double(table2array(aws_kyanjing(:,20)));
plot(time_kyanjing, -sd_kyanjing+2.17)
% doesnt seem to have snow? It seems like lots of noise in summer (july) up
% to ~0.3 m. 
% does it see rain, or vegetation maybe?

%% Soil moisture

% Langshisha pluvio
T = readtable('F:\13_Utrecht\03_data\data\SoilMoisture\201804_LangshishaPluvio_soilmoisture.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
soilmoisture_pluvio_ls = table2array(T(:,3:5));
time_pluviosoilmoisture_ls = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
soilmoisture_pluvio_ls(soilmoisture_pluvio_ls>0.5)=nan;
soilmoisture_pluvio_ls(soilmoisture_pluvio_ls<0.0)=nan;

plot(time_pluviosoilmoisture_ls, soilmoisture_pluvio_ls)
legend ('66 cm', '43cm', '10cm')
xlim([time_pluviosoilmoisture_ls(1) time_pluviosoilmoisture_ls(end)]);
ylabel ('Langshisha Pluvio Soil Moisture (m^3 m^{-3})')
filename = 'SoilMoisture_LangshishaPluvio'
saveas (gcf,strcat(figdir, filename), 'png')
saveas (gcf,strcat(figdir, filename), 'pdf')
savefig (gcf,strcat(figdir, filename))

% Langshisha Transect
T = readtable('F:\13_Utrecht\03_data\data\SoilMoisture\202111_LangshishaTranssect_soilmoisture.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
soilmoisture_lstransect = table2array(T(:,3:5));
time_soilmoisture_lstransect = datetime([Tt(:,1:3) Ttt(:, 4:6)]);

soilmoisture_lstransect(soilmoisture_lstransect<0.0)=nan;
plot(time_soilmoisture_lstransect, soilmoisture_lstransect(:, [3,2,1]))
legend ('47cm','23cm','12 cm') 


xlim([time_soilmoisture_lstransect(1) time_soilmoisture_lstransect(end)]);
ylabel ('Langshisha Transect Soil Moisture (m^3 m^{-3})')
filename = 'SoilMoisture_LangshishaTransect'
saveas (gcf,strcat(figdir, filename), 'png')
saveas (gcf,strcat(figdir, filename), 'pdf')
savefig (gcf,strcat(figdir, filename))

% Langshisha BC
T = readtable('F:\13_Utrecht\03_data\data\SoilMoisture\20200210_LangshishaBC_soilmoisture.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
soilmoisture_lsbc = table2array(T(:,3:5));
time_soilmoisture_lsbc = datetime([Tt(:,1:3) Ttt(:, 4:6)]);

soilmoisture_lsbc(soilmoisture_lsbc<0.0)=nan;
plot(time_soilmoisture_lsbc, soilmoisture_lsbc)
legend ('55 cm', '30cm', '10cm') 
xlim([time_soilmoisture_lsbc(1) datetime('18-Aug-2019')]);
ylabel ('Langshisha BC Soil Moisture (m^3 m^{-3})')
filename = 'SoilMoisture_LangshishaBC'
saveas (gcf,strcat(figdir, filename), 'png')
saveas (gcf,strcat(figdir, filename), 'pdf')
savefig (gcf,strcat(figdir, filename))

% Ganja La
T = readtable('F:\13_Utrecht\03_data\data\SoilMoisture\202111_GanjaLa_soilmoisture.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
soilmoisture_gl = table2array(T(:,3:5));
time_soilmoisture_gl = datetime([Tt(:,1:3) Ttt(:, 4:6)]);

soilmoisture_gl(soilmoisture_gl<0.0)=nan;
plot(time_soilmoisture_gl, soilmoisture_gl(:, [3,2,1]))
legend ('37cm', '23.5cm','10 cm') 
xlim([time_soilmoisture_gl(1) time_soilmoisture_gl(end)]);
ylabel ('GanjaLa Soil Moisture (m^3 m^{-3})')
filename = 'SoilMoisture_GanjaLa'
saveas (gcf,strcat(figdir, filename), 'png')
saveas (gcf,strcat(figdir, filename), 'pdf')
savefig (gcf,strcat(figdir, filename))

% Langtang
T = readtable('F:\13_Utrecht\03_data\data\SoilMoisture\202111_Langtang_soilmoisture.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
soilmoisture_lg = table2array(T(:,3:5));
time_soilmoisture_lg = datetime([Tt(:,1:3) Ttt(:, 4:6)]);

soilmoisture_lg(soilmoisture_lg<0.0)=nan;
plot(time_soilmoisture_lg, soilmoisture_lg(:, [3,2,1]))
legend ('59cm', '35cm','17 cm') 
xlim([time_soilmoisture_lg(1) time_soilmoisture_lg(end)]);
ylabel ('Langtang Soil Moisture (m^3 m^{-3})')
filename = 'SoilMoisture_langtang'
saveas (gcf,strcat(figdir, filename), 'png')
saveas (gcf,strcat(figdir, filename), 'pdf')
savefig (gcf,strcat(figdir, filename))

% Tangshyap
T = readtable('F:\13_Utrecht\03_data\data\SoilMoisture\202111_Tangshyap_soilmoisture.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
soilmoisture_ts = table2array(T(:,3:5));
time_soilmoisture_ts = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
figure
soilmoisture_ts(soilmoisture_ts<0.0)=nan;
plot(time_soilmoisture_ts, soilmoisture_ts(:, [3,2,1]))
legend ( '41cm', '30cm','17 cm') 
xlim([time_soilmoisture_ts(1) time_soilmoisture_ts(end)]);
ylabel ('Tangshyap Soil Moisture (m^3 m^{-3})')
filename = 'SoilMoisture_Tangshyap'
saveas (gcf,strcat(figdir, filename), 'png')
saveas (gcf,strcat(figdir, filename), 'pdf')
savefig (gcf,strcat(figdir, filename))

% tserkoRi
T = readtable('F:\13_Utrecht\03_data\data\SoilMoisture\20200210_TserkoRi_soilmoisture.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
soilmoisture_tr = table2array(T(:,3:5));
time_soilmoisture_tr = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
figure
soilmoisture_tr(soilmoisture_tr<0.0)=nan;
plot(time_soilmoisture_tr, soilmoisture_tr(:, [1,3,2]))
legend ('48 cm','25cm', '10cm') 
xlim([time_soilmoisture_tr(1) time_soilmoisture_tr(end)]);
ylabel ('TserkoRi Soil Moisture (m^3 m^{-3})')
filename = 'SoilMoisture_TserkoRi'
saveas (gcf,strcat(figdir, filename), 'png')
saveas (gcf,strcat(figdir, filename), 'pdf')
savefig (gcf,strcat(figdir, filename))

%% Streamflow

% kyanjing
T = readtable('F:\13_Utrecht\03_data\data\Discharge\Kyangjin\Kyanjing_Q_20132019.csv');
Tt = datevec(table2array(T(:,2)));
Ttt = datevec(table2array(T(:,3)));
streamflow_ky= str2double(table2array(T(:,4)));
time_streamflow_ky = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
plot(time_streamflow_ky, streamflow_ky)

% Langshihsa 2013
T = readtable('F:\13_Utrecht\03_data\data\Discharge\Langshisha\Langshisha_Q_20132016.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
streamflow_ls13= str2double(table2array(T(:,3)));
time_streamflow_ls13 = datetime([Tt(:,1:3) Ttt(:, 4:6)]);

% Langshihsa 2017
T = readtable('F:\13_Utrecht\03_data\data\Discharge\Langshisha\Langshisha_Q_20172018.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
streamflow_ls17=table2array(T(:,3));
time_streamflow_ls17 = datetime([Tt(:,1:3) Ttt(:, 4:6)]);

% Lirung
T = readtable('F:\13_Utrecht\03_data\data\Discharge\Lirung\Lirung_Q_all.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
streamflow_li= str2double(table2array(T(:,3)));
time_streamflow_li = datetime([Tt(:,1:3) Ttt(:, 4:6)]);

% plot together
figure
plot(time_streamflow_ky, streamflow_ky); hold on
plot(time_streamflow_ls13, streamflow_ls13); 
plot(time_streamflow_ls17, streamflow_ls17); 
plot(time_streamflow_li, streamflow_li); 
legend ('Kyanjing','Langshihsha','Langshisha','Lirung')
ylabel ('Streamflow (m^3 s^{-1})')
filename = 'Streamflow'
saveas (gcf,strcat(figdir, filename), 'png')
saveas (gcf,strcat(figdir, filename), 'pdf')
savefig (gcf,strcat(figdir, filename))
