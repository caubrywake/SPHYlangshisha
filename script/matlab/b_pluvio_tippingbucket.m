%% Look at rain
T = readtable('F:\13_Utrecht\03_data\data\TippingBuckets\20211206_TB_LangshishaBC_10271177_data.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
tp = datetime([Tt(:,1:3) Ttt(:, 4:6)]);

% 1 tip =0.2
p= ones(length(tp),1)*0.2;
T = timetable(tp, p);
tt = datetime('27-Oct-2013 00:00:00'):caldays(1):datetime('23-Oct-2021 00:00');
TT = retime(T, tt, 'sum');
p = table2array(TT);
tp = TT.tp;

close all

plot(tp, p); 
hold on;
plot(t4, (wl4-4179)*100)

%% lookat pluvio
T = readtable('F:\13_Utrecht\03_data\data\Pluvio\20211206_Pluvio_Langshisha.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
tpl = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
pl = table2array(T(:,3));
pl = table2array(T(:,3));
ta = table2array(T(:,6));
ta2 =table2array(T(:,7));
plot(tpl, ta)
plot(tpl, pl)
ylim([0 3])

hold on
plot(t1, w1(:,3))
plot(t2, w2(:,3))
plot(t3, w3(:,3))
plot(t4, w4(:,3))
%% air pressur ekyanjing
T = readtable('F:\13_Utrecht\03_data\data\AWS\Kyangjin_ICIMOD.csv');
Tt = datevec(table2array(T(:,1)));
Ttt = datevec(table2array(T(:,2)));
taws = datetime([Tt(:,1:3) Ttt(:, 4:6)]);
pres = table2array(T(:,16))/10;
plot(taws, pres)
hold on
plot(t1, w1(:,2))
plot(t2, w2(:,2))
plot(t3, w3(:,2))
plot(t4, w4(:,2))
ylim([60 80])

figure
plot(t2, w2(:,2)); hold on
plot(t2, w2(:, 1)+ nanmean(w2(:,2)-w2(:,1)))

figure
plot(t1, w1(:,2)); hold on
plot(t1, w1(:, 1)+ nanmean(w1(:,2)-w1(:,1)))

a = find(w3(:,1)<=0);
w3(a,1)=nan;
a = find(w3(:,2)<=0);
w3(a,2)=nan;
figure

plot(t3, w3(:,2)); hold on
plot(t3, w3(:, 1)+ nanmean(w3(:,2)-w3(:,1)))

figure

plot(t4, w4(:,2)); hold on
plot(t4, w4(:, 1)+ nanmean(w4(:,2)-w4(:,1)))



