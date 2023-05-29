%% Import well data
% this imports and plot the well data


% figures actually ade in new script in V2 folder
clear all
close all

addpath('D:\UU\field_data\03_data')
savedir = 'F:\13_Utrecht\05_figure\00_dataexploration\well\'
figdir =  'F:\13_Utrecht\05_figure\00_dataexploration\well\'

T = readtable('D:\UU\field_data\03_data\data\Groundwater\202111_LangshishaBottom_Groundwater.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
t1 = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
clear Tt Ttt
w1 = table2array(T(:, 3:5));

close all
plot(t1, w1(:,1)); hold on
plot(t1, w1(:,2))
wl1 = w1(:,1)*1000./(999.965*9.81)-2.07;


T = readtable('D:\UU\field_data\03_data\data\Groundwater\202111_LangshishaMid_Groundwater.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
t2 = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
clear Tt Ttt
w2 = table2array(T(:, 3:5));
 wl2 = w2(:,1)*1000./(999.965*9.81)-1.62;
plot(t2, wl2)

% bp_kpa = w2(:,2);
% bp_head = bp_kpa*1000./(999.965*9.81);
% bh_corr = bp_head + 2.780;
% compensated_water_abovetransducer = w2(:,1) - bh_corr;
% depth_to_water = 2.07-compensated_water_abovetransducer ;
% plot(t2, depth_to_water)


T = readtable('D:\UU\field_data\03_data\data\Groundwater\202111_LangshishaTop_Groundwater.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
t3 = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
clear Tt Ttt
w3 = table2array(T(:, 3:5));
 wl3 = w3(:,1)*1000./(999.965*9.81)-1.38;
 wl3(wl3<-5)=nan;
plot(t3, wl3)

figure
plot(t1, wl1-nanmean(wl1)); hold on
plot(t2, wl2-nanmean(wl2))
plot(t3, wl3-nanmean(wl3))
ylim([4 5])
ylim([4175 4180])


plot(t3, w3(:,1:2))

T = readtable('D:\UU\field_data\03_data\data\Groundwater\202111_ShalbachumBottom_Groundwater.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
t4 = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
clear Tt Ttt
w4 = table2array(T(:, 3:5));
 wl4 = w4(:,1)*1000./(999.965*9.81)-1.02;
 wl4(wl4<-5)=nan;
plot(t4, wl4)

%% compare the wells
figure
plot(t1, wl1); hold on
plot(t2, wl2)
plot(t3, wl3)
plot(t4, wl4)
legend ('Langshisha Bottom (4174m)','Langshisha Mid (4200m)', 'Langshisha Top (4301m)', 'Shalbacum (4110m)','location', 'best');
ylabel ('Depth to water (m)')
xlim([t1(1) t1(end)])
% save fig
filename = 'Well_overview'
saveas (gcf,strcat(figdir, filename), 'png')
saveas (gcf,strcat(figdir, filename), 'pdf')
savefig (gcf,strcat(figdir, filename))

% suf figure zooming to specific time
figure
plot(t1, wl1); hold on
plot(t2, wl2)
plot(t3, wl3)
plot(t4, wl4)
legend ('Langshisha Bottom (4174m)','Langshisha Mid (4200m)', 'Langshisha Top (4301m)', 'Shalbacum (4110m)','location', 'best');
ylabel ('Depth to water (m)')
tt1 = find(t1 == '23-May-2021');
tt2 = find(t1 == '23-Jun-2021');
xlim([t1(tt1) t1(tt2)])
filename = 'Well_Spring2021_zoom'
saveas (gcf,strcat(figdir, filename), 'png')
saveas (gcf,strcat(figdir, filename), 'pdf')
savefig (gcf,strcat(figdir, filename))

figure
plot(t1, wl1); hold on
plot(t2, wl2)
plot(t3, wl3)
plot(t4, wl4)
legend ('Langshisha Bottom (4174m)','Langshisha Mid (4200m)', 'Langshisha Top (4301m)', 'Shalbacum (4110m)', 'location', 'best');
ylabel ('Depth to water (m)')
tt1 = find(t1 == '02-Apr-2020');
tt2 = find(t1 == '28-Jun-2020');
xlim([t1(tt1) t1(tt2)])
filename = 'Well_Spring2020_zoom'
saveas (gcf,strcat(figdir, filename), 'png')
saveas (gcf,strcat(figdir, filename), 'pdf')
savefig (gcf,strcat(figdir, filename))
