clear;
clc;
close all;

max_dev = stlread("Cube_max_deviation.STL");
trisurf(max_dev, 'EdgeColor', 'k');

pbaspect([400 400 400]);
disp(max_dev.Points(1:3, :));
disp(max_dev.ConnectivityList(1, :));
