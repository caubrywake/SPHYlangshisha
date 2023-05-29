%% Precipitation record
clear all
close all

tall = datetime('2012-05-03'):days(1):datetime('2021-07-01');

%% loading Langshisha TB * 2013, 2014 and 2016 seasons
fn = 'D:\UU\field_data\TippingBuckets\TB_LangshishaPluvio_10271176_data.csv'
T =  readtable(fn);

Tt = datevec(table2array(T(:,1)));Ttt = datevec(table2array(T(:,2)));
t = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
tt = dateshift(t(1), 'start', 'day'):days(1):dateshift(t(end), 'end', 'day'); % making a continuous daily timestep covering the same duration
x= ones(length(t),1)*0.2;% as one tip is 0.2 mm
T = timetable(t, x); 

TB = table2array(retime(T, tt, 'sum'));
TBt = tt';
plot(TBt, TB)
% remove bad period
a  = 1;
b = find(TBt  == '2013-05-23');
TB(a:b)=nan;
a = find(TBt == '2015-01-02');
b = find(TBt  == '2015-10-01');
TB(a:b)=nan;
plot(TBt, TB)
a = find(TBt == '2016-05-27');
b = find(TBt  == '2016-06-25');
TB(a:b)=nan;
plot(TBt, TB)
TBt_ls = TBt;
TB_ls = TB;

T = timetable(TBt, TB);
TT = retime(T, tall, 'fillwithmissing');
TB_all(:,1) = table2array(TT);

%% Langshihsa basecamp: 2014-2021, missing 2019 season
fn = 'D:\UU\field_data\TippingBuckets\20211206_TB_LangshishaBC_10271177_data.csv'
T =  readtable(fn);

Tt = datevec(table2array(T(:,1)));Ttt = datevec(table2array(T(:,2)));
t = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
tt = dateshift(t(1), 'start', 'day'):days(1):dateshift(t(end), 'end', 'day'); % making a continuous daily timestep covering the same duration
x= ones(length(t),1)*0.2;% as one tip is 0.2 mm
T = timetable(t, x); 

TB = table2array(retime(T, tt, 'sum'));
TBt = tt';
plot(TBt, TB); hold on
% remove bad period
a  = find(TBt  == '2013-12-02');
b = find(TBt  == '2014-05-05');
TB(a:b)=nan;
a = find(TBt == '2019-06-27');
b = find(TBt  == '2019-10-29');
TB(a:b)=nan;
a = find(TBt == '2021-07-11');
b = find(TBt  == '2021-10-11');
TB(a:b)=nan;
plot(TBt, TB)

TBt_lsBC = TBt;
TB_lsBC = TB;

T = timetable(TBt, TB);
TT = retime(T, tall, 'fillwithmissing');
TB_all(:,2) = table2array(TT);

%% Shalbacum
fn = 'D:\UU\field_data\TippingBuckets\20211206_TB_Shalbachum_10271180_data.csv'
T =  readtable(fn);

Tt = datevec(table2array(T(:,1)));Ttt = datevec(table2array(T(:,2)));
t = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
tt = dateshift(t(1), 'start', 'day'):days(1):dateshift(t(end), 'end', 'day'); % making a continuous daily timestep covering the same duration
x= ones(length(t),1)*0.2;% as one tip is 0.2 mm
T = timetable(t, x); 

TB = table2array(retime(T, tt, 'sum'));
TBt = tt';
plot(TBt, TB); hold on
% remove bad period
a  = find(TBt  == '2015-08-18');
b = find(TBt  == '2015-10-30');
TB(a:b)=nan;
a = find(TBt == '2019-05-01');
b = find(TBt  == '2019-10-29');
TB(a:b)=nan;
a = find(TBt == '2020-05-23');
b = find(TBt  == '2020-08-08');
TB(a:b)=nan;
a = find(TBt == '2021-05-27');
b = find(TBt  == '2022-07-15');
TB(a:b)=nan;
a = find(TBt == '2021-07-28');
b = find(TBt  == '2021-10-16');
TB(a:b)=nan;

plot(TBt, TB)

TBt_sh = TBt;
TB_sh = TB;

T = timetable(TBt, TB);
TT = retime(T, tall, 'fillwithmissing');
TB_all(:,3) = table2array(TT);

%% Morimoto
fn = 'D:\UU\field_data\TippingBuckets\20211206_TB_MorimotoBC_10271179_data.csv'
T =  readtable(fn);

Tt = datevec(table2array(T(:,1)));Ttt = datevec(table2array(T(:,2)));
t = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
tt = dateshift(t(1), 'start', 'day'):days(1):dateshift(t(end), 'end', 'day'); % making a continuous daily timestep covering the same duration
x= ones(length(t),1)*0.2;% as one tip is 0.2 mm
T = timetable(t, x); 

TB = table2array(retime(T, tt, 'sum'));
TBt = tt';
plot(TBt, TB); hold on
% remove bad period
a  = find(TBt  == '2015-03-01');
b = find(TBt  == '2015-06-07');
TB(a:b)=nan;
a = find(TBt == '2021-07-01');
b = find(TBt  == '2021-11-13');
TB(a:b)=nan;
a = find(TBt == '2020-05-23');
b = find(TBt  == '2020-08-08');
TB(a:b)=nan;
a = find(TBt == '2021-05-27');
b = find(TBt  == '2022-07-15');
TB(a:b)=nan;
a = find(TBt == '2021-07-28');
b = find(TBt  == '2021-10-16');
TB(a:b)=nan;

plot(TBt, TB)

TBt_mm = TBt;
TB_mm = TB;

T = timetable(TBt, TB);
TT = retime(T, tall, 'fillwithmissing');
TB_all(:,4) = table2array(TT);

%% Kyanjing

fn = 'D:\UU\field_data\TippingBuckets\TB_Kyangjin_981620_data.csv'
T =  readtable(fn);

Tt = datevec(table2array(T(:,1)));Ttt = datevec(table2array(T(:,2)));
t = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
tt = dateshift(t(1), 'start', 'day'):days(1):dateshift(t(end), 'end', 'day'); % making a continuous daily timestep covering the same duration
x= ones(length(t),1)*0.192;% as one tip is 0.192 mm
T = timetable(t, x); 

TB = table2array(retime(T, tt, 'sum'));
TBt = tt';
plot(TBt, TB); hold on
% remove bad period
a  = find(TBt  == '2013-07-28');
b = find(TBt  == '2013-10-21');
TB(a:b)=nan;
a = find(TBt == '2021-07-01');
b = find(TBt  == '2021-11-13');
TB(a:b)=nan;
a = find(TBt == '2020-05-23');
b = find(TBt  == '2020-08-08');
TB(a:b)=nan;
a = find(TBt == '2021-05-27');
b = find(TBt  == '2022-07-15');
TB(a:b)=nan;
a = find(TBt == '2021-07-28');
b = find(TBt  == '2021-10-16');
TB(a:b)=nan;

plot(TBt, TB)

TBt_ky= TBt;
TB_ky = TB;

T = timetable(TBt, TB);
TT = retime(T, tall, 'fillwithmissing');
TB_all(:,5) = table2array(TT);%%

%% Load the pluvio to compare
T = readtable('D:\UU\field_data\Pluvio\20211206_Pluvio_Langshisha.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
t = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
x = table2array(T(:,3));
T = timetable(t,x);  TT= retime(T, 'daily', 'sum');
TTT = retime(TT, tall, "fillwithmissing");
TB = table2array(TTT);
TBt = TTT.t;
figure
plot(TBt, TB); hold on
% remove bad period
a  = find(TBt  == '2014-12-16');
b = find(TBt  == '2015-10-21');
TB(a:b)=nan;

TBt_pl= TBt;
TB_pl = TB;

TB_all(:,6) = TB;%%


%% Include ERA form dhiraj
T = table2array(readtable('D:\UU\field_data\ERA_p_langtang.csv'));
t = datetime(T(:,1:6));
pERA = T(:,7);
T = timetable(t,pERA);  TT= retime(T, 'daily', 'sum');
TTT = retime(TT, tall, "fillwithmissing");
TB_era = table2array(TTT);
TBt_era = TTT.t;
TB_all(:,7)=TB_era;

%% Plot all together
close all
figure
plot(TBt_mm, TB_mm); hold on
plot(TBt_sh, TB_sh);
plot(TBt_lsBC, TB_lsBC);
plot(TBt_ky, TB_ky);
plot(TBt_ls, TB_ls)
plot(TBt_pl,TB_pl )
plot(TBt_era, TB_era)
legend ('mm', 'sh','lsBC','ky', 'ls', 'pl', 'era')

%% Best correlation is between LS and MM and LS and LSBC
corrcoef(TB_all(:,1),TB_all(:,2), 'rows', 'pairwise')
corrcoef(TB_all(:,1),TB_all(:,3), 'rows', 'pairwise')
corrcoef(TB_all(:,1),TB_all(:,4), 'rows', 'pairwise')
corrcoef(TB_all(:,1),TB_all(:,5), 'rows', 'pairwise')

corrcoef(TB_all(:,2),TB_all(:,3), 'rows', 'pairwise')
corrcoef(TB_all(:,2),TB_all(:,4), 'rows', 'pairwise')

corrcoef(TB_all(:,3),TB_all(:,4), 'rows', 'pairwise')

corrcoef(TB_all(:,3),TB_all(:,5), 'rows', 'pairwise')

scatter(TB_all(:,1),TB_all(:,2)); hold on
scatter(TB_all(:,1),TB_all(:,3))
scatter(TB_all(:,1),TB_all(:,4))
scatter(TB_all(:,1),TB_all(:,3))

%%b Infill the pluio instead
corrcoef(TB_all(:,6),TB_all(:,1), 'rows', 'pairwise')
corrcoef(TB_all(:,6),TB_all(:,2), 'rows', 'pairwise')
corrcoef(TB_all(:,6),TB_all(:,3), 'rows', 'pairwise')
corrcoef(TB_all(:,6),TB_all(:,4), 'rows', 'pairwise')
corrcoef(TB_all(:,6),TB_all(:,5), 'rows', 'pairwise')
corrcoef(TB_all(:,6),TB_all(:,7), 'rows', 'pairwise')


corrcoef(TB_all(:,2),TB_all(:,3), 'rows', 'pairwise')
corrcoef(TB_all(:,2),TB_all(:,4), 'rows', 'pairwise')

corrcoef(TB_all(:,3),TB_all(:,4), 'rows', 'pairwise')

corrcoef(TB_all(:,3),TB_all(:,5), 'rows', 'pairwise')

scatter(TB_all(:,1),TB_all(:,2)); hold on
scatter(TB_all(:,1),TB_all(:,3))
scatter(TB_all(:,1),TB_all(:,4))


%% Infilling pluvio

% regression with langshihsa
% remove nan
x = TB_all(:,1);
y = TB_all(:,6);
ind = isnan(x) | isnan(y);
x(ind) = [];
y(ind) = [];
% fit in a first lin regression
fit1 = polyfit(x,y,1);
y1 = polyval(fit1,  TB_all(:,1));
y1(y1==fit1(2))=0;

% regtression with mrimoto
x = TB_all(:,4);
y = TB_all(:,6);
ind = isnan(x) | isnan(y);
x(ind) = [];
y(ind) = [];
% fit in a first lin regression
fit2 = polyfit(x,y,1);
y2 = polyval(fit2,  TB_all(:,6));
y2(y2==fit2(2))=0;

% regression with baecamp
x = TB_all(:,6);
y = TB_all(:,2);
ind = isnan(x) | isnan(y);
x(ind) = [];
y(ind) = [];
% fit in a first lin regression
fit3 = polyfit(x,y,1);
y3 = polyval(fit3,  TB_all(:,2));
y3(y3==fit3(2))=0;

% regression with era
x = TB_all(:,7);
y = TB_all(:,6);
ind = isnan(x) | isnan(y);
x(ind) = [];
y(ind) = [];
% fit in a first lin regression
fit4 = polyfit(x,y,1);
y4 = polyval(fit4,  TB_all(:,7));
y4(y4==fit4(2))=0;

%% Replace values
x = TB_all(:,6);
a = find(isnan(x));

x(a)= y4(a);
plot(tall, x); hold on
find(isnan(x));

plot(tall, x)
hold on
TB_all(:,8)=x;

% Remove values mora than 40
a = find(TB_all>40);
TB_all(a)=40;

close all
figure
plot(tall, TB_all(:,8)); hold on
plot(tall,TB_all(:, 6), 'k');
xlim([datetime('01-Jan-2014') datetime('31-Dec-2020')])
legend('Filled with lin. regression from ERA', 'Langshihsa Pluvio')
ylabel ('Daily Precip (mm)')
saveas(gcf,'C:\SPHY3\analysis\model_output\fig\dataplot\InfileldLangshishaPluvioPrecip.png')
%% Do annual cumulatibe sum

tvec = datevec(tall);

a = find(tvec(:,2)==01 & tvec(:,3)==01)
for ii = 1:8;
x = TB_all(:,ii);
for i = 1:length(a)-1
   xcum(a(i):a(i)+365,1) = cumsum(x(a(i):a(i)+365));
   tcum(a(i):a(i)+365,1) = tall(a(i):a(i)+365);
end 
TBcum(:, ii)=xcum;

end 
T = timetable
figure
plot(tcum,TBcum(:,7), 'LineWidth', 1); hold on
plot(tcum,TBcum(:,8), 'LineWidth', 1)
legend('era', 'pluvio infilled', 'location', 'best')
ylabel ('Annual Cumulative Precip (mm)')
saveas(gcf,'C:\SPHY3\analysis\model_output\fig\dataplot\InfileldLangshishaPluvioPrecip_cumulative.png')

figure
plot(tcum,TBcum(:,6:8), 'LineWidth', 1);
legend('pluvio','era' , 'filled')

T = timetable(tall', TB_all);
TT = retime(T, 'yearly', 'sum');
p_annual = table2array(TT);
filled  = p_annual(:,8)
pluvio = p_annual(:,6)
ratio = pluvio./filled
mean(ratio(5:9))

TT = timetable(tall',TB_all(:,8))
% Export table
writetimetable(TT,'D:\UU\field_data\processed\Pdaily_Ls_infilledw_20120503_20210701.csv')

%% Correct precip with wind
% inport wnd
T = readtable('D:\UU\field_data\Pluvio\20211206_Pluvio_Langshisha.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
t = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
x = table2array(T(:,10));
T = timetable(t,x);  TT= retime(T, 'daily', 'mean');
TTT = retime(TT, tall, "fillwithmissing");
U = table2array(TTT);
Ut = TTT.t;
plot(Ut, U)

% Fill Gaps with other years
values = U;
time = Ut;
% Find the indices with missing values (NaNs)
missingIndices = find(isnan(values));

% Loop through each missing index
for i = 1:numel(missingIndices)
    currentIndex = missingIndices(i);
    time_curIndex = time(currentIndex);
    % Find the previous year's corresponding index with the same day of the year
    previousYear = year(time(currentIndex)) + 1;
    sameDayIndices = find(year(time) == previousYear &  month(time) == month(time(currentIndex)) & day(time) == day(time(currentIndex)));
    time_prevIndex = time(sameDayIndices);
    previousIndex = sameDayIndices(end);  % Select the last index for the same day
    
    % Fill the missing value with the corresponding value from the previous year
    values(currentIndex) = values(previousIndex);
end

figure
plot(time, values); hold on
plot(Ut, U);
legend('Infilled from following years', 'Wind Speed', 'location', 'best')
ylabel ('Daily Mean Wind Speed (ms^{-1})')
saveas(gcf,'C:\SPHY3\analysis\model_output\fig\dataplot\InfilledLangshisha_WindSpeed.png')

% Correct precip
% import precip
T = readtable('D:\UU\field_data\processed\Pdaily_Ls_infilledw_20120503_20210701.csv');
t = T.Time;
p = T.Var1;


% applying undercatch correction to the precipitation data using the winf
% speed
   a = 0.728;
   b = 0.230;
   c = 0.336;
figure
CE = (a) * exp(-b*values) + c;
ylabel ('Catch Efficency')
saveas(gcf,'C:\SPHY3\analysis\model_output\fig\dataplot\WindCorrection_CE.png')

Pcorr = p.*(1./CE);
a = find(isnan(Pcorr));
Pcorr(a) = p(a);
figure
subplot(2,1,1);
plot(t, Pcorr); hold on
plot(t, p)
legend('Corrected precip','precip', 'location','best');
ylabel ('Daily Precipitation (mm)');
subplot(2,1,2)
plot(t, cumsum(Pcorr)); hold on
plot(t, cumsum(p));
legend('Corrected precip','precip', 'location','best');
ylabel ('Cumulative Daily Precipitation (mm)');
saveas(gcf,'C:\SPHY3\analysis\model_output\fig\dataplot\Pcorr.png')

TT = timetable(t, Pcorr);
writetimetable(TT,'D:\UU\field_data\processed\Pdaily_Ls_infilledw_CEcorr_20120503_20210701.csv')