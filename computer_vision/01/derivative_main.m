close all;
clear;
clc;

img_color = imread('image_1.jpg');

%% Convert to Gray %%
img_gray = rgb2_gray(img_color);

figure;
imshow(img_color);

%% Derivative kernels %%
der_x = 0.3 * [ -1, 0, 1;-1, 0, 1;-1, 0, 1];
der_y = 0.3 * [-1, -1, -1; 0, 0, 0; 1, 1, 1];

img_dx = fnc_filter(img_gray, der_x);
img_dy = fnc_filter(img_gray, der_y);

%% Laplacian %%
laplacian = abs(img_dx) + abs(img_dy);
laplacian = uint8(laplacian);

%% Show results
figure
subplot(2, 2, 1);
imshow(img_gray);

subplot(2, 2, 2);
imshow(img_dx);

subplot(2, 2, 3);
imshow(img_dy);

subplot(2, 2, 4);
imshow(laplacian);
