%%% temp lapse rates
% TemperatureD:
% Langshisha and Kyanjing temperature regime
T = readtable('D:\UU\field_data\03_data\data\AWS\Kyangjin_ICIMOD.csv');
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
T = readtable('D:\UU\field_data\03_data\data\Pluvio\20211206_Pluvio_Langshisha.csv');
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
T = readtable('D:\UU\field_data\03_data\data\Pluvio\Pluvio_GanjaLa.csv');
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
T = readtable('D:\UU\field_data\03_data\data\Pluvio\Pluvio_Yala.csv');
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
T = readtable('D:\UU\field_data\03_data\data\Pluvio\20211206_Pluvio_Morimoto.csv');
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
saveas(gcf,'C:\SPHY3\analysis\model_output\fig\dataplot\TempGradietn_Stationtimeseries.png')

% Make a table with all the montlhy temps
T1 = timetable(time_kyanjing_mth, ta_kyanjing_mth);
T2 = timetable(time_pl_ls_mth, ta_pl_ls_mth);
T3 = timetable(time_pl_gl_mth, ta_pl_gl_mth);
T4 = timetable(time_pl_ya_mth, ta_pl_ya_mth);
T5 = timetable(time_pl_mm_mth, ta_pl_mm_mth);
TT = synchronize(T1, T2, T3, T4, T5);

t = TT.time_kyanjing_mth;
x = table2array(TT);

%% decC/100m
elev = [3862, 4452, 4361, 4831, 4919]
tvec = datevec(t);
for i = 1:12;
tidx = find(tvec(:,2)==i);
for ii =1:5
   gr(i, ii)= mean(x(tidx, ii), 'omitnan');
end 
subplot(4,3,i)
scatter(elev, gr(i, :))
lsline
xx = gr(i, :); yy= elev;
a = find(isnan(xx));
xx(a)=[];yy(a)=[]

p = polyfit(yy, xx, 1);
gr_elev(i) = p(1)
end

i = 2
